//! Transaction sighash helpers

use crate::messages::{OutPoint, Payload, Tx, TxOut};
use crate::script::op_codes::{OP_CHECKSIG, OP_CODESEPARATOR};
use crate::script::{next_op, op_codes, Script};
use crate::util::{sha256d, var_int, Hash256, Serializable, ChainGangError};
use byteorder::{LittleEndian, WriteBytesExt};
use std::io::Write;

/// Signs all of the outputs
pub const SIGHASH_ALL: u8 = 0x01;
/// Sign none of the outputs so that they may be spent anywhere
pub const SIGHASH_NONE: u8 = 0x02;
/// Sign only the output paired with the the input
pub const SIGHASH_SINGLE: u8 = 0x03;
/// Sign only the input so others may inputs to the transaction
pub const SIGHASH_ANYONECANPAY: u8 = 0x80;
/// Bitcoin Cash / SV sighash flag for use on outputs after the fork
pub const SIGHASH_FORKID: u8 = 0x40;

/// The 24-bit fork ID for Bitcoin Cash / SV
const FORK_ID: u32 = 0;

// Other useful flags
//pub const ALL_FORKID: u8 = SIGHASH_ALL | SIGHASH_FORKID;
//const NONE_FORKID: u8 = SIGHASH_NONE | SIGHASH_FORKID;
//const SINGLE_FORKID: u8 = SIGHASH_SINGLE | SIGHASH_FORKID;
//const ALL_ANYONECANPAY_FORKID: u8 = ALL_FORKID | SIGHASH_ANYONECANPAY;
//const NONE_ANYONECANPAY_FORKID: u8 = NONE_FORKID | SIGHASH_ANYONECANPAY;
//const SINGLE_ANYONECANPAY_FORKID: u8 = SINGLE_FORKID | SIGHASH_ANYONECANPAY;

/// Generates a transaction digest for signing
///
/// This will use either BIP-143 or the legacy algorithm depending on if SIGHASH_FORKID is set.
///
/// # Arguments
///
/// * `tx` - Spending transaction
/// * `n_input` - Spending input index
/// * `script_code` - The lock_script of the output being spent. This may be a subset of the
///   lock_script if OP_CODESEPARATOR is used.
/// * `satoshis` - The satoshi amount in the output being spent
/// * `sighash_type` - Sighash flags
/// * `cache` - Cache to store intermediate values for future sighash calls.
pub fn sighash(
    tx: &Tx,
    n_input: usize,
    script_code: &[u8],
    satoshis: i64,
    sighash_type: u8,
    cache: &mut SigHashCache,
) -> Result<Hash256, ChainGangError> {
    // use default value of 0
    let checksig_index: usize = 0;
    sighash_checksig_index(
        tx,
        n_input,
        script_code,
        checksig_index,
        satoshis,
        sighash_type,
        cache,
    )
}

// Same as above `sighash` function with an additional `checksig_index` parameter
pub fn sighash_checksig_index(
    tx: &Tx,
    n_input: usize,
    script_code: &[u8],
    checksig_index: usize,
    satoshis: i64,
    sighash_type: u8,
    cache: &mut SigHashCache,
) -> Result<Hash256, ChainGangError> {
    if sighash_type & SIGHASH_FORKID != 0 {
        bip143_sighash(
            tx,
            n_input,
            script_code,
            checksig_index,
            satoshis,
            sighash_type,
            cache,
        )
    } else {
        legacy_sighash(tx, n_input, script_code, checksig_index, sighash_type)
    }
}

/// Cache for sighash intermediate values to avoid quadratic hashing
///
/// This is only valid for one transaction, but may be used for multiple signatures.
pub struct SigHashCache {
    hash_prevouts: Option<Hash256>,
    hash_sequence: Option<Hash256>,
    hash_outputs: Option<Hash256>,
}

impl SigHashCache {
    /// Creates a new cache
    pub fn new() -> SigHashCache {
        SigHashCache {
            hash_prevouts: None,
            hash_sequence: None,
            hash_outputs: None,
        }
    }
    // getter/setter/clear hash_prevouts
    pub fn hash_prevouts(&self) -> Option<&Hash256> {
        self.hash_prevouts.as_ref()
    }

    pub fn set_hash_prevouts(&mut self, hash: Hash256) {
        self.hash_prevouts = Some(hash);
    }

    pub fn clear_hash_prevouts(&mut self) {
        self.hash_prevouts = None;
    }
    //getter/setter/clear hash_sequence
    pub fn hash_sequence(&self) -> Option<&Hash256> {
        self.hash_sequence.as_ref()
    }

    pub fn set_hash_sequence(&mut self, hash: Hash256) {
        self.hash_sequence = Some(hash);
    }

    pub fn clear_hash_sequence(&mut self) {
        self.hash_sequence = None;
    }

    //getter/setter/clear hash_outputs
    pub fn hash_outputs(&self) -> Option<&Hash256> {
        self.hash_outputs.as_ref()
    }

    pub fn set_hash_outputs(&mut self, hash: Hash256) {
        self.hash_outputs = Some(hash)
    }

    pub fn clear_hash_outputs(&mut self) {
        self.hash_outputs = None;
    }
}

impl Default for SigHashCache {
    fn default() -> Self {
        Self::new()
    }
}

/// Generates a transaction digest for signing using BIP-143
///
/// This is to be used for all tranasctions after the August 2017 fork.
/// It fixing quadratic hashing and includes the satoshis spent in the hash.
fn bip143_sighash(
    tx: &Tx,
    n_input: usize,
    script_code: &[u8],
    checksig_index: usize,
    satoshis: i64,
    sighash_type: u8,
    cache: &mut SigHashCache,
) -> Result<Hash256, ChainGangError> {
    // The intention is to return any error(s) without any extra processing & according to the
    // docs the '?' operator is the most idiomatic & concise.
    let s = sig_hash_preimage_checksig_index(
        tx,
        n_input,
        script_code,
        checksig_index,
        satoshis,
        sighash_type,
        cache,
    )?;
    Ok(sha256d(&s))
}

// Given a script and operator return a Vec of positions of the operator
fn find_all_occurances_of(script_code: &[u8], operation: u8) -> Vec<usize> {
    let positions: Vec<usize> = script_code
        .iter()
        .enumerate()
        .filter_map(|(index, &value)| {
            if value == operation {
                Some(index)
            } else {
                None
            }
        })
        .collect();
    positions
}

// Remove instances of OP_CODESEPARATOR from the script_code
// extract_subscript is the function that takes the script and the index of OP_CHECKSIG, and extracts the subscript)
fn extract_subscript(script_code: &[u8], checksig_index: usize) -> Result<Vec<u8>, ChainGangError> {
    
    
    if !script_code.contains(&OP_CODESEPARATOR) {
        // if there is no OP_CODESEPARATOR there is nothing to do
        Ok(script_code.to_vec())
    } else {
        // Look for all OP_CHECKSIG
        let checksig_positions: Vec<usize> = find_all_occurances_of(script_code, OP_CHECKSIG);
        if checksig_index > (checksig_positions.len() -1) {
            let err_msg = format!("checksig_index {} exceeds the number of OP_CHECKSIGs ({}) found in code", checksig_index, checksig_positions.len());
            return Err(ChainGangError::BadArgument(err_msg));
        };

        let checksig_pos = checksig_positions.get(checksig_index).unwrap_or(&0);

        // Look for all OP_CODESEPARATOR
        let codeseparator_positions: Vec<usize> =
            find_all_occurances_of(script_code, OP_CODESEPARATOR);

        // We need to find the first OP_CODESEPARATOR before the OP_CHECKSIG pos
        let start_subscript: usize = if codeseparator_positions.len() < 2 {
            0
        } else {
            let filtered_code_pos: Vec<usize> = codeseparator_positions
                .iter()
                .copied()
                .filter(|pos| pos < checksig_pos)
                .collect();
            *filtered_code_pos.last().unwrap_or(&0)
        };

        let mut sub_script = Vec::with_capacity(script_code.len() - start_subscript);
        let mut i = start_subscript;

        while i < script_code.len() {
            let next = next_op(i, script_code);
            if script_code[i] != op_codes::OP_CODESEPARATOR {
                sub_script.extend_from_slice(&script_code[i..next]);
            }
            i = next;
        }
        Ok(sub_script)
    }
}

/// Generates the transaction digest for signing using the legacy algorithm
///
/// This is used for all transaction validation before the August 2017 fork.
fn legacy_sighash(
    tx: &Tx,
    n_input: usize,
    script_code: &[u8],
    checksig_index: usize,
    sighash_type: u8,
) -> Result<Hash256, ChainGangError> {
    if n_input >= tx.inputs.len() {
        return Err(ChainGangError::BadArgument("input out of tx_in range".to_string()));
    }

    let mut s = Vec::with_capacity(tx.size());
    let base_type = sighash_type & 31;
    let anyone_can_pay = sighash_type & SIGHASH_ANYONECANPAY != 0;

    // Remove instances of OP_CODESEPARATOR from the script_code
    let sub_script = extract_subscript(script_code, checksig_index)?;

    // Serialize the version
    s.write_u32::<LittleEndian>(tx.version)?;

    // Serialize the inputs
    let n_inputs = if anyone_can_pay { 1 } else { tx.inputs.len() };
    var_int::write(n_inputs as u64, &mut s)?;
    for i in 0..tx.inputs.len() {
        let i = if anyone_can_pay { n_input } else { i };
        let mut tx_in = tx.inputs[i].clone();
        if i == n_input {
            tx_in.unlock_script = Script(Vec::with_capacity(4 + sub_script.len()));
            tx_in.unlock_script.0.extend_from_slice(&sub_script);
        } else {
            tx_in.unlock_script = Script(vec![]);
            if base_type == SIGHASH_NONE || base_type == SIGHASH_SINGLE {
                tx_in.sequence = 0;
            }
        }
        tx_in.write(&mut s)?;
        if anyone_can_pay {
            break;
        }
    }

    // Serialize the outputs
    let tx_out_list = if base_type == SIGHASH_NONE {
        vec![]
    } else if base_type == SIGHASH_SINGLE {
        if n_input >= tx.outputs.len() {
            return Err(ChainGangError::BadArgument("input out of tx_out range".to_string()));
        }
        let mut truncated_out = tx.outputs.clone();
        truncated_out.truncate(n_input + 1);
        truncated_out
    } else {
        tx.outputs.clone()
    };
    var_int::write(tx_out_list.len() as u64, &mut s)?;
    for (i, tx_out) in tx_out_list.iter().enumerate() {
        if i == n_input && base_type == SIGHASH_SINGLE {
            let empty = TxOut {
                satoshis: -1,
                lock_script: Script(vec![]),
            };
            empty.write(&mut s)?;
        } else {
            tx_out.write(&mut s)?;
        }
    }

    // Serialize the lock time
    s.write_u32::<LittleEndian>(tx.lock_time)?;

    // Append the sighash_type and finally double hash the result
    s.write_u32::<LittleEndian>(sighash_type as u32)?;
    Ok(sha256d(&s))
}

pub fn sig_hash_preimage(
    tx: &Tx,
    n_input: usize,
    script_code: &[u8],
    satoshis: i64,
    sighash_type: u8,
    cache: &mut SigHashCache,
) -> Result<Vec<u8>, ChainGangError> {
    // use default value of 0
    let checksig_index: usize = 0;
    sig_hash_preimage_checksig_index(
        tx,
        n_input,
        script_code,
        checksig_index,
        satoshis,
        sighash_type,
        cache,
    )
}

// this code was duplicated from bip143_sighash above (that function now calls this one)
// as above with checksig_index
pub fn sig_hash_preimage_checksig_index(
    tx: &Tx,
    n_input: usize,
    script_code: &[u8],
    checksig_index: usize,
    satoshis: i64,
    sighash_type: u8,
    cache: &mut SigHashCache,
) -> Result<Vec<u8>, ChainGangError> {
    if n_input >= tx.inputs.len() {
        return Err(ChainGangError::BadArgument("input out of tx_in range".to_string()));
    }

    let mut s = Vec::with_capacity(tx.size());
    let base_type = sighash_type & 31;
    let anyone_can_pay = sighash_type & SIGHASH_ANYONECANPAY != 0;

    // Remove instances of OP_CODESEPARATOR from the script_code
    let sub_script = extract_subscript(script_code, checksig_index)?;

    // Serialize the version
    s.write_u32::<LittleEndian>(tx.version)?;
    // 2. Serialize hash of prevouts
    if !anyone_can_pay {
        if cache.hash_prevouts.is_none() {
            let mut prev_outputs = Vec::with_capacity(OutPoint::SIZE * tx.inputs.len());
            for input in tx.inputs.iter() {
                input.prev_output.write(&mut prev_outputs)?;
            }
            cache.hash_prevouts = Some(sha256d(&prev_outputs));
        }
        s.write_all(&cache.hash_prevouts.unwrap().0)?;
    } else {
        s.write_all(&[0; 32])?;
    }

    // 3. Serialize hash of sequences
    if !anyone_can_pay && base_type != SIGHASH_SINGLE && base_type != SIGHASH_NONE {
        if cache.hash_sequence.is_none() {
            let mut sequences = Vec::with_capacity(4 * tx.inputs.len());
            for tx_in in tx.inputs.iter() {
                sequences.write_u32::<LittleEndian>(tx_in.sequence)?;
            }
            cache.hash_sequence = Some(sha256d(&sequences));
        }
        s.write_all(&cache.hash_sequence.unwrap().0)?;
    } else {
        s.write_all(&[0; 32])?;
    }

    // 4. Serialize prev output
    tx.inputs[n_input].prev_output.write(&mut s)?;

    // 5. Serialize input script
    var_int::write(sub_script.len() as u64, &mut s)?;
    s.write_all(&sub_script)?;

    // 6. Serialize satoshis
    s.write_i64::<LittleEndian>(satoshis)?;

    // 7. Serialize sequence
    s.write_u32::<LittleEndian>(tx.inputs[n_input].sequence)?;

    // 8. Serialize hash of outputs
    if base_type != SIGHASH_SINGLE && base_type != SIGHASH_NONE {
        if cache.hash_outputs.is_none() {
            let mut size = 0;
            for tx_out in tx.outputs.iter() {
                size += tx_out.size();
            }
            let mut outputs = Vec::with_capacity(size);
            for tx_out in tx.outputs.iter() {
                tx_out.write(&mut outputs)?;
            }
            cache.hash_outputs = Some(sha256d(&outputs));
        }
        s.write_all(&cache.hash_outputs.unwrap().0)?;
    } else if base_type == SIGHASH_SINGLE && n_input < tx.outputs.len() {
        let mut outputs = Vec::with_capacity(tx.outputs[n_input].size());
        tx.outputs[n_input].write(&mut outputs)?;
        s.write_all(&sha256d(&outputs).0)?;
    } else {
        s.write_all(&[0; 32])?;
    }

    // 9. Serialize lock_time
    s.write_u32::<LittleEndian>(tx.lock_time)?;

    // 10. Serialize hash type
    s.write_u32::<LittleEndian>((FORK_ID << 8) | sighash_type as u32)?;
    Ok(s)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::address::addr_decode;
    use crate::messages::{OutPoint, TxIn};
    use crate::network::Network;
    use crate::script::op_codes::*;
    use crate::transaction::p2pkh;
    use hex;

    #[test]
    fn bip143_sighash_test() {
        let lock_script =
            hex::decode("76a91402b74813b047606b4b3fbdfb1a6e8e053fdb8dab88ac").unwrap();
        let addr = "mfmKD4cP6Na7T8D87XRSiR7shA1HNGSaec";
        let hash160 = addr_decode(addr, Network::BSV_Testnet).unwrap().0;
        let tx = Tx {
            version: 2,
            inputs: vec![TxIn {
                prev_output: OutPoint {
                    hash: Hash256::decode(
                        "f671dc000ad12795e86b59b27e0c367d9b026bbd4141c227b9285867a53bb6f7",
                    )
                    .unwrap(),
                    index: 0,
                },
                unlock_script: Script(vec![]),
                sequence: 0,
            }],
            outputs: vec![
                TxOut {
                    satoshis: 100,
                    lock_script: p2pkh::create_lock_script(&hash160),
                },
                TxOut {
                    satoshis: 259899900,
                    lock_script: p2pkh::create_lock_script(&hash160),
                },
            ],
            lock_time: 0,
        };
        let mut cache = SigHashCache::new();
        let sighash_type = SIGHASH_ALL | SIGHASH_FORKID;
        let sighash =
            bip143_sighash(&tx, 0, &lock_script, 0, 260000000, sighash_type, &mut cache).unwrap();
        let expected = "1e2121837829018daf3aeadab76f1a542c49a3600ded7bd74323ee74ce0d840c";
        assert!(sighash.0.to_vec() == hex::decode(expected).unwrap());
        assert!(cache.hash_prevouts.is_some());
        assert!(cache.hash_sequence.is_some());
        assert!(cache.hash_outputs.is_some());
    }

    #[test]
    fn legacy_sighash_test() {
        let lock_script =
            hex::decode("76a914d951eb562f1ff26b6cbe89f04eda365ea6bd95ce88ac").unwrap();
        let tx = Tx {
            version: 1,
            inputs: vec![TxIn {
                prev_output: OutPoint {
                    hash: Hash256::decode(
                        "bf6c1139ea01ca054b8d00aa0a088daaeab4f3b8e111626c6be7d603a9dd8dff",
                    )
                    .unwrap(),
                    index: 0,
                },
                unlock_script: Script(vec![]),
                sequence: 0xffffffff,
            }],
            outputs: vec![TxOut {
                satoshis: 49990000,
                lock_script: Script(
                    hex::decode("76a9147865b0b301119fc3eadc7f3406ff1339908e46d488ac").unwrap(),
                ),
            }],
            lock_time: 0,
        };
        let sighash = legacy_sighash(&tx, 0, &lock_script, 0, SIGHASH_ALL).unwrap();
        let expected = "ad16084eccf26464a84c5ee2f8b96b4daff9a3154ac3c1b320346aed042abe57";
        assert!(sighash.0.to_vec() == hex::decode(expected).unwrap());
    }

    #[test]
    fn op_codeseparator_test1() {
        let mut script_code: Vec<u8> = Vec::new();
        script_code.extend_from_slice(&[OP_CODESEPARATOR, OP_DUP, OP_HASH160]);
        let decoded = hex::decode("e252b946e62e0802cfc1db8242cc842d53e2fe25").unwrap();
        script_code.extend_from_slice(&decoded);
        script_code.extend_from_slice(&[OP_EQUALVERIFY, OP_CHECKSIG]);

        // Drop leading OP_CODESEPARATOR
        let expected_subscript = script_code[1..].to_vec();

        let actual_subscript = extract_subscript(&script_code, 0).unwrap();
        assert_eq!(actual_subscript, expected_subscript);
    }

    #[test]
    fn op_codeseparator_test2() {
        let mut script_code: Vec<u8> = Vec::new();
        script_code.extend_from_slice(&[OP_DUP, OP_HASH160]);
        let decoded = hex::decode("e252b946e62e0802cfc1db8242cc842d53e2fe25").unwrap();
        script_code.extend_from_slice(&decoded);
        script_code.extend_from_slice(&[OP_EQUALVERIFY, OP_CHECKSIG]);

        // No change
        let actual_subscript = extract_subscript(&script_code, 0).unwrap();
        assert_eq!(actual_subscript, script_code);
    }

    #[test]
    fn op_codeseparator_test3() {
        let mut script_code: Vec<u8> = Vec::new();
        script_code.extend_from_slice(&[
            OP_CODESEPARATOR,
            OP_1,
            OP_DROP,
            OP_CODESEPARATOR,
            OP_DUP,
            OP_HASH160,
        ]);
        let decoded: Vec<u8> = hex::decode("e252b946e62e0802cfc1db8242cc842d53e2fe25").unwrap();
        script_code.extend_from_slice(&decoded);
        script_code.extend_from_slice(&[OP_EQUALVERIFY, OP_CHECKSIG]);

        // Latest OP_CODESEPARATOR is the one that matters
        // Drop leading OP_CODESEPARATOR, OP_1, OP_DROP , OP_CODESEPARATOR
        let expected_subscript = script_code[4..].to_vec();

        // assert_eq!(extract_subscript(&script_code), expected_subscript);
        let actual_subscript = extract_subscript(&script_code, 0).unwrap();
        assert_eq!(actual_subscript, expected_subscript);
    }

    #[test]
    fn op_codeseparator_test4() {
        let mut script_code: Vec<u8> = Vec::new();
        script_code.extend_from_slice(&[OP_CODESEPARATOR, OP_1, OP_DROP, OP_DUP, OP_HASH160]);
        let decoded: Vec<u8> = hex::decode("e252b946e62e0802cfc1db8242cc842d53e2fe25").unwrap();
        script_code.extend_from_slice(&decoded);
        script_code.extend_from_slice(&[OP_EQUALVERIFY, OP_CHECKSIG, OP_VERIFY, OP_1]);

        // Drop the OP_CODESEPARATOR
        let expected_subscript = script_code[1..].to_vec();
        let actual_subscript = extract_subscript(&script_code, 0).unwrap();

        assert_eq!(actual_subscript, expected_subscript);
    }

    #[test]

    fn op_codeseparator_test5_1() {
        let mut script_code: Vec<u8> = Vec::new();
        script_code.extend_from_slice(&[
            OP_CODESEPARATOR, // deleted
            OP_2DUP,
            OP_1,
            OP_DROP,
            OP_CODESEPARATOR, // deleted
            OP_DUP,
            OP_HASH160,
        ]);
        let decoded: Vec<u8> = hex::decode("e252b946e62e0802cfc1db8242cc842d53e2fe25").unwrap();
        script_code.extend_from_slice(&decoded);
        script_code.extend_from_slice(&[
            OP_EQUALVERIFY,
            OP_CHECKSIG,
            OP_VERIFY,
            OP_CODESEPARATOR, //Extra
            OP_DUP,
            OP_HASH160,
        ]);
        script_code.extend_from_slice(&decoded);
        script_code.extend_from_slice(&[OP_EQUALVERIFY, OP_CHECKSIG]);

        let mut expected_subscript_one = Vec::new();
        expected_subscript_one.extend_from_slice(&[OP_DUP, OP_HASH160]);
        expected_subscript_one.extend_from_slice(&decoded);
        expected_subscript_one.extend_from_slice(&[
            OP_EQUALVERIFY,
            OP_CHECKSIG,
            OP_VERIFY,
            OP_CODESEPARATOR, // Should be Kept as per note 2 below
            OP_DUP,
            OP_HASH160,
        ]);
        expected_subscript_one.extend_from_slice(&decoded);
        expected_subscript_one.extend_from_slice(&[OP_EQUALVERIFY, OP_CHECKSIG]);

        /*
        1) Deleting its calling OP_CODESEPARATOR and any preceding parts of the script from the script
        2) Any OP_CODESEPARATOR opcodes that appear later in script, than the most recently executed code separator, will be included in the script
        https://bitcoinops.org/en/topics/op_codeseparator/
        */

        let actual_subscript = extract_subscript(&script_code, 0).unwrap();
        assert_eq!(actual_subscript, expected_subscript_one);
    }

    #[test]
    fn op_codeseparator_test5_2() {
        let mut script_code: Vec<u8> = Vec::new();
        script_code.extend_from_slice(&[
            OP_CODESEPARATOR,
            OP_2DUP,
            OP_1,
            OP_DROP,
            OP_CODESEPARATOR,
            OP_DUP,
            OP_HASH160,
        ]);
        let decoded: Vec<u8> = hex::decode("e252b946e62e0802cfc1db8242cc842d53e2fe25").unwrap();
        script_code.extend_from_slice(&decoded);
        script_code.extend_from_slice(&[
            OP_EQUALVERIFY,
            OP_CHECKSIG,
            OP_VERIFY,
            OP_CODESEPARATOR, //Extra
            OP_DUP,
            OP_HASH160,
        ]);
        script_code.extend_from_slice(&decoded);
        script_code.extend_from_slice(&[OP_EQUALVERIFY, OP_CHECKSIG]);

        let mut expected_subscript_two = Vec::new();
        expected_subscript_two.extend_from_slice(&[OP_DUP, OP_HASH160]);
        expected_subscript_two.extend_from_slice(&decoded);
        expected_subscript_two.extend_from_slice(&[OP_EQUALVERIFY, OP_CHECKSIG]);

        let actual_subscript = extract_subscript(&script_code, 1).unwrap();
        assert_eq!(actual_subscript, expected_subscript_two);
    }
}
