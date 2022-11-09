#!/bin/bash 
# n = $1
# for (( i=0 ; i<$n ; i++ )); 
# do
#     python -m experimentation $2 i
# done

while getopts n:e:i: flag
do
    case "${flag}" in
        n) num=${OPTARG};;
        e) exp=${OPTARG};;
        i) iter=${OPTARG};;    
    esac
done

for (( i=0; i<$num; i++ )); 
do
    python -m experimentation $exp $i $iter
done