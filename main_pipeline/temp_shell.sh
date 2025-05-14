INPUT_BASE2="/maps/sj514/overture/theme=base/type=land_cover"
OUTPUT_BASE2="/maps/hm708/pre_processed_land"
SUFFIX2="-4c588cee-fa22-41da-975c-c6df5012d209-c000.zstd.parquet" 
FRICTION_MAP_PATH2="/maps/hm708/land_friction_map.tif"

SLOPE_FILE="/maps/hm708/slope_1KMmd_SRTM.tif"
ELEVATION_FILE="/maps/hm708/elevation_1KMmd_SRTM.tif"
FRICTION_MAP_PATH3="/maps/hm708/land_friction_map_with_sclaing.tif"

MAX_PROCS=7
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

#assembling friction surface
echo "All land preprocessing done. Now assembling land friction map..."
python3 querying_algorithm.py "$OUTPUT_BASE2" "$FRICTION_MAP_PATH2" "land"

wait