#!/usr/bin/env python3
"""
writes for file storage
"""
import datetime
import random

# FILES
FILE_HASH = str(random.random()).split('.')[1]
AVM_RESULTS = "./file_storage/avm_results_{}.py".format(FILE_HASH)

def append_to_file_storage(avm_results):
    """
    appends the findings to file in case of crash
    """
    with open(AVM_RESULTS, "a", encoding="utf-8") as open_file:
        open_file.write(avm_results)
