from argparse import ArgumentParser
import sys
import os.path
import pandas as pd

from linker import generate_main_data, combined_filename

def command_line_parser(main_args):
    parser = ArgumentParser(description="Finds information related to genes from scaffold and location parameters")
    parser.add_argument('-l',
                        '--left',
                        required=True,
                        type=int,
                        help="The left limit of the window we are looking for")
    parser.add_argument('-r',
                        '--right',
                        required=True,
                        type=int,
                        help="The right limit of the window we are looking for")
    parser.add_argument('-s',
                        '--scaffold',
                        required=True,
                        type=int,
                        help="The scaffold we are looking for")
    parser.add_argument('-f',
                        '--refresh',
                        default=False,
                        help="Refresh the main dataset")
    args = parser.parse_args(main_args)
    return args


def find_related_genes(left, right, scaffold):
    data = pd.read_csv(combined_filename)
    scaffold_name = "scaffold_"+str(scaffold)
    scaffold_filtered = data[data['Seqid'] == scaffold_name]
    left_filtered = scaffold_filtered[scaffold_filtered['End'] > left]
    right_filtered = left_filtered[left_filtered['Start'] < right]
    return right_filtered


def main(main_args=None):
    args = command_line_parser(main_args)
    if args.refresh or not os.path.isfile(combined_filename):
        generate_main_data()
        print("Generated main dataset in " + combined_filename)

    related_genes = find_related_genes(args.left, args.right, args.scaffold)
    print(related_genes)


if __name__ == '__main__':
    main(sys.argv[1:])
