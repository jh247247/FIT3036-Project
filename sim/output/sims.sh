SIM_PATH="../DaisyWorld.py"
SIM_DEFAULT_OPTIONS="-g"
SIM_START_TEMP=-20
SIM_STOP_TICK=10000
SIM_DELTA_RAD=$(echo "2/$SIM_STOP_TICK" | bc -l)
SIM_INITIAL_RAD=0.5

AMOUNT_OF_RUNS=40
MAX_THREADS_BACKGROUND=4

OUTPUT_EXTENSION=".csv"

BASE_OUTPUT_NAME="default"

function gen {
    r=1
    # base case, no invasive
    while [ $r -le $AMOUNT_OF_RUNS ]; do
        for j in $(seq 1 $MAX_THREADS_BACKGROUND); do
            if [ $r -le $AMOUNT_OF_RUNS ]; then
                echo "Run count: " $r
                python3 $SIM_PATH $SIM_DEFAULT_OPTIONS -s $SIM_STOP_TICK \
                        -t $SIM_START_TEMP -r $SIM_INITIAL_RAD \
                        -d $SIM_DELTA_RAD $2 > \
                        $1"-"$r$OUTPUT_EXTENSION &
                ((r++))
            fi
        done
        wait
    done
}

function plot {
    octave --eval "plotOutput('$1')"
}

gen $BASE_OUTPUT_NAME
plot $BASE_OUTPUT_NAME
