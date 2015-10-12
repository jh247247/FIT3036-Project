#!/bin/bash

SIM_PATH="../DaisyWorld.py"
SIM_DEFAULT_OPTIONS="-g"
SIM_START_TEMP=-24
SIM_STOP_TICK=100000
SIM_DELTA_RAD=$(echo "2/$SIM_STOP_TICK" | bc -l)
SIM_INITIAL_RAD=0.5

AMOUNT_OF_RUNS=20
MAX_THREADS_BACKGROUND=4

OUTPUT_EXTENSION=".csv"

r=$1

max=$(expr $r + $MAX_THREADS_BACKGROUND - 1)

while [ $r -le $max ]; do
    # make file name
    fname=$2"-"$r$OUTPUT_EXTENSION

    # check if 3rd arg is set, then invasive enabled...
    if [ ! -z "$3" ]; then
	opt=$3" "$2
	echo opt
    fi

    # if file doesn't exist, create it
    if [ ! -f $fname ]; then
        python3 $SIM_PATH $SIM_DEFAULT_OPTIONS -s $SIM_STOP_TICK \
                -t $SIM_START_TEMP -r $SIM_INITIAL_RAD \
                -d $SIM_DELTA_RAD -rs $r $opt \
                > $fname &
    fi
    ((r++))
done
wait
