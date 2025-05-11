INPUT_BASE="/maps/sj514/overture/theme=transportation/type=segment"
OUTPUT_BASE="/maps/hm708/processed_roads"
SUFFIX="-d84517a6-f7b3-48eb-8ec2-e27684978d01-c000.zstd.parquet"
FRICTION_MAP_PATH1='/maps/hm708/road_friction_map.tif'

INPUT_BASE2="/maps/sj514/overture/theme=base/type=land_cover"
OUTPUT_BASE2="/maps/hm708/processed_land"
SUFFIX2="-4c588cee-fa22-41da-975c-c6df5012d209-c000.zstd.parquet" 
FRICTION_MAP_PATH2=/maps/hm708/land_friction_map.tif

SLOPE_FILE=/maps/hm708/slope_1KMmd_SRTM.tif
ELEVATION_FILE=/maps/hm708/elevation_1KMmd_SRTM.tif
FRICTION_MAP_PATH3=/maps/hm708/land_friction_map_with_sclaing.tif

MAX_PROCS=6




running=0
for i in $(seq 0 49); do
    PART_NUM=$(printf "%05d" $i)
    INPUT_FILE="${INPUT_BASE}/part-${PART_NUM}${SUFFIX}"
    OUTPUT_FILE="${OUTPUT_BASE}${i}.parquet"

    echo "Running: python3 creating_road_speed_table.py '$INPUT_FILE' '$OUTPUT_FILE'"
    python3 creating_road_speed_table.py "$INPUT_FILE" "$OUTPUT_FILE" &

    ((running+=1))

    if [[ $running -ge $MAX_PROCS ]]; then
        wait -n   # wait for any one background process to finish
        ((running-=1))
    fi
done

wait  # wait for any remaining background jobs to finish


# add the querying script
echo "All road preprocessing done. Now assembling road friction map..."
python3 querying_algorithm.py "$OUTPUT_BASE" "$FRICTION_MAP_PATH1" "transportation"
# input_suffix, output_file, type_of_friction_map
wait


running=0

for i in $(seq 0 83); do
  PART_NUM=$(printf "%05d" $i)
  INPUT_FILE2="${INPUT_BASE2}/part-${PART_NUM}${SUFFIX2}"
  OUTPUT_FILE2="${OUTPUT_BASE2}${i}.parquet"

  echo "Running: python3 creating_land_coverage_table.py '$INPUT_FILE2' '$OUTPUT_FILE2'"
  python3 creating_land_coverage_table.py "$INPUT_FILE2" "$OUTPUT_FILE2" &

  ((running+=1))

  if [[ $running -ge $MAX_PROCS ]]; then
    wait -n  # wait for any one background process to finish
    ((running-=1))
  fi
done

wait

echo "All land preprocessing done. Now assembling land friction map..."
python3 querying_algorithm.py "$OUTPUT_BASE2" "$FRICTION_MAP_PATH2" "land"

wait

python3 add_elevation.py "$FRICTION_MAP_PATH2" "$SLOPE_FILE" "$ELEVATION_FILE" "$FRICTION_MAP_PATH3"
#my_data_path, slope_file, elevation_file, output_file