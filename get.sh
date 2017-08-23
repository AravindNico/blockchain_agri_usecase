#!/bin/bash  
# To get the Port number , username and password
echo " "
echo "---------Portnumber------------"
port=sudo grep rpc ~/.multichain/chain1/params.dat
echo " "
echo "---------Username--------------"
username=sudo grep rpcuser ~/.multichain/chain1/multichain.conf
echo " "
echo "---------Password--------------"
password=sudo grep rpcpassword ~/.multichain/chain1/multichain.conf

