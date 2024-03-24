from pyteomics import mzid
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


def write_psms(fp, psms, dataset_number):
    peptides = {}
    number = 0
    for psm in psms:
        number += 1
        spectrum = psm['spectrum']
        calculatedMassToCharge = psm['calculatedMassToCharge']
        experimentalMassToCharge = psm['experimentalMassToCharge']
        charge = psm['charge']
        start = psm['start']
        end = psm['end']
        sequence = psm['sequence']
        protein = psm['protein']

        fp.write(f':PSM{dataset_number}_{number} a jpost:PSM ;\n')
        fp.write(f'    dct:identifier "PSM{dataset_number}_{number}" ;\n')
        fp.write(f'    jpost:hasSpectrum {spectrum} ;\n')
        fp.write(f'    sio:SIO_000216 [\n')
        fp.write(f'        a jpost:CalculatedMassToCharge ;\n')
        fp.write(f'        sio:SIO_000221 obo:MS_1000040 ;\n')
        fp.write(f'        sio:SIO_000300 {calculatedMassToCharge} \n')
        fp.write(f'    ] ;\n')
        fp.write(f'    sio:SIO_000216 [\n')
        fp.write(f'        a jpost:ExperimentalMassToCharge ;\n')
        fp.write(f'        sio:SIO_000221 obo:MS_1000040 ;\n')
        fp.write(f'        sio:SIO_000300 {experimentalMassToCharge} \n')
        fp.write(f'    ] ;\n')
        fp.write(f'    sio:SIO_000216 [\n')
        fp.write(f'        sio:SIO_000221 obo:MS_1000041 ;\n')        
        fp.write(f'        sio:SIO_000300 {charge} \n')
        fp.write(f'    ] .\n')
        fp.write('\n')

        peptide = f'{start}_{end}_{sequence}_{protein}'
        if peptide in peptides:
            peptides[peptide].append(f'PSM{dataset_number}_{number}')
        else:
            peptides[peptide] = [f'PSM{dataset_number}_{number}']

    return peptides


def write_peptides(fp, peptides, dataset_number):
    proteins = {}
    number = 0
    for peptide, psms in peptides.items():
        number += 1
        pep_id = f'PEP{dataset_number}_{number}'
        start, end, sequence, protein = peptide.split('_')
        fp.write(f':DS{dataset_number} jpost:hasPeptide {pep_id} .\n')
        fp.write(f':{pep_id} a jpost:Peptide ;\n')
        for psm in psms:
            fp.write(f'    jpost:hasPSM {psm} ;\n')
        fp.write(f'    sio:SIO_000216 [\n')
        fp.write(f'        a jpost:numOfPsms ;\n')
        fp.write(f'    dct:identifier "pep_id" ;\n')
        fp.write(f'    sio:SIO_000300 {len(psms)} \n')
        fp.write(f'    ] ;\n')
        fp.write(f'    sio:SIO_000216 [\n')
        fp.write(f'        a obo:MS_1001344 ;\n')
        fp.write(f'        sio:SIO_000300 {sequence} \n')
        fp.write(f'    ] .\n')
        fp.write('\n')
        
        protein_key = f'{start}_{end}_{protein}'
        if protein_key in proteins:
            proteins[protein_key].append(pep_id)
        else:
            proteins[protein_key] = [pep_id]

    return proteins


def write_proteins(fp, proteins, dataset_number):
    number = 0
    for protein, peptides in proteins.items():
        number += 1
        start, end, protein = protein.split('_')
        protein_id = f'PRT{dataset_number}_{number}'
        fp.write(f':DS{dataset_number} jpost:hasProtein {protein_id} .\n')
        fp.write(f':{protein_id} a jpost:Protein ;\n')
        fp.write(f'    dct:identifier "{protein_id}" ;\n')
        for peptide in peptides:
            fp.write(f'    jpost:hasPeptideEvidence [\n')
            fp.write(f'        a jpost:PeptideEvidence ;\n')
            fp.write(f'        jpost:hasPeptide :{peptide} ;\n')
            fp.write(f'        faldo:location [\n')
            fp.write(f'            a faldo:Region ;\n')
            fp.write(f'            faldo:begin [\n')
            fp.write(f'                a faldo:ExactPosition ;\n')
            fp.write(f'                faldo:reference :{peptide} ;\n')
            fp.write(f'                faldo:position {start} \n')
            fp.write(f'            ] ;\n')
            fp.write(f'            faldo:end [\n')
            fp.write(f'                a faldo:ExactPosition ;\n')
            fp.write(f'                faldo:reference :{peptide} ;\n')
            fp.write(f'                faldo:position {end} \n')
            fp.write(f'            ] ;\n')            
            fp.write(f'        ] ;\n')
            fp.write(f'    ] .\n')
        


def write_rawdata(fp, rawdata_map, dataset_number):
    for location, rawdata_id in rawdata_map.items():
        fp.write(f'bid:PRF{dataset_number} jpost:hasRawData {rawdata_id} .\n')
        fp.write(f':{rawdata_id} a jpost:RawData ;\n')
        fp.write(f'    rdfs:label "{location} ." ;\n')
        fp.write('\n')


def write_spectrum(fp, spectrum_map, dataset_number):
    for spectrum, spectrum_id in spectrum_map.items():
        spec_id, rawdata_id = spectrum.split(';')
        fp.write(f':{spectrum_id} a jpost:Spectrum ;\n')
        fp.write(f'    rdfs:label "{spec_id} ;" ;\n')
        fp.write(f'    jpost:inRawData bid:{rawdata_id} .\n')
        fp.write('\n')


def write_dataset(fp, dataset_number, reader):
    fp.write(f':DS{dataset_number} a jpost:Dataset ;\n')
    fp.write(f'    jpost:hasProfile bid:PRF{dataset_number} .\n')
    fp.write(f'bid:PRF{dataset_number} a jpost:Profile .\n')
    
    rawdata_map = {}
    spectrum_map = {}
    psms = []
    for record in reader:
        spectrum = record['spectrumID']
        location = record['location']
        spectrum_id = f'bid:SPC{dataset_number}_{len(spectrum_map) + 1}'
        rawdata_id = f'bid:RAW{dataset_number}_{len(rawdata_map) + 1}'

        if location in rawdata_map:
            rawdata_id = rawdata_map[location]
        else:
            rawdata_map[location] = rawdata_id

        if spectrum in spectrum_map:
            spectrum_id = spectrum_map[spectrum + ';' + rawdata_id]
        else:
            spectrum_map[spectrum + ';' + rawdata_id] = spectrum_id

        items = record['SpectrumIdentificationItem']
        for item in items:
            calculatedMassToCharge = item['calculatedMassToCharge']
            experimentalMassToCharge = item['experimentalMassToCharge']
            charge = item['chargeState']
            rank = item['rank']

            peptides = item['PeptideEvidenceRef']
            for peptide in peptides:
                start = peptide['start']
                end = peptide['end']
                sequence = peptide['PeptideSequence']
                protein = peptide['protein description']

                psms.append({
                    'spectrum': spectrum_id,
                    'rawdata': rawdata_id,
                    'calculatedMassToCharge': calculatedMassToCharge,
                    'experimentalMassToCharge': experimentalMassToCharge,
                    'charge': charge,
                    'rank': rank,
                    'start': start,
                    'end': end,
                    'sequence': sequence,
                    'protein': protein
                })

        peptides = write_psms(fp, psms, dataset_number)
        proteins = write_peptides(fp, peptides, dataset_number)
        write_proteins(fp, proteins, dataset_number)
        write_rawdata(fp, rawdata_map, dataset_number)
        write_spectrum(fp, spectrum_map, dataset_number)


def get_options():
    parser = ArgumentParser()
    parser.add_argument('-m', '--mzid_in', required=True, help='MzIdentML file')
    parser.add_argument('-o', '--output', required=True, help='Output file (TTL)')
    parser.add_argument('-r', '--rev_id', required=True, help='Revision ID')
    parser.add_argument('-n', '--branch_number', required=True, help='Branch number')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_options()

    revision_id = args.rev_id
    branch_number = args.branch_number

    dataset_number = get_dataset_number(revision_id, branch_number)

    fp = open(args.output, 'wt')

    reader = mzid.read(args.mzid_in)
    write_head(fp)
    write_dataset(fp, dataset_number, reader)

    reader.close()
    fp.close()
