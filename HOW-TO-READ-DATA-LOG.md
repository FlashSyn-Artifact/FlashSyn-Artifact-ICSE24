
## How to read a log file?
Let's take `Results-Expected/FlashSynData/200+X/bEarnFi_inte.txt` as an example, since it's one of the shortest log files. 

It stores logs when `FlashSyn` ran over the bEarnFi benchmark with counterexample-driven loops and with 200 data points per action initially. 

The first several lines show the number of initial data points for each action. 
Starting from line 6, the file shows the results returned by the optimizer for each symbolic actions vector -- attack vector candidates. 

Starting from line 26, it shows the execution results(Actual Profit) for these attack vector candidates. And a summary of the best execution results is logged after that(line 217 -- line 223). The rest of results follows the similar pattern. An exception is that, starting from the second round(round 1), FlashSyn gradually arguments the data points based on counterexamples. For example, line 450 shows how many data points is added in this round. 

At the end of log file(line 1823 -- line 1824), the file summarizes all Symbolic Actions Vectors and the parameters that give us best positive profit, 

Note all the Harvest_USDT(resp., Harvest_USDC) log files in this folder are referring to Harvest_USDC(resp., Harvest_USDT) statistics listed in all Tables. 


