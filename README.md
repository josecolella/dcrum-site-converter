# DCRUM-Site-Converter

A small commandline program to transform an excel or csv to a standardised Dynatrace DCRUM site csv

# Why

A way to a automate the creation of the csv that is to be imported in DCRUM which contains all the sites. When given an excel or csv document from a client, the document usually has all the networks with masks instead of ip ranges, or columns that contain valid information but is named incorrectly. This commandline program was created to clean up the input file, transform network to ip ranges, and transform the data to contain only the columns that are used for sites import.

# How

The excel or csv file is imported. Once imported, the commandline utilizes the mapping sent in by the user to map the columns of the resulting file to the column of the input file. This way the user can specify which column holds the information that is to make up the output file, what values the columns should have, etc...

# Requirements

- python
- pandas: Analyze and transform columns 
- ipcalc: Translating Networks into ip ranges, e.g. 192.168.1.0/24 -> 192.168.1.1 - 192.168.1.254
- xlrd: Reading excel files

Usage:

```sh
python main.py -i subnets_16032017.xlsx -o file4.csv -m '{"Id": "", "Domains": "Network", "Name": "Description", "Site Type": "Manual", "Region": "Madrid", "Area": "Site", "Comment": "Location", "UDL": "false", "WAN": "false", "Link Speed In": "", "Link Speed Out": ""}' -t True
```
