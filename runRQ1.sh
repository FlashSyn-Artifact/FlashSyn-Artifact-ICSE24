#!/bin/bash

# Easy: bZx1, bEarnFi, Eminence, Warp, Puppet, PuppetV2, ElevenFi, OneRing, Novo, Wdoge
# Mid: Harvest_USDC, Harvest_USDT, ValueDeFi, ApeRocket
# Hard: CheeseBank, AutoShark
# fail: Yearn, InverseFi

dir='Results-To-Reproduce/FlashSynData/2000+X'
mkdir -p ./$dir

# Function to print current date and time
print_date_time() {
    echo "========= Current Date and Time: $(date) ========="
}

# Counters for benchmarks
total_benchmarks=$((2 * (10 + 4 + 2))) # 2 runs for 16 benchmarks
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
    echo "running FlashSyn-inter with 2000 initial datapoints with counterexample driven loops for $case..."
    timeout 10800s python3.7 src/main.py $case 0 1 2000 > ./$dir/${case}_inte.txt
    echo "$case done."
    update_counter

    print_date_time
    echo "running FlashSyn-poly with 2000 initial datapoints with counterexample driven loops for $case..."
    timeout 7200s python3.7 src/main.py $case 1 1 2000 > ./$dir/${case}_poly.txt
    echo "$case done."
    update_counter
}


# Check for user input
if [ $# -eq 0 ]; then
    # Easy:
    for case in 'bZx1' 'bEarnFi' 'Eminence' 'Warp' 'Puppet' 'PuppetV2' 'ElevenFi' 'OneRing' 'Novo' 'Wdoge'; do 
        run_case "$case"
    done

    # Mid:
    for case in 'Harvest_USDC' 'Harvest_USDT' 'ValueDeFi' 'ApeRocket'; do
        run_case "$case"
    done

    # Hard:
    for case in 'CheeseBank' 'AutoShark'; do
        run_case "$case"
    done
else
    # Argument provided, run for the specified case
    run_case "$1"
fi





echo "===================================================================================================="
echo "========================================== ALL COMPLETE ============================================"
echo "===================================================================================================="