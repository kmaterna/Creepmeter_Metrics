#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt


filelist = ["../Papers/1970s.md", "../Papers/1980s.md",
            "../Papers/1990s.md", "../Papers/2000s.md",
            "../Papers/2010s.md", "../Papers/2020s.md" ]

class Record:
    def __init__(self, date, authors, region):
        self.date = date
        self.authors = authors
        self.region = region

def filter_to_region(list_of_records, target_region):
    return [x for x in list_of_records if x.region == target_region]

def read_dates_list(list_of_files):
    long_records_list = []
    for file in list_of_files:
        long_records_list = long_records_list + read_dates(file)
    return long_records_list

def read_dates(filename):
    records_list = []
    with open(filename, 'r') as ifile:
        for line in ifile:
            chunks = line.split('(')
            if len(chunks) == 0:
                continue
            authors_chunk = chunks[0]
            second_chunk = chunks[1].split(')')[0]
            region = line.split("{")[1].split("}")[0]
            new_record = Record(date=int(second_chunk), authors=authors_chunk, region=region)
            records_list.append(new_record)
    return records_list

def make_stairstep(records_list, starting_date, ending_date):
    x, y = [], []
    date_list = [x.date for x in records_list]
    x.append(starting_date)
    y.append(0)
    for item in date_list:
        x.append(item)
        y.append(y[-1])
        x.append(item)
        y.append(y[-1]+1)
    x.append(ending_date)
    y.append(y[-1])
    return x, y

def make_histogram(date_list):
    plt.figure(figsize=(12, 8), dpi=300)
    plt.hist(date_list, bins=8)
    plt.xticks([1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025])
    plt.ylabel('Number of Papers Using Creepmeters', fontsize=20)
    plt.xlabel('Year', fontsize=20)
    plt.gca().tick_params(axis='both', which='major', labelsize=17)
    plt.title("Total = " + str(len(date_list)) + " Papers", fontsize=20)
    plt.savefig("Paper_bar_plot.png")
    return

def make_timeseries_plot(records_list):
    plt.figure(figsize=(7, 6), dpi=300)
    start_date = 1970
    end_date = 2025
    x, y = make_stairstep(records_list, starting_date=start_date, ending_date=end_date)
    dashed_x = [1971, 2024]
    dashed_y = [0, len(records_list)]
    plt.plot(dashed_x, dashed_y, linestyle='--', linewidth=0.3, color='black')
    plt.plot(x, y, linewidth=5, label='Total')

    CA_list = filter_to_region(records_list, target_region='CA')
    x1, y1 = make_stairstep(CA_list, starting_date=start_date, ending_date=end_date)
    plt.plot(x1, y1, linewidth=1, color='orange', label='California')

    T_list = filter_to_region(records_list, target_region='Turkey')
    x2, y2 = make_stairstep(T_list, starting_date=start_date, ending_date=end_date)
    plt.plot(x2, y2, linewidth=1, color='red', label='Turkey')

    TW_list = filter_to_region(records_list, target_region='Taiwan')
    x3, y3 = make_stairstep(TW_list, starting_date=start_date, ending_date=end_date)
    plt.plot(x3, y3, linewidth=1, color='black', label='Taiwan')

    plt.ylabel('Number of Papers Using Creepmeters', fontsize=20)
    plt.xlabel('Year', fontsize=20)
    plt.gca().tick_params(axis='both', which='major', labelsize=17)
    plt.legend(loc=2, fontsize=20)
    plt.grid(True)
    plt.savefig("TimeSeries_plot.png")
    return


if __name__ == "__main__":
    print("Hello")
    records_list = read_dates_list(filelist)
    make_histogram([x.date for x in records_list])
    make_timeseries_plot(records_list)
