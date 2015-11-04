#!/bin/bash

for detModel in 38
do
    for recoVar in {69..76}
    do
        python MetaDataSetting.py ${detModel} ${recoVar}
    done
done
