#!/usr/bin/env python

fare_rules = open('metros/ATX/fare_rules.txt', 'rU')

for line in fare_rules:
    columns = line.split(',')
    if columns[1] == '550':
        print columns

fare_rules.close()