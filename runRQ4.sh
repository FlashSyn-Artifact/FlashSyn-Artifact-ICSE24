#!/bin/bash

dir='Results-To-Reproduce/FlashFind+FlashSynData'
mkdir -p ./$dir


# Function to print current date and time
print_date_time() {
    echo "========= Current Date and Time: $(date) ========="
}

# Counters for benchmarks
total_benchmarks=11 # 2 runs for 16 benchmarks
completed_benchmarks=0

# Function to update and display counter
update_counter() {
    completed_benchmarks=$((completed_benchmarks + 1))
    remaining_benchmarks=$((total_benchmarks - completed_benchmarks))
    echo "Benchmarks: $completed_benchmarks/$total_benchmarks finished, $remaining_benchmarks/$total_benchmarks to do"
}


run_case() {
    local case=$1
    print_date_time
    echo "running FlashSyn-poly with actions discovered by FlashFind with 2000 initial datapoints with counterexample driven loops for $case..."
    timeout 7200s python3.7 src/mainExtra.py $case 1 > ./$dir/${case}_poly.txt
    echo "$case done."
    update_counter
}


# Check for user input
if [ $# -eq 0 ]; then
    # easy
    for case in  'bZx1' 'bEarnFi' 'Novo' 'Wdoge'; do
        run_case "$case"
    done

    # mid
    for case in  'OneRing' 'Eminence'; do
        run_case "$case"
    done

    # hard
    for case in  'Harvest_USDT' 'Harvest_USDC' 'ValueDeFi' 'Warp' 'ApeRocket'; do
        run_case "$case"
    done
    
else
    # Argument provided, run for the specified case
    run_case "$1"
fi




echo "===================================================================================================="
echo "========================================== ALL COMPLETE ============================================"
echo "===================================================================================================="
