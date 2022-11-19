#!/bin/bash

umaxnorm=${1:+-m${1}}
u1norm=${2:+-n${2}}
upot=${3:+-p${3}}
coef1=${4:+-u${4}}
coef2=${5:+-v${5}}

# Put here the program (maybe with path)
GETF0="get_pitch $umaxnorm $u1norm $upot $coef1 $coef2"

for fwav in pitch_db/train/*.wav; do
    ff0=${fwav/.wav/.f0}
    echo "$GETF0 $fwav $ff0 ----"
    $GETF0 $fwav $ff0 > /dev/null || (echo "Error in $GETF0 $fwav $ff0"; exit 1)
done

exit 0
