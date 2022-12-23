#!/usr/bin/python3

import os
import time
import fnmatch
import chardet
from tqdm import tqdm

dir_path = './'
#get a list of filenames in the directory
filenames = os.listdir(dir_path)
#filter the filenames to include only .sql files
filenames = fnmatch.filter(filenames, '*.sql')
filenames = sorted(filenames)

with tqdm(total=len(filenames), desc="Processing files") as pbar:
    #iterate over the filenames
    for filename in filenames:
        file_path = os.path.join(dir_path, filename)
        try:
            #check if the file is larger than 900KB
            if os.path.getsize(file_path) > 500000:
                #open the file in binary mode
                with open(file_path, 'rb') as f:
                    # Read the file data
                    data = f.read()

                #detect encoding
                result = chardet.detect(data)
                encoding = result['encoding']

                #decode the data using the detected encoding
                lines = data.decode(encoding)

                chunk_size = 450 * 1000
                chunk_data = lines
                chunk_number = 1
                #get the current time in epoch seconds
                epoch_time = str(int(time.time()))
                while len(chunk_data) * 2 > chunk_size:
                    split_point = len(chunk_data) * chunk_size // os.path.getsize(file_path)

                    first_part = chunk_data[:split_point]
                    second_part = chunk_data[split_point:]

                    #write the first part to a new file with the original extension
                    with open(file_path + '.' + epoch_time + '.' + str(chunk_number) + '.sql', 'w') as f:
                        f.writelines(first_part)
                    chunk_data = second_part
                    chunk_number += 1
                #write the last part to a new file with the original extension
                with open(file_path + '.' + epoch_time + '.' + str(chunk_number) + '.sql', 'w') as f:
                    f.writelines(chunk_data)
        except Exception as e:
            # print the error message and continue processing the next file
            print(f"Error preparing file {file_path}: {e}")
            continue
        pbar.update(1)
