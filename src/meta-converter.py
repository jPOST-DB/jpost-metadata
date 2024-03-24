import pandas as pd
from argparse import ArgumentParser


def get_dataset_number(revision_id, branch_number):
    project_number = int(revision_id.replace('JPST', ''))
    ds_number = f'{project_number}_{branch_number}'
    return ds_number


def write_head(fp):
    prefixes = [
        '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .',
		'@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .',
        '@prefix dct: <http://purl.org/dc/terms/> .',
        '@prefix uniprot: <http://purl.uniprot.org/uniprot/> .',
        '@prefix isoforms: <http://purl.uniprot.org/isoforms/> .',
        '@prefix idup: <http://identifiers.org/uniprot/> .',
        '@prefix taxonomy: <http://identifiers.org/taxonomy/> .',
        '@prefix obo: <http://purl.obolibrary.org/obo/> .',
        '@prefix ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#> .',
        '@prefix unimod: <http://www.unimod.org/obo/unimod.obo#> .',
        '@prefix sio: <http://semanticscience.org/resource/> .',
        '@prefix foaf: <http://xmlns.com/foaf/0.1/> .',
        '@prefix faldo: <http://biohackathon.org/resource/faldo#> .',
        '@prefix skos: <http://www.w3.org/2004/02/skos/core#> .',
        '@prefix px: <https://github.com/PX-RDF/ontology/blob/master/px.owl#> .',
        '@prefix pxd: <http://proteomecentral.proteomexchange.org/dataset/> .',
        '@prefix jpost: <http://rdf.jpostdb.org/ontology/jpost.owl#> .',
        '@prefix jrepo: <https://repository.jpostdb.org/entry/> .',
        '@prefix bid: <http://rdf.jpostdb.org/bid/> .',
        '@prefix vcard: <http://www.w3.org/2006/vcard/ns#> .',
        '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .',
        '@prefix : <http://rdf.jpostdb.org/entry/> .'
    ]

    for prefix in prefixes:
        fp.write(prefix + '\n')
    fp.write('\n')


def write_dataset(fp, dataset_number, taxonomy_df, function_df):
    fp.write(f':DS{dataset_number} a jpost:Dataset ;\n')

    for index in taxonomy_df.index:
        id = index + 1
        fp.write(f'    jpost:hasTaxonomy :TAX{dataset_number}_{id} ;\n')
    
    for index in function_df.index:
        id = index + 1
        fp.write(f'    jpost:hasFormula :FUN{dataset_number}_{id} ;\n')

    fp.write(f'    rdfs:label "DS{dataset_number}" .\n')


def writeTaxonomy(fp, dataset_number, taxonomy_df):
    for index in taxonomy_df.index:
        number = index + 1
        id = f'TAX{dataset_number}_{number}'
        fp.write(f':{id} a jpost:Taxonomy ;\n')
        fp.write(f'    dct:identifier "{id}" ;\n')
        fp.write(f'    rdfs:label "{taxonomy_df.loc[index, "Genome"]}" ;\n')
        fp.write(f'    jpost:psmCount {taxonomy_df.loc[index, "PSM count"]} ;\n')
        fp.write(f'    jpost:pepCount {taxonomy_df.loc[index, "Peptide count"]} ;\n')
        fp.write(f'    jpost:gtd :GTDB{number} ;\n')
        fp.write(f'    jpost:taxonomy :NCBI{number} .\n')

        if not str(taxonomy_df.loc[index, "GTDB_Name"]) == 'nan':
            fp.write(f':GTDB{number} a jpost:GTDB ;\n')
            fp.write(f'    rdfs:label "{taxonomy_df.loc[index, "GTDB_Name"]}" ;\n')
            fp.write(f'    jpost:rank "{taxonomy_df.loc[index, "GTDB_Rank"]}" ;\n')
            fp.write(f'    jpost:superkingdom "{taxonomy_df.loc[index, "GTDB_Superkingdom"]}" ;\n')
            fp.write(f'    jpost:phylum "{taxonomy_df.loc[index, "GTDB_Phylum"]}" ;\n')
            fp.write(f'    jpost:class "{taxonomy_df.loc[index, "GTDB_Class"]}" ;\n')
            fp.write(f'    jpost:order "{taxonomy_df.loc[index, "GTDB_Order"]}" ;\n')
            fp.write(f'    jpost:family "{taxonomy_df.loc[index, "GTDB_Family"]}" ;\n')
            fp.write(f'    jpost:genus "{taxonomy_df.loc[index, "GTDB_Genus"]}" ;\n')
            fp.write(f'    jpost:species "{taxonomy_df.loc[index, "GTDB_Species"]}" .\n')

        if not str(taxonomy_df.loc[index, "NCBI_Name"]) == 'nan':
            fp.write(f':NCBI{number} a jpost:NCBI ;\n')
            fp.write(f'    rdfs:label "{taxonomy_df.loc[index, "NCBI_Name"]}" ;\n')
            fp.write(f'    jpost:rank "{taxonomy_df.loc[index, "NCBI_Rank"]}" ;\n')
            fp.write(f'    jpost:superkingdom "{taxonomy_df.loc[index, "NCBI_Superkingdom"]}" ;\n')
            fp.write(f'    jpost:phylum "{taxonomy_df.loc[index, "NCBI_Phylum"]}" ;\n')
            fp.write(f'    jpost:class "{taxonomy_df.loc[index, "NCBI_Class"]}" ;\n')
            fp.write(f'    jpost:order "{taxonomy_df.loc[index, "NCBI_Order"]}" ;\n')
            fp.write(f'    jpost:family "{taxonomy_df.loc[index, "NCBI_Family"]}" ;\n')
            fp.write(f'    jpost:genus "{taxonomy_df.loc[index, "NCBI_Genus"]}" ;\n')
            fp.write(f'    jpost:species "{taxonomy_df.loc[index, "NCBI_Species"]}" .\n  ')
            fp.write('\n')


def writeFunction(fp, dataset_number, function_df):
    for index in function_df.index:
        number = index + 1
        id = f'FUN{dataset_number}_{number}'
        fp.write(f':{id} a jpost:Function ;\n')
        fp.write(f'    dct:identifier "{id}" ;\n')
        fp.write(f'    rdfs:label "{function_df.loc[index, "Name"]}" ;\n')
        fp.write(f'    jpost:proteinId {function_df.loc[index, "Protein_ID"]} ;\n')
        fp.write(f'    jpost:psmCount {function_df.loc[index, "PSM count"]} ;\n')
        fp.write(f'    jpost:pepCount {function_df.loc[index, "Peptide count"]} ;\n')        
        fp.write(f'    jpost:score {function_df.loc[index, "Score"]} ;\n')
        fp.write(f'    jpost:intensity {function_df.loc[index, "Intensity no1"]} ;\n')
        fp.write(f'    jpost:annotation :MAG{dataset_number}_{number} .\n')

        go_ids = function_df.loc[index, "Gene_Ontology_id"].split(';')
        go_names = str(function_df.loc[index, "Gene_Ontology_name"]).split(';')
        go_namespaces = str(function_df.loc[index, "Gene_Ontology_namespace"]).split(';')

        fp.write(f':MAG{dataset_number}_{number} a jpost:Annotation ;\n')
        if len(go_ids) == len(go_names) == len(go_namespaces):
            for go_id, go_name, go_namespace in zip(go_ids, go_names, go_namespaces):
                if not go_id == '-':
                    fp.write(f'     jpost:hasGO [\n')
                    fp.write(f'        dct:identifier "{go_id}" ;\n')
                    fp.write(f'        rdfs:label "{go_name}" ;\n')
                    fp.write(f'        jpost:namespace "{go_namespace}" \n')
                    fp.write(f'    ] ;\n')
        if not function_df.loc[index, "EC_id"] == '-':
            fp.write(f'    jpost:ec [\n')
            fp.write(f'        dct:identifier "{function_df.loc[index, "EC_id"]}" ;\n')
            fp.write(f'        jpost:de "{function_df.loc[index, "EC_de"]}" ;\n')
            fp.write(f'        jpost:an "{function_df.loc[index, "EC_an"]}" ;\n')
            fp.write(f'        jpost:an "{function_df.loc[index, "EC_ca"]}" \n')
            fp.write(f'    ] ;\n')
        if not function_df.loc[index, "KEGG_ko"] == '-':
            fp.write(f'    jpost:kegg [\n')
            fp.write(f'        dct:identifier "{function_df.loc[index, "KEGG_ko"]}" ;\n') 
            fp.write(f'        jpost:entry "{function_df.loc[index, "KEGG_Pathway_Entry"]}" ;\n')
            fp.write(f'        jpost:name "{function_df.loc[index, "KEGG_Pathway_Name"]}" ;\n')
            fp.write(f'        jpost:module "{function_df.loc[index, "KEGG_Module"]}" ;\n')
            fp.write(f'        jpost:reaction "{function_df.loc[index, "KEGG_Reaction"]}" ;\n')
            fp.write(f'        jpost:rclass "{function_df.loc[index, "KEGG_rclass"]}" \n')
            fp.write(f'    ] ;\n')
        if not str(function_df.loc[index, "COG accession"]) == 'nan':
            fp.write(f'    jpost:cog [\n')
            fp.write(f'        dct:identifier "{function_df.loc[index, "COG accession"]}" ;\n') 
            fp.write(f'        jpost:category "{function_df.loc[index, "COG category"]}" ;\n')
            fp.write(f'        jpost:name "{function_df.loc[index, "COG name"]}" \n')  
            fp.write(f'    ] ;\n')
        if not str(function_df.loc[index, "NOG accession"]) == 'nan':
            fp.write(f'    jpost:nog [\n')
            fp.write(f'        dct:identifier "{function_df.loc[index, "NOG accession"]}" ;\n')
            fp.write(f'        jpost:category "{function_df.loc[index, "NOG category"]}" ;\n')  
            fp.write(f'        jpost:name "{function_df.loc[index, "NOG name"]}" \n')  
            fp.write(f'    ] ;\n')
        fp.write(f'    jpost:cazy "{function_df.loc[index, "CAZy"]}" ;\n')
        fp.write(f'    jpost:bigg "{function_df.loc[index, "BiGG_Reaction"]}" ;\n')
        fp.write(f'    jpost:pfams "{function_df.loc[index, "PFAMs"]}" .\n')        
        fp.write('\n')

def get_options():
    parser = ArgumentParser()
    parser.add_argument('-t', '--taxonomy_in', required=True, help='Taxonomy input file (TSV)')
    parser.add_argument('-f', '--function_in', required=True, help='Function input file (TSV)')
    parser.add_argument('-o', '--output', required=True, help='Output file (TTL)')
    parser.add_argument('-r', '--rev_id', required=True, help='Revision ID')
    parser.add_argument('-n', '--branch_number', required=True, help='Branch number')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_options()

    revision_id = args.rev_id
    branch_number = args.branch_number

    dataset_number = get_dataset_number(revision_id, branch_number)

    taxonomy_df = pd.read_csv(args.taxonomy_in, sep='\t')
    function_df = pd.read_csv(args.function_in, sep='\t')

    fp = open(args.output, 'wt')
    write_head(fp)
    write_dataset(fp, dataset_number, taxonomy_df, function_df)
    fp.write('\n')

    writeTaxonomy(fp, dataset_number, taxonomy_df)
    writeFunction(fp, dataset_number, function_df)

    fp.close()
