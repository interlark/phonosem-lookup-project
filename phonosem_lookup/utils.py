import csv


def read_csv(csv_file, skip_header=False):
    with open(csv_file) as file:
        reader = csv.reader(file)
        if skip_header:
            next(reader, None)  # skip header
        return list(reader)
