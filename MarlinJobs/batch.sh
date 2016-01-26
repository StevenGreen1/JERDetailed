#!/bin/bash

for recoVar in 71 #{69..76}
do
    python MarlinSubmit.py 38 ${recoVar}
done
