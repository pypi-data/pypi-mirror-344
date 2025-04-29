use async_trait::async_trait;

use crate::{
    messages::{BlockHeader, Tx},
    network::Network,
    util::ChainGangError,
};
use serde::Deserialize;

//#[allow(unused_must_use)]

/// Balance returned from WoC
#[derive(Debug, Default, Deserialize, Clone, Copy)]
pub struct Balance {
    pub confirmed: i64,
    pub unconfirmed: i64,
}

/// Type to represent UTXO Entry
#[allow(dead_code)]
#[derive(Debug, Deserialize, Default, Clone, PartialEq, Eq)]
pub struct UtxoEntry {
    pub height: i32,
    pub tx_pos: u32,
    pub tx_hash: String,
    pub value: i64,
}
/// Type to represent UTXO set
pub type Utxo = Vec<UtxoEntry>;

/// Trait of the blockchain interface
///
#[async_trait]
pub trait BlockchainInterface: Send + Sync {
    fn set_network(&mut self, network: &Network);

    // Return Ok(()) if connection is good
    async fn status(&self) -> Result<(), ChainGangError>;

    /// Get balance associated with address
    async fn get_balance(&self, address: &str) -> Result<Balance, ChainGangError>;

    /// Get UXTO associated with address
    async fn get_utxo(&self, address: &str) -> Result<Utxo, ChainGangError>;

    /// Broadcast Tx, return the txid
    async fn broadcast_tx(&self, tx: &Tx) -> Result<String, ChainGangError>;

    async fn get_tx(&self, txid: &str) -> Result<Tx, ChainGangError>;

    async fn get_latest_block_header(&self) -> Result<BlockHeader, ChainGangError>;

    async fn get_block_headers(&self) -> Result<String, ChainGangError>;
}
