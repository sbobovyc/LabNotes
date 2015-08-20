if [ -z $1 ] 
then 
	echo "Usage: bash csv2csvMat.sh directory"
else
	DIR=$1
	for f in $DIR/*.csv
	do 
	OUTFILE="${f%.*}_mat.csv"
	cut --delimiter=, --field=2,3,4,5,6,7,8 $f > $OUTFILE
	done	
fi

