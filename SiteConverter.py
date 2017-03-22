#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# TODO: Optimize convert method
# TODO: Add handling for duplicate site entries

import pandas as pd
import ipcalc
import os
import typing


class SiteDefinitionException(Exception):
    def __init__(self, message, errors):
        super(SiteDefinitionException, self).__init__(message)


class SiteConverter(object):
    # Dictionary with the formal site definition and default values
    DCRUM_SITE_COLUMNS = {
        "Id": '',
        "Name": '',
        "Site Type": 'Manual',
        "Region": '',
        "Area": '',
        "UDL": 'false',
        "WAN": 'false',
        "Link Speed In": '',
        "Link Speed Out": '',
        "Comment": '',
        "Domains": ''
    }

    """docstring for ClassName"""

    def __init__(self, file):
        file_name, extension = os.path.splitext(file)
        if extension == 'csv':
            self.df = pd.read_csv(file)
        else:
            self.df = pd.read_excel(file)
        self.original_columns = self.df.columns.values

    def clean_to_site_definition(self, mappings: dict, translateNetworkMasks=False):
        # Optimize this more
        for column, value in SiteConverter.DCRUM_SITE_COLUMNS.items():
            if mappings[column] and mappings[column] != value:
                try:
                    self.df[column] = self.df[mappings[column]]
                except KeyError:
                    self.df[column] = mappings[column]
            else:
                self.df[column] = value
        if translateNetworkMasks:
            def convertNetworkMask(ipWithNetworkMask: str):
                ipRanges = tuple(str(ip)
                                 for ip in ipcalc.Network(ipWithNetworkMask)
                                 )
                return "{beginningIP}-{endingIP}".format(
                    beginningIP=ipRanges[0], endingIP=ipRanges[-1])
            self.df['Domains'] = self.df[
                'Domains'].apply(convertNetworkMask)

    def transform_to_site_definition(self):
        self.df = self.df[list(SiteConverter.DCRUM_SITE_COLUMNS.keys())]

    def save_to_site_definition(self, file_name: str, sep: str=';'):
        self.df.to_csv(file_name, sep=sep, index=False)
