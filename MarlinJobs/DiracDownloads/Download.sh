#!/bin/bash

source ../../env.sh

evtType=Z_uds
detModel=38
recoVar=43
jobDescription=JERDetailed

for energy in 30 40 50 60 70 80 #91 100 110 120 130 140 150 160 170 180 190 200 220 240 260 280 300 350 400 450 500
do 
    cd /r06/lc/sg568/JERDetailed/RootFiles/Detector_Model_${detModel}/Reco_Var_${recoVar}/${energy}GeV 
    dirac-ilc-find-in-FC /ilc/user/s/sgreen EvtType=${evtType} MokkaJobNumber=${detModel} ReconstructionVariant=${recoVar} Energy=${energy} JobDescription=${jobDescription} Type=Rec > "tmp.txt"
    while read line 
    do
        if [[ $line == *'.root'* ]]
        then
            if [ ! -f "${line##*/}" ] && [ ! -f "/r06/lc/sg568/JERDetailed/RootFiles/Detector_Model_${detModel}/Reco_Var_${recoVar}/${energy}GeV/${line##*/}" ];
            then
                dirac-dms-get-file $line
            fi
        fi
    done < "tmp.txt"
    rm "tmp.txt"
done

