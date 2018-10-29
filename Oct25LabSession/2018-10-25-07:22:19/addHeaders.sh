#!/bin/bash

names1="ACC"
names2="BVP"
names3="EDA"
names4="HR"
names5="IBI"
names6="TEMP"
ext='.csv'

for d in */; do
    echo "Fixing headers for session: "$d
    $(gsed -i '1d' $d$names1$ext)
    $(gsed -i '1s/^/Accelerometer x,Accelerometer y,Accelerometer z\n/' $d$names1$ext)

    $(gsed -i '1d' $d$names2$ext)
    $(gsed -i '1s/^/BVP\n/' $d$names2$ext)

    $(gsed -i '1d' $d$names3$ext)
    $(gsed -i '1s/^/EDA\n/' $d$names3$ext)

    $(gsed -i '1d' $d$names4$ext)
    $(gsed -i '1s/^/HR\n/' $d$names4$ext)

    $(gsed -i '1d' $d$names5$ext)
    $(gsed -i '1s/^/IBI\n/' $d$names5$ext)

    $(gsed -i '1d' $d$names6$ext)
    $(gsed -i '1s/^/TEMP\n/' $d$names6$ext)
done
