#!/bin/bash

# Install the data needed by NLTK to tokenize
python3.5 -m nltk.downloader punkt

# Run the unit tests
#python3.5 test_prepare_data.py