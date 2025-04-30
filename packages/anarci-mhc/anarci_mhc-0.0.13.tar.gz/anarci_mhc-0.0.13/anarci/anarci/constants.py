import os

# Numbering scheme names
scheme_short_to_long = { "m":"martin", "c":"chothia", "k":"kabat","imgt":"imgt", "kabat":"kabat", "chothia":"chothia", "martin":"martin", "i":"imgt", "a":"aho","aho":"aho","wolfguy":"wolfguy", "w":"wolfguy"}

scheme_names = list(scheme_short_to_long.keys()) 

#all_species = list(all_germlines['V']['H'].keys())

all_species = ["Homo_sapiens",
           "Mus",
           "Rattus_norvegicus",
           "Oryctolagus_cuniculus",
           "Macaca_mulatta",
           "Sus_scrofa",
           "Vicugna_pacos",
           "Bos_taurus"]

amino_acids = sorted(list("QWERTYIPASDFGHKLCVNM"))
set_amino_acids = set(amino_acids)
anarci_path  = os.path.split(__file__)[0]

chain_type_to_class = {"H":"H", "K":"L", "L":"L", "A":"A", "B":"B", "G":"G", "D":"D"}

data_path = os.path.join(anarci_path, "dat")
hmm_path = os.path.join(data_path, 'ALL.hmm')

all_reference_states = list(range( 1, 129)) # These are the IMGT reference states (matches)