use crate::util::ChainGangError;
use num_bigint::{BigInt, Sign};
use num_traits::Zero;

// Type to simplify the types..
pub type Stack = Vec<Vec<u8>>;

/// Pops a bool off the stack
#[inline]
pub fn pop_bool(stack: &mut Stack) -> Result<bool, ChainGangError> {
    if stack.is_empty() {
        let msg = "Cannot pop bool, empty stack".to_string();
        return Err(ChainGangError::ScriptError(msg));
    }
    let top = stack.pop().unwrap();
    // Bools cannot be popped having more than 32-bits, but may be used in other ways
    if top.len() > 4 {
        let msg = format!("Cannot pop bool, len too long {}", top.len());
        return Err(ChainGangError::ScriptError(msg));
    }
    Ok(decode_bool(&top))
}

/// Pops a pre-genesis number off the stack
#[inline]
pub fn pop_num(stack: &mut Stack) -> Result<i32, ChainGangError> {
    if stack.is_empty() {
        let msg = "Cannot pop num, empty stack".to_string();
        return Err(ChainGangError::ScriptError(msg));
    }
    let top = stack.pop().unwrap();
    // Numbers cannot be popped having more than 4 bytes, but may overflow on the stack to 5 bytes
    // after certain operations and may be used as byte vectors.
    if top.len() > 4 {
        let msg = format!("Cannot pop num, len too long {}", top.len());
        return Err(ChainGangError::ScriptError(msg));
    }
    Ok(decode_num(&top)? as i32)
}

/// Pops a bigint number off the stack
#[inline]
pub fn pop_bigint(stack: &mut Stack) -> Result<BigInt, ChainGangError> {
    if stack.is_empty() {
        let msg = "Cannot pop bigint, empty stack".to_string();
        return Err(ChainGangError::ScriptError(msg));
    }
    let mut top = stack.pop().unwrap();
    Ok(decode_bigint(&mut top))
}

/// Converts a stack item to a bool
#[inline]
pub fn decode_bool(s: &[u8]) -> bool {
    if s.is_empty() {
        return false;
    }
    for item in s.iter().take(s.len() - 1) {
        if *item != 0 {
            return true;
        }
    }
    s[s.len() - 1] & 127 != 0
}

/// Converts a stack item to a number
#[inline]
pub fn decode_num(s: &[u8]) -> Result<i64, ChainGangError> {
    let mut val = match s.len() {
        0 => return Ok(0),
        1 => (s[0] & 127) as i64,
        2 => (((s[1] & 127) as i64) << 8) + (s[0] as i64),
        3 => (((s[2] & 127) as i64) << 16) + ((s[1] as i64) << 8) + (s[0] as i64),
        4 => {
            (((s[3] & 127) as i64) << 24)
                + ((s[2] as i64) << 16)
                + ((s[1] as i64) << 8)
                + (s[0] as i64)
        }
        _ => {
            for item in s.iter().take(s.len() - 1).skip(4) {
                if *item != 0 {
                    return Err(ChainGangError::ScriptError("Number too big".to_string()));
                }
            }
            if s[s.len() - 1] & 127 != 0 {
                return Err(ChainGangError::ScriptError("Number too big".to_string()));
            }
            ((s[3] as i64) << 24) + ((s[2] as i64) << 16) + ((s[1] as i64) << 8) + (s[0] as i64)
        }
    };
    if s[s.len() - 1] & 128 != 0 {
        val = 0 - val;
    }
    Ok(val)
}

/// Converts a number to a 32-bit stack item
#[inline]
pub fn encode_num(val: i64) -> Result<Vec<u8>, ChainGangError> {
    if !(-2147483647..=2147483647).contains(&val) {
        return Err(ChainGangError::ScriptError("Number out of range".to_string()));
    }
    let (posval, negmask) = if val < 0 { (-val, 128) } else { (val, 0) };
    if posval == 0 {
        Ok(vec![])
    } else if posval < 128 {
        Ok(vec![(posval as u8) | negmask])
    } else if posval < 32768 {
        Ok(vec![posval as u8, ((posval >> 8) as u8) | negmask])
    } else if posval < 8388608 {
        Ok(vec![
            (posval) as u8,
            (posval >> 8) as u8,
            ((posval >> 16) as u8) | negmask,
        ])
    } else {
        Ok(vec![
            (posval) as u8,
            (posval >> 8) as u8,
            (posval >> 16) as u8,
            ((posval >> 24) as u8) | negmask,
        ])
    }
}

/// Converts a stack item to a big int number
#[inline]
pub fn decode_bigint(s: &mut [u8]) -> BigInt {
    let len = s.len();
    if s.is_empty() {
        return BigInt::zero();
    }
    let mut sign = Sign::Plus;
    if s[len - 1] & 0x80 == 0x80 {
        sign = Sign::Minus;
    }
    s[len - 1] &= !0x80;
    BigInt::from_bytes_le(sign, s)
}

/// Converts a big int number to a stack item
#[inline]
pub fn encode_bigint(val: BigInt) -> Vec<u8> {
    let mut result = val.to_bytes_le();
    if result.1[result.1.len() - 1] & 0x80 == 0x80 {
        result.1.push(match result.0 {
            Sign::Plus | Sign::NoSign => 0x00,
            Sign::Minus => 0x80,
        });
    } else if result.0 == Sign::Minus {
        let len = result.1.len();
        result.1[len - 1] |= 0x80;
    }
    if result.1.len() == 1 && result.1[0] == 0 {
        return vec![];
    }
    result.1
}

#[inline]
pub fn decode_number_combined(s: &[u8]) -> Result<BigInt, ChainGangError> {
    let len = s.len();

    if len == 0 {
        println!("Zero length number");
        return Ok(BigInt::zero());
    }

    // Handle small integers (up to 4 bytes)
    if len <= 4 {
        let mut val = match len {
            1 => (s[0] & 127) as i64,
            2 => (((s[1] & 127) as i64) << 8) + (s[0] as i64),
            3 => (((s[2] & 127) as i64) << 16) + ((s[1] as i64) << 8) + (s[0] as i64),
            4 => {
                (((s[3] & 127) as i64) << 24)
                    + ((s[2] as i64) << 16)
                    + ((s[1] as i64) << 8)
                    + (s[0] as i64)
            }
            _ => unreachable!(), // We already checked len
        };

        if s[len - 1] & 128 != 0 {
            val = -val;
        }
        println!("Returing this way");
        return Ok(BigInt::from(val));
    }

    // Handle big integers (more than 4 bytes)
    let mut sign = Sign::Plus;
    if s[len - 1] & 0x80 == 0x80 {
        sign = Sign::Minus;
    }
    let mut big_int_bytes = s.to_vec();
    big_int_bytes[len - 1] &= !0x80; // Clear the sign bit
    println!("Returned this big num way");
    Ok(BigInt::from_bytes_le(sign, &big_int_bytes))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn decode_bool_tests() {
        assert!(decode_bool(&[1]) == true);
        assert!(decode_bool(&[255, 0, 0, 0]) == true);
        assert!(decode_bool(&[0, 0, 0, 129]) == true);
        assert!(decode_bool(&[0]) == false);
        assert!(decode_bool(&[0, 0, 0, 0]) == false);
        assert!(decode_bool(&[0, 0, 0, 128]) == false);
        assert!(decode_bool(&[]) == false);
    }

    #[test]
    fn pop_bool_tests() {
        assert!(pop_bool(&mut vec![vec![1]]).unwrap() == true);
        assert!(pop_bool(&mut vec![vec![0, 0, 0, 127]]).unwrap() == true);
        assert!(pop_bool(&mut vec![vec![0, 0, 0, 127]]).unwrap() == true);
        assert!(pop_bool(&mut vec![]).is_err());
        assert!(pop_bool(&mut vec![vec![0, 0, 0, 0, 0]]).is_err());
        assert!(pop_bool(&mut vec![vec![]]).unwrap() == false);
        assert!(pop_bool(&mut vec![vec![0]]).unwrap() == false);
        assert!(pop_bool(&mut vec![vec![0, 0, 0, 0]]).unwrap() == false);
        assert!(pop_bool(&mut vec![vec![0, 0, 0, 128]]).unwrap() == false);
    }

    #[test]
    fn encode_decode_num_tests() {
        // Range checks
        assert!(encode_num(2147483647).is_ok());
        assert!(encode_num(-2147483647).is_ok());
        assert!(encode_num(2147483648).is_err());
        assert!(encode_num(-2147483648).is_err());
        // Encode decode
        assert!(decode_num(&encode_num(0).unwrap()).unwrap() == 0);
        assert!(decode_num(&encode_num(1).unwrap()).unwrap() == 1);
        assert!(decode_num(&encode_num(-1).unwrap()).unwrap() == -1);
        assert!(decode_num(&encode_num(1111).unwrap()).unwrap() == 1111);
        assert!(decode_num(&encode_num(-1111).unwrap()).unwrap() == -1111);
        assert!(decode_num(&encode_num(111111).unwrap()).unwrap() == 111111);
        assert!(decode_num(&encode_num(-111111).unwrap()).unwrap() == -111111);
        assert!(decode_num(&encode_num(2147483647).unwrap()).unwrap() == 2147483647);
        assert!(decode_num(&encode_num(-2147483647).unwrap()).unwrap() == -2147483647);
    }

    #[test]
    fn pop_num_tests() {
        assert!(pop_num(&mut vec![vec![]]).unwrap() == 0);
        assert!(pop_num(&mut vec![vec![1]]).unwrap() == 1);
        assert!(pop_num(&mut vec![vec![129]]).unwrap() == -1);
        assert!(pop_num(&mut vec![vec![0, 0, 0, 0]]).unwrap() == 0);
        assert!(pop_num(&mut vec![vec![0, 0, 0, 0, 0]]).is_err());
    }

    #[test]
    fn encode_decode_num_bigint_tests() {
        // Range checks
        assert!(encode_num(2147483647).is_ok());
        assert!(encode_num(-2147483647).is_ok());
        assert!(encode_num(2147483648).is_err());
        assert!(encode_num(-2147483648).is_err());
        // Encode decode
        assert!(decode_number_combined(&encode_num(0).unwrap()).unwrap() == BigInt::from(0));

        assert!(decode_number_combined(&encode_num(1).unwrap()).unwrap() == BigInt::from(1));

        assert!(decode_number_combined(&encode_num(-1).unwrap()).unwrap() == BigInt::from(-1));

        assert!(decode_number_combined(&encode_num(1111).unwrap()).unwrap() == BigInt::from(1111));
        assert!(
            decode_number_combined(&encode_num(-1111).unwrap()).unwrap() == BigInt::from(-1111)
        );
        assert!(
            decode_number_combined(&encode_num(111111).unwrap()).unwrap() == BigInt::from(111111)
        );
        assert!(
            decode_number_combined(&encode_num(-111111).unwrap()).unwrap() == BigInt::from(-111111)
        );
        assert!(
            decode_number_combined(&encode_num(2147483647).unwrap()).unwrap()
                == BigInt::from(2147483647)
        );
        assert!(
            decode_number_combined(&encode_num(-2147483647).unwrap()).unwrap()
                == BigInt::from(-2147483647)
        );

        assert!(
            decode_number_combined(&encode_bigint(BigInt::from(0))).unwrap() == BigInt::from(0)
        );
    }
}
