INPUT_BASE="/maps/sj514/overture/theme=transportation/type=segment"
OUTPUT_BASE="/maps/hm708/processed_roads"
SCRIPT= "creating_road_speed_table.py"
SUFFIX="-d84517a6-f7b3-48eb-8ec2-e27684978d01-c000.zstd.parquet"
MAX_PROCS=3

running=0
for i in $(seq 0 49); do
    PART_NUM=$(printf "%05d" $i)
    INPUT_FILE="${INPUT_BASE}/part-${PART_NUM}${SUFFIX}"
    OUTPUT_FILE="${OUTPUT_BASE}${i}.parquet"

    echo "Running: python3 $SCRIPT '$INPUT_FILE' '$OUTPUT_FILE'"
    python3 $SCRIPT "$INPUT_FILE" "$OUTPUT_FILE" &

    ((running+=1))

    if [[ $running -ge $MAX_PROCS ]]; then
        wait -n   # wait for any one background process to finish
        ((running-=1))
    fi
done

wait  # wait for any remaining background jobs to finish


# add the querying script
echo "All preprocessing done. Now assembling friction map..."
python3 querying_algorithm.py "$OUTPUT_BASE" "/maps/hm708/road_friction_map.h5" "transportation"
# input_suffix, output_file, type_of_friction_map