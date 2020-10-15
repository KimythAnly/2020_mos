for i in $(seq 0 9)
do
    ./render_mos.py -i $i > "naturalness${i}.html"
done

