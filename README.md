# Overview
A Safe (known as a Gnosis Safe) is a smart contract that acts as a wallet. Safe's offer far better security and functionality compared to legacy EOA blockchain wallets. The problem is, it's extremely hard to get basic transaction information from the on-chain events such as signers, tokens, amounts and modules.

The `./decoder.py` file enables you to input a message hash and decode the signers of a Safe transaction by decoding the ECDSA signature to tell you the exact wallets responsible for the Safe's transaction. 

For more details on how this decoder works, I suggest reading how Gnosis Safe encodes the transaction details into a ECDSA signature [here](https://docs.safe.global/smart-account-signatures). 
