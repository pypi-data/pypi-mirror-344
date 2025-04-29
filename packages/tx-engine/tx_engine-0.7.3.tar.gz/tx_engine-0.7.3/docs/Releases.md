# Releases
* v0.3.3 - Add p2pkh_script, hash160, address_to_public_key_hash
* v0.3.4 - Add public_key_to_address
* v0.3.5 - script.get_commands() - returns bytes
* v0.3.6 - wallet.sign_tx() - test
* v0.3.7 - Tx vin hash is now String
* v0.3.7 - Version bump
* v0.3.8 - Version bump
* v0.3.9 - John's updates add_tx_in, add_tx_out, signing
* v0.4.0 - Added Eq and __repr__ to Tx, TxIn, TxOut and Script and Tx validate
* v0.4.1 - Added Script append_byte, append_data, append_pushdata
* v0.4.2 - Changed to MIT License
* v0.4.3 - Changed to MIT License v2
* v0.4.4 - Signing fix
* v0.4.5 - Script index and is_p2pkh added
* v0.4.5 - Remove dependency on secp256k1 library (which cc-ed OpenSSL)
* v0.4.6 - Bump version due to mistake in tagging v0.4.5
* v0.4.7 - Fix number parsing in Script.parse_string()
* v0.4.8 - Further number parsing in Script.parse_string()
* v0.4.9 - Fix OP_SUB
* v0.5.0 - Forgot to update crate, Version bump
* v0.5.1 - Use Python encode_num
* v0.5.2 - Fix OP_MUL and OP_EQUAL
* v0.5.3 - Version bump, build failure
* v0.5.4 - OP_EQUALVERIFY, Python decode_num
* v0.5.5 - Interface, RPCInterface, verify script and flags, TxIn & TxOut - script in constructor
* v0.5.6 - Remove lengths in to_string, fixes for Python 3.10, Replace [] with "" for scripts in Tx
* v0.5.7 - Add Wallet.generate_keypair() and Python dependencies
* v0.5.8 - Resolve Python dependencies, fix pushdata in Script.to_string()
* v0.5.9 - Address OP_BIN2NUM issue
* v0.6.0 - Address OP_NUM2BIN issue
* v0.6.1 - Bump version as missed cargo.toml file
* v0.6.2 - Added sig_hash functions to support for exotic script development, fixed a problem with transaction checker when setting a 'z' value externally
* v0.6.3 - Added Tx.parse_hexstr - broken!
* v0.6.4 - Added Tx.parse_hexstr
* v0.6.5 - wif_to_bytes wallet function added TxIn to Output function added, minor version bump
* v0.6.6 - wif_to_bytes wallet function added TxIn to Output function added, minor version bump (forgot to bump the version in cargo.toml)
* v0.6.7 - additional wallet functions added to support WildBits
* v0.6.8 - Updates to the script interpreter to support a debugger, python interface to the rust stack implementation, Context updates to support a debugger
* v0.6.9 - Rust Wallet functionality - CI build failure
* v0.6.10 - Try again
* v0.6.11 - Try again
* v0.6.12 - Try again - now with CI changes
* v0.6.13 - Try again - now min Python version 3.11
* v0.6.14 - Try again - remove platforms that did not read env vars
* v0.6.15 - Try again - remove two more platforms that did not read env vars
* v0.7.0 - Bump version for Python 3.13 support
* v0.7.1 - Fixed OP_CODESEPARATOR
* v0.7.2 - Added OP_2MUL and OP_2DIV script operations
* v0.7.3 - Fixed WoC endpoints get_block_header and get_merkle_proof to use new TSC endpoint