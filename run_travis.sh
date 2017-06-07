#!/bin/bash

# Install the data needed by NLTK to tokenize
python3.5 -m nltk.downloader punkt

# Run the unit tests
python3.5 prepare_data_test.py