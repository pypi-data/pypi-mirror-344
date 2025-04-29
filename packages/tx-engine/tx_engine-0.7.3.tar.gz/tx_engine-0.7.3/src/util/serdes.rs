use crate::util::ChainGangError;
use std::io;
use std::io::{Read, Write};

/// An object that may be serialized and deserialized
pub trait Serializable<T> {
    /// Reads the object from serialized form
    fn read(reader: &mut dyn Read) -> Result<T, ChainGangError>
    where
        Self: Sized;

    /// Writes the object to serialized form
    fn write(&self, writer: &mut dyn Write) -> io::Result<()>;
}

impl Serializable<[u8; 16]> for [u8; 16] {
    fn read(reader: &mut dyn Read) -> Result<[u8; 16], ChainGangError> {
        let mut d = [0; 16];
        reader.read_exact(&mut d)?;
        Ok(d)
    }

    fn write(&self, writer: &mut dyn Write) -> io::Result<()> {
        writer.write_all(self)?;
        Ok(())
    }
}

impl Serializable<[u8; 32]> for [u8; 32] {
    fn read(reader: &mut dyn Read) -> Result<[u8; 32], ChainGangError> {
        let mut d = [0; 32];
        reader.read_exact(&mut d)?;
        Ok(d)
    }

    fn write(&self, writer: &mut dyn Write) -> io::Result<()> {
        writer.write_all(self)?;
        Ok(())
    }
}
