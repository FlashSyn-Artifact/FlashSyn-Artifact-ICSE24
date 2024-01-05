## Folder Structure

Some supplemental materials(extension of our paper submission) are included in SuppMaterial.pdf

The benchmarks we used are listed under Benchmarks/ folder. Note \<X\>_swap.sol files are the script we used to verify repaying flash loans (see Supplementary material Section 5). 

The experimental data is put under Data/ folder. It contains two sub-folders.
- FlashSynData/ sub-folder contains all experimental data for running FlashSyn alone.
- FlashFind+FlashSynData/ sub-folder contains all experimental data for running FlashFind + FlashSyn combined. 

The source code of FlashSyn and FlashFind are put under src/ folder.


In FlashSynData/:

- All of our experimental data(a.k.a. logs) is stored under 10 folders - Data/200_noloop, Data/200+X, Data/500_noloop, Data/500+X, Data/1000_noloop, Data/1000+X, Data/2000_noloop, Data/2000+X, Data/precise, Data/FlashSyn+FlashFind

- Folders \<Y\>+X folders contain logs of FlashSyn when we ran FlashSyn over benchmarks with \<Y\> initial data points per action. The initial data points and the logs when collecting initial data points are stored in \<Y\>+X/data/\<benchmark\>_data.txt

- Folders \<Y\>_noloop contains logs of FlashSyn when we ran FlashSyn over benchmarks while counterexample-driven loops are disabled. 


In FlashFind+FlashSynData/:

- Folder initialData/ stores all the logs for collecting initial data. \<X\>_poly.txt stores log files for each benchmark. 




## How to get the results on the paper submission? 
Go to Data/FlashSynData/ folder.

- To get Table 3 part 1 (for RQ1), run RQ1.py. 

- To get Table 3 part 2 (for RQ2), run RQ2Precise.py

- To get Table 4 (for RQ3), we need to run 3 files separately.

  - Run RQ2RQ3_time.py to get the `Avg.Time (s)` row. 

  - Run RQ2RQ3_datapoints.py to get the  `Avg. Data Points` row. 

  - Run RQ3NormProfit.py to get the `Ag. Normalized Profit` and `# Benchmarks Solved` row. The data inside RQ3NormProfit.py can be got by running RQ3Profit.py


Go to Data/FlashFind+FlashSynData/ folder.

- To get Table 5 (for RQ4), we need to manually get the results from corresponding initial data file and synthesis log file. For example, use Novo_poly.txt and initialData/NovoIC.txt to calculate its total time spent. 


## How to get the results on the supplemental materials?
Go to Benchmarks/ folder, 

- To get Table 1, execute each \<X\>_swap.sol files in foundry. 


Go to Data/FlashSynData/ folder.

- To get Table 2, run RQ3Profit.py and then RQ3NormProfit.py.

- To get Table 3, run RQ3_time.py

- To get Table 4, run RQ2RQ3_initialCollect.py

- To get table 5, run RQ3_datapoints.py



## How to read a log file?
Let's take Data/FlashSynData/200+X/bEarnFi_inte.txt as an example, since it's one of the shortest log files. 

It stores logs when FlashSyn ran over the bEarnFi benchmark with counterexample-driven loops and with 200 data points per action initially. 

The first several lines show the number of initial data points for each action. 
Starting from line 6, the file shows the results returned by the optimizer for each symbolic actions vector -- attack vector candidates. 

Starting from line 26, it shows the execution results(Actual Profit) for these attack vector candidates. And a summary of the best execution results is logged after that(line 217 -- line 223). The rest of results follows the similar pattern. An exception is that, starting from the second round(round 1), FlashSyn gradually arguments the data points based on counterexamples. For example, line 450 shows how many data points is added in this round. 

At the end of log file(line 1823 -- line 1824), the file summarizes all Symbolic Actions Vectors and the parameters that give us best positive profit, 

Note all the Harvest_USDT(resp., Harvest_USDC) log files in this folder are referring to Harvest_USDC(resp., Harvest_USDT) statistics listed in all Tables. 



