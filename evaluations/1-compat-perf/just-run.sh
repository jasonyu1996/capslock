if [ -z "$1" ]; then
    NPROCS=1
else
    NPROCS=$1
fi

export RERUN_MIRI=1

mkdir -p results
python3 ../common/list-selected.py ../common/db.json < top100.txt \
    | parallel -j$NPROCS --bar 'python3 run-single-tests.py {} results/$(basename {}).json'

DRAW=1 python3 process_results.py results
