#!/bin/bash

# Function to print current date and time
print_date_time() {
    echo "========= Current Date and Time: $(date) ========="
}


# Function to update and display counter
update_counter() {
    completed_benchmarks=$((completed_benchmarks + 1))
    remaining_benchmarks=$((total_benchmarks - completed_benchmarks))
    echo "Benchmarks: $completed_benchmarks/$total_benchmarks finished, $remaining_benchmarks/$total_benchmarks to do"
}



run_case() {
    local initialDatapoints=$1
    local case=$2
    print_date_time
    echo "running FlashSyn-inter with $initialDatapoints initial datapoints with counterexample driven loops for $case..."
    timeout 10800s python3.7 src/main.py $case 0 1 $initialDatapoints > ./$dir/${case}_inte.txt
    echo "$case done."
    update_counter

    print_date_time
    echo "running FlashSyn-poly with $initialDatapoints initial datapoints with counterexample driven loops for $case..."
    timeout 7200s python3.7 src/main.py $case 1 1 $initialDatapoints > ./$dir/${case}_poly.txt
    echo "$case done."
    update_counter
}


run_case_without_couterexampleloops() {
    local initialDatapoints=$1
    local case=$2
    print_date_time
    echo "running FlashSyn-inter with $initialDatapoints initial datapoints without counterexample driven loops for $case..."
    timeout 10800s python3.7 src/main.py $case 0 1 $initialDatapoints > ./$dir/${case}_inte.txt
    echo "$case done."
    update_counter

    print_date_time
    echo "running FlashSyn-poly with $initialDatapoints initial datapoints without counterexample driven loops for $case..."
    timeout 7200s python3.7 src/main.py $case 1 1 $initialDatapoints > ./$dir/${case}_poly.txt
    echo "$case done."
    update_counter
}




# Counters for benchmarks
total_benchmarks=$((2 * 2 * (10 + 4 + 2) * 4)) # 2 runs for 16 benchmarks, 4 initial datapoints
completed_benchmarks=0


# Check for user input
if [ $# -eq 0 ]; then

    for case in 'bZx1' 'bEarnFi' 'Eminence' 'Warp' 'Puppet' 'PuppetV2' 'ElevenFi' 'OneRing' 'Novo' 'Wdoge'; do
        echo "================== Running FlashSyn on ${case}... =================="
        for initialDatapoints in 200 500 1000 2000; do
            dir="Results-To-Reproduce/FlashSynData/${initialDatapoints}+X"
            mkdir -p ./$dir
            run_case "$initialDatapoints" "$case"
            run_case_without_couterexampleloops "$initialDatapoints" "$case"
        done
    done

    for case in 'Harvest_USDC' 'Harvest_USDT' 'ValueDeFi' 'ApeRocket'; do
        echo "================== Running FlashSyn on ${case}... =================="
        for initialDatapoints in 200 500 1000 2000; do
            dir="Results-To-Reproduce/FlashSynData/${initialDatapoints}+X"
            mkdir -p ./$dir
            run_case "$initialDatapoints" "$case"
            run_case_without_couterexampleloops "$initialDatapoints" "$case"
        done
    done


    for case in 'CheeseBank' 'AutoShark'; do
        echo "================== Running FlashSyn on ${case}... =================="
        for initialDatapoints in 200 500 1000 2000; do
            dir="Results-To-Reproduce/FlashSynData/${initialDatapoints}+X"
            mkdir -p ./$dir
            run_case "$initialDatapoints" "$case"
            run_case_without_couterexampleloops "$initialDatapoints" "$case"
        done
    done

    
else
    for initialDatapoints in 200 500 1000 2000; do
        dir="Results-To-Reproduce/FlashSynData/${initialDatapoints}+X"
        mkdir -p ./$dir
        run_case "$initialDatapoints" "$1"
        run_case_without_couterexampleloops "$initialDatapoints" "$1"
    done
fi




echo "===================================================================================================="
echo "========================================== ALL COMPLETE ============================================"
echo "===================================================================================================="
