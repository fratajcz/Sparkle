#!/bin/bash

# Execute this script from the Sparkle directory

#SBATCH --job-name=test/save_snapshot.sh
#SBATCH --output=Tmp/save_snapshot.sh.txt
#SBATCH --error=Tmp/save_snapshot.sh.err
#SBATCH --partition=graceADA
#SBATCH --mem-per-cpu=3gb
#SBATCH --exclude=
#SBATCH --ntasks=1
#SBATCH --nodes=1

# Initialise
sparkle/CLI/initialise.py > /dev/null

# Save snapshot
output="$(sparkle/CLI/save_snapshot.py | tail -1)"
if [[ "$output" == *".zip saved successfully!" ]];
then
    echo "[success] save_snapshot test succeeded"
else
    echo "[failure] save_snapshot test failed with output:"
    echo "$output"
fi
