#!/bin/sh

ETH='https://rpc.ankr.com/eth/'
BSC='https://rpc.ankr.com/bsc/'
Fantom='https://rpc.ankr.com/fantom/'

if [ $1 = "Wdoge" ] 
then 
   forge test --match-contract $1 --fork-url $BSC --fork-block-number 17248705 $2 $3

elif [ $1 = "ValueDeFi" ]
then
   forge test --match-contract $1 --fork-url $ETH --fork-block-number 11256672 $2 $3

elif [ $1 = "OneRing" ]
then  
   forge test --match-contract $1 --fork-url $Fantom --fork-block-number 34041497 $2 $3

elif [ $1 = "Novo" ]
then 
   forge test --match-contract $1 --fork-url $BSC --fork-block-number 18225001 $2 $3

elif [ $1 = "ApeRocket" ]
then
   forge test --match-contract $1 --fork-url $BSC --fork-block-number 9139707 $2 $3

elif [ $1 = "ElevenFi" ]
then
   forge test --match-contract $1 --fork-url $BSC --fork-block-number 8534789 $2 $3

elif [ $1 = "Harvest_USDT" ]
then 
   forge test --match-contract $1 --fork-url $ETH --fork-block-number  $2 $3  

elif [ $1 = "Harvest_USDC" ]
then 
   forge test --match-contract $1 --fork-url $ETH --fork-block-number 11129499 $2 $3

elif [ $1 = "Eminence" ]
then 
   forge test --match-contract $1 --fork-url $ETH --fork-block-number 10954410 $2 $3

elif [ $1 = "bEarnFi" ]
then 
   forge test --match-contract $1 --fork-url $BSC --fork-block-number 7457124 $2 $3

elif [ $1 = "bZx1" ]
then 
   forge test --match-contract attackTester --fork-url $ETH --fork-block-number 9484680 $2 $3

elif [ $1 = "warp" ]
then
   forge test --match-contract $1 --fork-url $ETH --fork-block-number 11473329 $2 $3

elif [ $1 = "harvest_usdt" ]
then
   forge test --match-contract $1 --fork-url $ETH --fork-block-number 11129499 $2 $3
elif [ $1 = "harvest_usdc" ]
then
   forge test --match-contract $1 --fork-url $ETH --fork-block-number 11129473 $2 $3
elif [ $1 = "fantom" ]
then
   echo "fantom"
else
   echo "None of the condition met"
fi