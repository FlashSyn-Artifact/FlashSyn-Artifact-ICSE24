#!/bin/bash

# only 7 benchmarks are available for precise framework
# bEarnFi, Eminence, Puppet, PuppetV2, Wdoge, CheeseBank, Warp, 

dir='Results-To-Reproduce/FlashSynData/precise/'
mkdir -p ./$dir


# Function to print current date and time
print_date_time() {
    echo "========= Current Date and Time: $(date) ========="
}

# Counters for benchmarks
total_benchmarks=7
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
    echo "running FlashSyn-precise baseline for $case..."
    timeout 7200s python3.7 src/mainPrecise.py $case 1 > ./$dir/${case}_precise.txt
    echo "$case (precise) done."
    update_counter
}



# Check for user input
if [ $# -eq 0 ]; then
    # Easy:
    for case in 'bEarnFi' 'Puppet' 'PuppetV2' ; do
        run_case "$case"
    done

    # Mid:
    for case in 'Eminence' 'Wdoge'; do
        run_case "$case"
    done

    # Hard:
    for case in 'CheeseBank' 'Warp'; do
        run_case "$case"
    done
else
    # Argument provided, run for the specified case
    run_case "$1"
fi




echo "===================================================================================================="
echo "========================================== ALL COMPLETE ============================================"
echo "===================================================================================================="
