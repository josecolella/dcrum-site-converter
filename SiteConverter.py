#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pandas as pd
import ipcalc


class SiteConverter(object):
    DCRUM_SITE_COLUMNS = ["Id", "Name", "Site Type", "Region", "Area",
                          "UDL", "WAN", "Link Speed In", "Link Speed Out",
                          "Comment", "Domains"]

    """docstring for ClassName"""

    def __init__(self, file):
        self.remove_column_set = set()
        self.df = pd.read_excel(file)
        self.original_columns = self.df.columns.values

    def _convertNetworkMask(self, ipWithNetworkMask):
        ipRanges = tuple(str(ip) for ip in ipcalc.Network(ipWithNetworkMask))
        return "{beginningIP}-{endingIP}".format(beginningIP=ipRanges[0], endingIP=ipRanges[-1])

    def convert(self, mappings):
        ##OPTIMIZE THIS METHOD
        self.df['Id'] = ''
        self.df['Domains'] = self.df[
            mappings['Domains']].apply(self._convertNetworkMask)
        del self.df[mappings['Domains']]
        self.remove_column_set.add(mappings['Domains'])
        self.df['Name'] = self.df[mappings['Name']]
        del self.df[mappings['Name']]
        self.remove_column_set.add(mappings['Name'])
        self.df['Site Type'] = 'Manual'
        self.df['Region'] = 'Madrid'
        self.df['Area'] = self.df[mappings['Area']]
        del self.df[mappings['Area']]
        self.remove_column_set.add(mappings['Area'])
        self.df['UDL'] = 'false'
        self.df['WAN'] = 'false'
        self.df['Link Speed In'] = ''
        self.df['Link Speed Out'] = ''
        self.df['Comment'] = self.df[mappings['Comment']]
        del self.df[mappings['Comment']]
        self.remove_column_set.add(mappings['Comment'])

    def clean(self):
        for original_column in (set(self.original_columns).difference(self.remove_column_set)):
            del self.df[original_column]

    def transform(self):
        self.df = self.df[SiteConverter.DCRUM_SITE_COLUMNS]

    def save(self, file_name, sep=';'):
        self.df.to_csv(file_name, sep=sep, index=False)
