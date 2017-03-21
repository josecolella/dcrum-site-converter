import pandas as pd
import ipcalc
import argparse


columns = ["Id", "Name", "Site Type", "Region", "Area", "UDL", "WAN", "Link Speed In", "Link Speed Out", "Comment", "Domains"]


def convertNetworkMask(ipWithNetworkMask):
    ipRanges = tuple(str(ip) for ip in ipcalc.Network(ipWithNetworkMask))
    return "{beginningIP}-{endingIP}".format(beginningIP=ipRanges[0], endingIP=ipRanges[-1])

tmp = set()
df = pd.read_excel('subnets_16032017.xlsx')

original_columns = df.columns.values

df['Id'] = ''
df['Domains'] = df['Name'].apply(convertNetworkMask)
del df['Name']
tmp.add('Name')
df['Name'] = df['Description']
del df['Description']
tmp.add('Description')
df['Site Type'] = 'Manual'
df['Region'] = 'Madrid'
df['Area'] = df['Site']
del df['Site']
tmp.add('Site')
df['UDL'] = 'false'
df['WAN'] = 'false'
df['Link Speed In'] = ''
df['Link Speed Out'] = ''
df['Comment'] = df['Location']
del df['Location']
tmp.add('Location')

for original_column in (set(original_columns).difference(tmp)):
    del df[original_column]

df = df[["Id", "Name", "Site Type", "Region", "Area", "UDL", "WAN", "Link Speed In", "Link Speed Out", "Comment", "Domains"]]

df.to_csv('file2.csv', sep=';', columns=columns, index=False)

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(
# description='Program that converts excels to DCRUM sites format for
# import')
