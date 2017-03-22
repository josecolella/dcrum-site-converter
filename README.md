# dcrum-site-converter
A small commandline program to transform an excel or csv to a standardised Dynatrace DCRUM site csv


Usage:

```sh
python main.py -i subnets_16032017.xlsx -o file4.csv -m '{"Id": "", "Domains": "Network", "Name": "Description", "Site Type": "Manual", "Region": "Madrid", "Area": "Site", "Comment": "Location", "UDL": "false", "WAN": "false", "Link Speed In": "", "Link Speed Out": ""}' -t True
```
