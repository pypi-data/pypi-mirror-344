use async_trait::async_trait;

use async_mutex::Mutex;
use std::collections::HashMap;
use std::sync::Arc;

use crate::{
    interface::blockchain_interface::{Balance, BlockchainInterface, Utxo},
    messages::{BlockHeader, Tx},
    network::Network,
    util::ChainGangError,
};

/// TestData - is the data used to set up a a test fixture and can be used to capture broadcast transactions
#[derive(Debug, Default, Clone)]
pub struct TestData {
    utxo: HashMap<String, Utxo>,
    height: u32,
    broadcast: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct TestInterface {
    network_type: Network,
    /// TestData  is separated and enclosed in a Mutex to provide interior mutablity.
    test_data: Arc<Mutex<TestData>>,
}

impl Default for TestInterface {
    fn default() -> Self {
        Self::new()
    }
}

impl TestInterface {
    pub fn new() -> Self {
        TestInterface {
            network_type: Network::BCH_Testnet,
            test_data: Arc::new(Mutex::new(TestData::default())),
        }
    }

    pub async fn set_test_data(&mut self, test_data: &TestData) {
        // Check there is no broadcast data
        assert!(test_data.broadcast.is_empty());

        for (addr, utxo) in &test_data.utxo {
            self.set_utxo(addr, utxo).await;
        }
        self.set_height(test_data.height).await;
    }

    pub async fn set_utxo(&self, address: &str, utxo: &Utxo) {
        let mut test_data = self.test_data.lock().await;
        test_data.utxo.insert(address.to_string(), utxo.to_vec());
    }

    pub async fn set_height(&self, height: u32) {
        let mut test_data = self.test_data.lock().await;
        test_data.height = height;
    }
}

#[async_trait]
impl BlockchainInterface for TestInterface {
    fn set_network(&mut self, network: &Network) {
        self.network_type = *network;
    }

    // Return Ok(()) if connection is good
    async fn status(&self) -> Result<(), ChainGangError> {
        Ok(())
    }

    /// Get balance associated with address
    async fn get_balance(&self, address: &str) -> Result<Balance, ChainGangError> {
        debug!("get_balance");

        let utxo: Utxo = self.get_utxo(address).await?;
        let test_data = self.test_data.lock().await;

        let confirmation_height: i32 = (test_data.height - 6).try_into().unwrap();

        let confirmed: i64 = utxo
            .iter()
            .filter(|x| x.height >= 0 && x.height <= confirmation_height)
            .map(|x| x.value)
            .sum();

        let unconfirmed: i64 = utxo
            .iter()
            .filter(|x| x.height < 0 || x.height > confirmation_height)
            .map(|x| x.value)
            .sum();

        let balance = Balance {
            confirmed,
            unconfirmed,
        };
        Ok(balance)
    }

    /// Get UXTO associated with address
    async fn get_utxo(&self, address: &str) -> Result<Utxo, ChainGangError> {
        debug!("broadcast_tx");

        let test_data = self.test_data.lock().await;

        match test_data.utxo.get(address) {
            Some(value) => Ok(value.to_vec()),
            None => Ok(Vec::new()),
        }
    }

    /// Broadcast Tx
    async fn broadcast_tx(&self, tx: &Tx) -> Result<String, ChainGangError> {
        debug!("broadcast_tx");
        let mut test_data = self.test_data.lock().await;

        // Record tx
        test_data.broadcast.push(tx.as_hexstr());

        // Return hex
        let txid = tx.hash().encode();
        Ok(txid)
    }

    async fn get_tx(&self, _txid: &str) -> Result<Tx, ChainGangError> {
        debug!("get_tx");
        std::unimplemented!();
    }

    async fn get_latest_block_header(&self) -> Result<BlockHeader, ChainGangError> {
        debug!("get_latest_block_header");
        std::unimplemented!();
    }

    async fn get_block_headers(&self) -> Result<String, ChainGangError> {
        debug!("get_block_headers");
        std::unimplemented!();
    }
}
