#!/bin/bash

# set the environment name
ENV_NAME=idb

# activate the environment
echo "Activating $ENV_NAME environment..."
eval "$(conda shell.bash hook)"
conda activate $ENV_NAME

# check if activation was successful
if [ $? -ne 0 ]; then
   	echo "Environment does not exist."
   	echo "Creating $ENV_NAME environment..."
   	conda env create -f environment.yml -n $ENV_NAME
   	conda activate $ENV_NAME
fi

python setup.py sdist
twine upload --repository testpypi  dist/*