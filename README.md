# Overview
Gnosis Safe's are a blockchain account abstraction product that replaces EOA wallets with a smart contract. The problem is, when decoding the log events of a Safe's transactions you can't easily pull details such as signers. 

The `./decoder.py` file enables you to input a message hash and decode the signers of the transaction. Now, using this decoder, you can easily determine the addresses associated with creating a Safe, sending money from Safe, or adding smart contract functionality to the Safe. 

For more details on how this decoder works, I suggest reading how Gnosis Safe encodes the transaction details into a message hash [here](https://docs.safe.global/smart-account-signatures). 