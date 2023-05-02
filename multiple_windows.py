from argparse import ArgumentParser
import sys
import os.path
import pandas as pd

from single_window import find_related_genes
from linker import combined_filename

def command_line_parser(main_args):
    parser = ArgumentParser(description="Finds information related to genes from scaffold and location parameters")
    parser.add_argument('-f',
                        '--file',
                        required=True,
                        type=str,
                        help="File containing windows and scaffolds we want to find: each line should be in the form [start, end, scaffold]")
    parser.add_argument('-o',
                        '--output',
                        required=True,
                        type=str,
                        help="Output file containing information about related genes")
    parser.add_argument('-r',
                        '--refresh',
                        default=False,
                        help="Refresh the main dataset")
    args = parser.parse_args(main_args)
    return args

def find_related_from_file(file):
    aggregated_data = []
    with open(file, "r") as related_genes:
        for line in related_genes.readlines():
            split_line = line.strip().split(", ")
            left = split_line[0]
            right = split_line[1]
            scaffold = split_line[2]
            related_genes = find_related_genes(int(left), int(right), scaffold)
            aggregated_data.append(related_genes)


    return pd.concat(aggregated_data)

def main(main_args=None):
    args = command_line_parser(main_args)
    if args.refresh or not os.path.isfile(combined_filename):
        generate_main_data()
        print("Generated main dataset in " + combined_filename)

    related_genes = find_related_from_file(args.file)
    related_genes.to_csv(args.output)


if __name__ == '__main__':
    main(sys.argv[1:])
