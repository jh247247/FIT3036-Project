SIM_PATH="../DaisyWorld.py"
SIM_DEFAULT_OPTIONS="-g"
SIM_START_TEMP=-24
SIM_STOP_TICK=100000
SIM_DELTA_RAD=$(echo "2/$SIM_STOP_TICK" | bc -l)
SIM_INITIAL_RAD=0.5

AMOUNT_OF_RUNS=20
MAX_THREADS_BACKGROUND=4

OUTPUT_EXTENSION=".csv"

# invasive black daisies options
INVASIVE_START=22.5
INVASIVE_END=42.5
INVASIVE_INCREMENT=0.5
INVASIVE_OPTION="-b"

BASE_OUTPUT_NAME="normal"
INVASIVE_OUTPUT_NAME="invasive"

function gen {
    r=1
    # base case, no invasive
    while [ $r -le $AMOUNT_OF_RUNS ]; do
        for j in $(seq 1 $MAX_THREADS_BACKGROUND); do
            if [ $r -le $AMOUNT_OF_RUNS ]; then
                echo "Run count: " $r
		# dont you love hacks...
                python3 $SIM_PATH $SIM_DEFAULT_OPTIONS -s $SIM_STOP_TICK \
                        -t $SIM_START_TEMP -r $SIM_INITIAL_RAD \
                        -d $SIM_DELTA_RAD $2 $3 > \
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

function genplot {
    EPOCH=`date +%s`
    gen $1"-"$EPOCH $2
    plot $1"-"$EPOCH
}

genplot $BASE_OUTPUT_NAME

for i in $(seq $INVASIVE_START $INVASIVE_INCREMENT $INVASIVE_END); do
    genplot $INVASIVE_OUTPUT_NAME"-"$i "$INVASIVE_OPTION $i"
done
