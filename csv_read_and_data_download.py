#!/usr/bin/python

import os
import sys
import urllib
import csv

try:
    filename = sys.argv[1]
    url_col_name = sys.argv[2]
except ValueError:
    print("\nERROR: Please specify filename and url column name to download\n")
    print("Usage:")
    print(" $ csv_read_and_data.py data.csv data_url\n")
    print("- First param should be the csv file path")
    print("- Second param should be the column name that has data urls to download\n")
    sys.exit(0)

# open csv file to read
with open(filename, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # iterate on all rows in csv
    for row_index, row in enumerate(csv_reader):
        # find the url column name to download in first row
        if row_index == 0:
            DATA_URL_COL_NUM = None
            for col_index, col in enumerate(row):
                # find the index of column that has urls to download
                if col == url_col_name:
                    DATA_URL_COL_NUM = col_index
            if DATA_URL_COL_NUM is None:
                print("\nERROR: url column name '" + url_col_name + "' not found, available options:")
                for col_index, col in enumerate(row):
                    print(" " + col)
                print("\nUsage:")
                print(" $ csv_read_and_data.py data.csv data_url\n")
                sys.exit(0)
            continue
        # find data urls in rows 1+
        data_url = row[DATA_URL_COL_NUM]
        # check if we have an data URL and download
        if data_url != '' and data_url != "\n":
            data_filename = data_url.split('/')[-1].split('?')[0]
            directory = filename.split('.csv')[0] + "-" + url_col_name
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                urllib.urlretrieve(data_url, directory + '/' + data_filename)
                print("[" + str(row_index) + "] File saved: " + data_filename)
            except ValueError:
                print("[" + str(row_index) + "] Could not download url: " + data_url)
        else:
            print("[" + str(row_index) + "] No url in " + url_col_name)
