import sys

header = sys.stdin.readline().strip().split(",")
first_data_row = sys.stdin.readline().strip().split(",")

if header and first_data_row:
    for column, value in zip(header, first_data_row):
        print(f"{column}: {value}")
