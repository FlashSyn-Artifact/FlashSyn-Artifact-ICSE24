# Purpose:

## Badges:
We are applying for 
1. available 
2. reusable
   

## Justification
1. We have made our artifact available on GitHub and Zenodo.
2. We have provided both the dependencies for running our tools (via Docker) and documentation (in this repository).
3. We have set up the artifact to run our experiments and to produce results in an easily understandable and re-usable form.
4. We have included all of our original experimental raw data which could be checked by reviewers.


# Provenance: 
This artifact can be accessed via the following links:
    [Zenodo](https://zenodo.org/records/10458602) or 
    [Github](https://github.com/FlashSyn-Artifact/FlashSyn-Artifact-ICSE24)    


# Data: 
## Folder Structure
- `Benchmarks/` folder contains all the benchmarks used in the paper.   
- `paper/` folder contains the accepted paper including the links to the archival repository at the end of the abstract. Please focus on Table 3, Table 4, Table 5 in Evaluation Section, which will be reproduced by this artifact.
- `Results-Expected` folder contains the original data results of the experiments mentioned in the paper. 
    - To get Table 3 part 1 -- all except last column (for RQ1), run `RQ1.py`. Its raw data is stored in `FlashSynData/2000+X/` folder.
    - To get Table 3 part 2 -- last column (for RQ2), run `RQ2.py`. Its raw data is stored in `FlashSynData/precise/` folder.
    - To get Table 4 (for RQ3), we need to run 3 files separately. Its raw data is stored in `FlashSynData/` folder.
        - Run `RQ3_Time.py` to get the `Avg.Time (s)` row. 
        - Run `RQ3_Datapoints.py` to get the  `Avg. Data Points` row. 
        - Run `RQ3_NormProfit+Solved.py` to get the `Avg. Normalized Profit` and `# Benchmarks Solved` row. 
    - To get Table 5 (for RQ4), run `RQ4.py`. Its raw data is stored in `FlashFind+FlashSynData/` folder. Note this script will only generate the left part of the Table 5, the right part of Table 5 is exactly the same data as shown in `FlashSyn-poly` columns of Table 3. 

- `Results-To-Reproduce` folder is a folder reserved for the results generated by the artifact. It also contains several Python scripts similar to the ones in `Results-Expected` folder to extract tables from the raw data.


## Validate the results reproduced by the artifact
Reviewers can either compare the results generated by the artifact(introduced later) with the results in `Results-Expected` folder or the results in the paper. 

- Link to the paper: https://github.com/FlashSyn-Artifact/FlashSyn-Artifact-ICSE24/blob/main/paper/FlashSynICSE24.pdf



# Setup (for executable artifacts): 

## Disk Usage:
The docker image takes approximately 6 GB. 

## Hardware: 
The executable should be able to run on common Ubuntu laptops or desktops. However, running the artifact on a laptop could lead to failures of 1-2 benchmarks because solving these benchmarks requires expensive computational resources. We found our artifact does not work on a Macbook ARM or Windows.  

Our original experiment is conducted on an Ubuntu 22.04 server, with an AMD Ryzen Threadripper 2990WX 32-Core Processor and 128 GB RAM. 

We recommend reviewers to run the artifact on a server with an Ubuntu AMD desktop with at least 16 GB RAM and 4 processors. 


## Software: 
To use this artifact, the following dependencies are required:
- A working installation of [Docker](https://docs.docker.com/get-docker/)
- Bash
- Ubuntu 


# Usage (for executable artifacts): 

## Installation:
This artifact requires users install docker first. 

To install Docker please see one of the following resources
1. [Install Docker for Ubuntu.](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

After installing Docker, please run the following command to pull the docker image from Docker Hub:
```
sudo docker pull zhiychen597/flashsyn:latest
```

(NEW!) Create docker volumes to persist data generated by the artifact, in case of losing log files due to unexpected termination of the docker container. 
```
sudo docker volume create FlashSyn-Data-Reproduce
```




## (Optional) How to build the docker image from scratch:

please run the following command to build the docker image: 
```
sudo docker build -t flashsyn .
```


## Execution:
    
## A basic usage example to test the docker image setup:

Step 1: Start a temporary container using the Docker image.

(NEW!) Using a docker volume to persist the log files generated. 
```diff
- sudo docker run -it zhiychen597/flashsyn:latest bash
+ sudo docker run -it -v FlashSyn-Data-Reproduce:/FlashSyn/Results-To-Reproduce/ zhiychen597/flashsyn:latest bash
```


Step 2: (In the Docker Image )Check whether Foundry is installed correctly.
```
. ~/.bashrc
forge -V
```
The `forge` command should print the following message:
`forge 0.2.0 (...)`



Step 3: (In the Docker Image) run the following command in the container to test the setup.
```

chmod +x ./runTest.sh  && ./runTest.sh
```
The `./runTest.sh` will run a precise baseline version of FlashSyn on a simple benchmark `bEarnFi`. If everything is setup correctly, this command should generate a log data file at `Results-To-Reproduce/FlashSynData/precise/bEarnFi_precise.txt`. Please refer to [HOW-TO-READ-DATA-LOG.md](./HOW-TO-READ-DATA-LOG.md) for more details about how to completely understand the log file. 

Print the file to screen using the following command:
```
cat Results-To-Reproduce/FlashSynData/precise/bEarnFi_precise.txt
```
If the last line of the output is " =================== Best Profit  XXX  ============================" where XXX is a positive number close to 13832, the setup can be confirmed correct. 



## Detailed commands to replicate the major results from the paper:

**Note 1**: 
    The results reproduced may not be exactly the same as the results in the paper. Our implementation uses a shgo solver to solve the optimization problem, which will adopt different search strategies based on hardware resources. 
    Within the context of this paper, the most important thing is whether there exists an attack vector with positive profit(the last line of a log data file unless timeout), which represents the existence of a flash loan attack. The exact value of the profit is not that important. It is normal to synthesize attack vectors with slightly different profits within different runs. 

**Note 2**:
    In the original experiment described in the paper, FlashSyn uses up to 18 processes. Since we are not sure if reviewers have enough computational resources, we limit the number of processes to 1 in this artifact. This may lead to a slightly worse performance of FlashSyn. 

**Note 3**:
    The docker image was built on an Ubuntu ADM Desktop and was tested on another Ubuntu AMD Desktop. We are not sure if it will work on other operating systems.



Our experiment is divided into 4 parts. Each part corresponds to one research question (RQ). The following commands will run the experiments for each RQ and generate the results in `Results-To-Reproduce` folder. 

RQ1 tests the effectiveness of FlashSyn with 2000 initial data points with counterexample driven loops, which empirically represents the best setting for FlashSyn to perform the best, which takes approximately 18 hours to finish. 

RQ2 tests the effectiveness of a precise baseline, which takes about 4 hours to finish. 

RQ3 tests FlashSyn under 8 different settings. It means replicating RQ1 8 times with different settings, which takes approximately a week to finish. 

RQ4 tests the effectiveness of FlashSyn with additional actions discovered by FlashFind, which takes about 4 hours to finish.


-------------------------------------
Step 1: Start a temporary container using the Docker image.

(NEW!) Using a docker volume to persist the log files generated.
```diff
- sudo docker run -it flashsyn bash
+ sudo docker run -it -v FlashSyn-Data-Reproduce:/FlashSyn/Results-To-Reproduce/ zhiychen597/flashsyn:latest bash
```


### RQ1 (Takes approximately 18 hours)
The `runRQ1.sh` script runs FlashSyn-poly and FlashSyn-inter with 2000 initial data points and counterexample driven loops on 16 benchmarks. It takes several minutes to up to 2 hours to finish each benchmark depending on the difficulty of the benchmark. Our `./runRQ1.sh` script will run FlashSyn-poly and FlashSyn-inter with the best setting for overall 16 benchmark (which means FlashSyn is executed 32 times).

Step 2: Run the following command in the container to run experiment for RQ1. (Takes approximately 18 hours)
```
. ~/.bashrc
chmod +x ./runRQ1.sh  && ./runRQ1.sh
```

Step 3: Run the following command to extract data from data files and generate Table 3 (Part 1).
```
python3 Results-To-Reproduce/RQ1.py
```

----------
It is possible to run each benchmark separately. 

```
./runRQ1.sh XXX
```

where XXX could be `bZx1`/`bEarnFi`/`Eminence`/`Warp`/`Puppet`/`PuppetV2`/`ElevenFi`/`OneRing`/`Novo`/`Wdoge` (Running time is about 30 minutes), `Harvest_USDC`/`Harvest_USDT`/`ValueDeFi`/`ApeRocket` (Running time is about 2 hour), `CheeseBank`/`AutoShark` (Running time is about 4 hours)



### RQ2 (Takes approximately 3 hours)
The `runRQ2.sh` script runs a precise baseline version of FlashSyn on 7 benchmarks which we were able to extract their precise mathematical formula (which means FlashSyn is executed 7 times).

Step 2: Run the following command in the container to run experiment for RQ2. (Takes approximately 4 hours)
```
. ~/.bashrc
chmod +x ./runRQ2.sh  && ./runRQ2.sh
```

Step 3: Run the following command to extract data from data files and generate Table 3 (Part 2).
```
python3 Results-To-Reproduce/RQ2.py
```


----------
It is possible to run each benchmark separately. 

```
./runRQ2.sh XXX
```

where XXX could be `bEarnFi`/`Puppet`/`PuppetV2` (Running time is about 15 minutes), `Eminence`/`Wdoge` (Running time is about 1 hour), `CheeseBank`/`Warp` (Running time is about 2 hours)





### RQ4 (Takes approximately 4 hours)
The `runRQ4.sh` script runs FlashSyn-poly with actions identified by FlashFind with 2000 initial data points and with counterexample driven loops on overall 11 benchmarks. (which means FlashSyn is executed 11 times).

Step 2: Run the following command in the container to run experiment for RQ4. (Takes approximately 4 hours)
```
. ~/.bashrc
chmod +x ./runRQ4.sh  && ./runRQ4.sh
```

Step 3: Run the following command to extract data from data files and generate left part of Table 5.
```
python3 Results-To-Reproduce/RQ4.py
```

**Note:** 
This script will only generate the left part of the Table 5, the right part of Table 5 is exactly the same data as shown in `FlashSyn-poly` columns of Table 3.


----------
It is possible to run each benchmark separately. 

```
./runRQ4.sh XXX
```

where XXX could be `bZx1`/`bEarnFi`/`Novo`/`Wdoge` (Running time is about 15 minutes), `OneRing`/`Eminence` (Running time is about 30 minutes), `Harvest_USDT`/`Harvest_USDC`/`ValueDeFi`/`Warp`/`ApeRocket` (Running time is about <=2 hours)




### RQ3 (Takes approximately 5 days)
The `runRQ3.sh` script runs FlashSyn-poly and FlashSyn-inter with 200/500/1000/2000 initial data points and with/without counterexample driven loops on overall 16 benchmarks, (which means FlashSyn is executed 2 * 2 * 4 * 16 = 256 times). That's why this experiment takes a long time to finish.

Step 2: Run the following command in the container to run experiment for RQ3. (Takes approximately 1 week)
```
. ~/.bashrc
chmod +x ./runRQ3.sh  && ./runRQ3.sh
```

Step 3: Run the following command to extract data from data files and generate Table 3 (Part 2).
```
python3 Results-To-Reproduce/RQ3_Time.py                  # to get the `Avg.Time (s)` row. 
python3 Results-To-Reproduce/RQ3_Datapoints.py            # to get the `Avg. Data Points` row.
python3 Results-To-Reproduce/RQ3_NormProfit+Solved.py     # to get the `Ag. Normalized Profit` and `# Benchmarks Solved` row.
```

----------
It is possible to run each benchmark separately. 

```
./runRQ3.sh XXX
```

where XXX could be `bZx1`/`bEarnFi`/`Eminence`/`Warp`/`Puppet`/`PuppetV2`/`ElevenFi`/`OneRing`/`Novo`/`Wdoge` (Running time is about 4 hours), `Harvest_USDC`/`Harvest_USDT`/`ValueDeFi`/`ApeRocket` (Running time is about 12 hours), `CheeseBank`/`AutoShark` (Running time is about 24 hours)







## AWS Execution Results. 

To facilitate the review process, we have also provided an AWS EC2 instance. Reviewers can access the instance via the password provided in the review response.


After connecting to our AWS instance, execute the following command to start the docker container.
```
sudo docker run -it -v FlashSyn-Data-Reproduce:/FlashSyn/Results-To-Reproduce/ zhiychen597/flashsyn:latest bash
```

### RQ2: (here we use RQ2 as an example because it finishes quickly, RQ1 and RQ4 will be added soon later)

(NEW!) Clear the experiment results from the previous run. 
```
rm Results-To-Reproduce/FlashSynData/precise/*
```


Execute the following command to run the experiment for RQ2. 
```
./runRQ2.sh
```


Execute the following command to read the RQ2 results. 
```
python3 Results-To-Reproduce/RQ2.py
```

The following is a screenshot of our successful execution of RQ2 on AWS. 

![RQ2](./screenshots/RQ2.png)



### RQ1: (to be added soon)



### RQ4: (to be added soon)

