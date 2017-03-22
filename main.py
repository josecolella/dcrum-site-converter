# Copyright (c) 2017 Jose Colella

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="dcrum-site-converter",
        description="""A program to given a csv or excel will transform it to a standardized CSV that can be imported.
        The command line program requires an input file and output file and a mapping. The input file is a string, as is the output file.
        The mapping is a JSON string that maps the official Site columns to the columns in the input file. For example, give the following JSON mapping:
        '{
              "Area": "Site",
              "Comment": "Location",
              "Domains": "Network",
              "Id": "",
              "Link Speed In": "",
              "Link Speed Out": "",
              "Name": "Description",
              "Region": "Madrid",
              "Site Type": "Manual",
              "UDL": "false",
              "WAN": "false"
        }'
        the program will create an Area Column with the content of the Site column of the input file. It will do this for all the columns.
        The resulting output file will only contain the following columns:
            - "Id", "Name", "Site Type", "Region", "Area", "UDL", "WAN", "Link Speed In", "Link Speed Out", "Comment", "Domains"
        to match the official site csv definition.

        Example usage:

        python main.py -i subnets_16032017.xlsx  -o outfile.csv -m '{"Id": "", "Domains": "Network", "Name": "Description", "Site Type": "Manual", "Region": "Madrid", "Area": "Site", "Comment": "Location", "UDL": "false", "WAN": "false", "Link Speed In": "", "Link Speed Out": ""}'
        """
    )
    parser.add_argument(
        '-i',
        '--input',
        help="The file to convert (excel or csv)",
        type=str,
        required=True
    )
    parser.add_argument(
        '-m',
        '--mapping',
        help="The mapping from the input file columns to the DCRUM site file",
        type=str,
        required=True
    )
    parser.add_argument(
        '-o',
        '--output',
        help="The name of the output file",
        type=str,
        required=True)
    parser.add_argument(
        '-t',
        '--translate_networks',
        help="If the script should translate the networks to ranges",
        type=bool,
        default=False
    )

    args = parser.parse_args()
    input_file = args.input
    mappings = json.loads(args.mapping)
    output_file = args.output
    translate = args.translate_networks

    import siteConverter
    site = siteConverter.SiteConverter(input_file)
    site.clean_to_site_definition(mappings, translate)
    site.transform_to_site_definition()
    site.save_to_site_definition(output_file)
