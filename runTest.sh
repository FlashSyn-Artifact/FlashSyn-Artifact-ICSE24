#!/bin/bash

dir='Results-To-Reproduce/FlashSynData/precise/'
mkdir -p ./$dir


# Function to print current date and time
print_date_time() {
    echo "========= Current Date and Time: $(date) ========="
}


# easy
for case in 'bEarnFi' ; do
    print_date_time
    echo "running FlashSyn-precise baseline for $case..."
    timeout 7200s python3.7 src/mainPrecise.py $case 1 > ./$dir/${case}_precise.txt
    echo "$case (precise) done."
done

echo "===================================================================================================="
echo "========================================== ALL COMPLETE ============================================"
echo "===================================================================================================="
