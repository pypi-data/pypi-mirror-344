use async_trait::async_trait;
use reqwest::StatusCode;

use crate::util::Serializable;
use serde::Serialize;

use crate::{
    interface::blockchain_interface::{Balance, BlockchainInterface, Utxo},
    messages::{BlockHeader, Tx},
    network::Network,
    util::ChainGangError,
};

/// Structure for json serialisation for broadcast_tx
#[derive(Debug, Serialize)]
struct BroadcastTxType {
    pub txhex: String,
}

#[derive(Debug, Clone)]
pub struct WocInterface {
    network_type: Network,
}

impl Default for WocInterface {
    fn default() -> Self {
        Self::new()
    }
}

impl WocInterface {
    pub fn new() -> Self {
        WocInterface {
            network_type: Network::BSV_Testnet,
        }
    }

    /// Return the current network as a string
    fn get_network_str(&self) -> &'static str {
        match self.network_type {
            Network::BSV_Mainnet => "main",
            Network::BSV_Testnet => "test",
            Network::BSV_STN => "stn",
            _ => panic!("unknown network {}", &self.network_type),
        }
    }
}

#[async_trait]
impl BlockchainInterface for WocInterface {
    fn set_network(&mut self, network: &Network) {
        self.network_type = *network;
    }

    // Return Ok(()) if connection is good
    async fn status(&self) -> Result<(), ChainGangError> {
        log::debug!("status");

        let network = self.get_network_str();
        let url = format!("https://api.whatsonchain.com/v1/bsv/{network}/woc");
        let response = reqwest::get(&url).await?;
        if response.status() != 200 {
            log::warn!("url = {}", &url);
            return Err(ChainGangError::ResponseError(format!("response.status() = {}", response.status())));
        };
        match response.text().await {
            Ok(txt) if txt == "Whats On Chain" => Ok(()),
            Ok(txt) => Err(ChainGangError::ResponseError(format!("Unexpected txt = {}", txt))),
            Err(err) => Err(ChainGangError::ResponseError(format!("response.text() = {}", err))),
        }
    }

    /// Get balance associated with address
    async fn get_balance(&self, address: &str) -> Result<Balance, ChainGangError> {
        log::debug!("get_balance");

        let network = self.get_network_str();
        let url =
            format!("https://api.whatsonchain.com/v1/bsv/{network}/address/{address}/balance");
        let response = reqwest::get(&url).await?;
        if response.status() != 200 {
            warn!("url = {}", &url);
            return Err(ChainGangError::ResponseError(format!("response.status() = {}", response.status())));
        };
        let txt = match response.text().await {
            Ok(txt) => txt,
            Err(x) => {
                log::debug!("address = {}", &address);
                return Err(ChainGangError::ResponseError(format!("response.text() = {}", x)));
            }
        };
        let data: Balance = match serde_json::from_str(&txt) {
            Ok(data) => data,
            Err(x) => {
                log::debug!("address = {}", &address);
                log::warn!("txt = {}", &txt);
                return Err(ChainGangError::JSONParseError(format!("json parse error = {}", x)));
            }
        };
        Ok(data)
    }

    /// Get UXTO associated with address
    async fn get_utxo(&self, address: &str) -> Result<Utxo, ChainGangError> {
        log::debug!("get_utxo");
        let network = self.get_network_str();

        let url =
            format!("https://api.whatsonchain.com/v1/bsv/{network}/address/{address}/unspent");
        let response = reqwest::get(&url).await?;
        if response.status() != 200 {
            log::warn!("url = {}", &url);
            return Err(ChainGangError::ResponseError(format!("response.status() = {}", response.status())));
        };
        let txt = match response.text().await {
            Ok(txt) => txt,
            Err(x) => {
                return Err(ChainGangError::ResponseError(format!("response.text() = {}", x)));
            }
        };
        let data: Utxo = match serde_json::from_str(&txt) {
            Ok(data) => data,
            Err(x) => {
                log::warn!("txt = {}", &txt);
                return Err(ChainGangError::JSONParseError(format!("json parse error = {}", x)));
            }
        };
        Ok(data)
    }

    /// Broadcast Tx
    ///
    async fn broadcast_tx(&self, tx: &Tx) -> Result<String, ChainGangError> {
        log::debug!("broadcast_tx");
        let network = self.get_network_str();
        let url = format!("https://api.whatsonchain.com/v1/bsv/{network}/tx/raw");
        log::debug!("url = {}", &url);
        let data_for_broadcast = BroadcastTxType {
            txhex: tx.as_hexstr(),
        };
        //let data = serde_json::to_string(&data_for_broadcast).unwrap();
        let client = reqwest::Client::new();
        let response = client.post(&url).json(&data_for_broadcast).send().await?;
        let status = response.status();
        // Assume a response of 200 means broadcast tx success
        match status {
            StatusCode::OK => {
                let res = response.text().await?;
                let hash = res.trim();
                let txid = hash.trim_matches('"');
                Ok(txid.to_string())
            }
            _ => {
                log::debug!("url = {}", &url);
                Err(ChainGangError::ResponseError(format!("response.status() = {}", status)))
            }
        }
    }

    async fn get_tx(&self, txid: &str) -> Result<Tx, ChainGangError> {
        log::debug!("get_tx");

        let network = self.get_network_str();
        let url = format!("https://api.whatsonchain.com/v1/bsv/{network}/tx/{txid}/hex");
        let response = reqwest::get(&url).await?;
        if response.status() != 200 {
            log::warn!("url = {}", &url);
            return Err(ChainGangError::ResponseError(format!("response.status() = {}", response.status())));
        };
        match response.text().await {
            Ok(txt) => {
                let bytes = hex::decode(txt)?;
                let mut byte_slice = &bytes[..];
                let tx: Tx = Tx::read(&mut byte_slice)?;
                Ok(tx)
            }
            Err(x) => Err(ChainGangError::ResponseError(format!("response.text() = {}", x))),
        }
    }

    async fn get_latest_block_header(&self) -> Result<BlockHeader, ChainGangError> {
        log::debug!("get_latest_block_header");
        let network = self.get_network_str();
        let url =
            format!("https://api.whatsonchain.com/v1/bsv/{network}/block/headers/latest?count=1");
        let response = reqwest::get(&url).await?;
        if response.status() != 200 {
            log::warn!("url = {}", &url);
            return Err(ChainGangError::ResponseError(format!("response.status() = {}", response.status())));
        };
        match response.text().await {
            Ok(txt) => {
                let bytes = hex::decode(txt)?;
                let mut byte_slice = &bytes[..];
                let blockheader: BlockHeader = BlockHeader::read(&mut byte_slice)?;
                Ok(blockheader)
            }
            Err(x) => Err(ChainGangError::ResponseError(format!("response.text() = {}", x))),
        }
    }

    async fn get_block_headers(&self) -> Result<String, ChainGangError> {
        log::debug!("get_block_headers");
        let network = self.get_network_str();
        let url = format!("https://api.whatsonchain.com/v1/bsv/{network}/block/headers");
        let response = reqwest::get(&url).await?;
        if response.status() != 200 {
            log::warn!("url = {}", &url);
            return Err(ChainGangError::ResponseError(format!("response.status() = {}", response.status())));
        };
        match response.text().await {
            Ok(headers) => Ok(headers),
            Err(x) => Err(ChainGangError::ResponseError(format!("response.text() = {}", x))),
        }
    }
}
