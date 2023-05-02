import gff3_parser
import pandas as pd
gene_info_filepath = "data/Crubella_474_v1.1.gene.gff3"
annotation_delimiter = "	"
annotation_filepath = "data/Crubella_474_v1.1.annotation_info.txt"
combined_filename = "data/main_data.csv"

def generate_main_data():
    parsed_gene_info = gff3_parser.parse_gff3(gene_info_filepath, verbose = False, parse_attributes=True)
    named_genes = parsed_gene_info[parsed_gene_info['Name'].notna()]
    named_genes = named_genes[named_genes['Type'] == "gene"]
    named_genes = named_genes[['Seqid', 'Start', 'End', 'Name']]

    annotations = pd.read_csv(annotation_filepath, sep=annotation_delimiter)
    name_link = annotations[['locusName', 'Best-hit-arabi-name', 'arabi-symbol', 'arabi-defline']]

    combined_map = named_genes.set_index('Name').join(name_link.set_index('locusName'))
    combined_map.to_csv(combined_filename)

