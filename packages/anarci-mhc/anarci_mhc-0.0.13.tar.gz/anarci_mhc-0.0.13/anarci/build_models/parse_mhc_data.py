#!/usr/bin/env python
"""
MHCIMGT.py 
@author: leem
@date:   28 Apr 2016

Tool to parse out HTML from the DomainDisplay tool in IMGT
which has the MHC sequences aligned to IMGT's numbering scheme for the G domain
http://www.imgt.org/3Dstructure-DB/cgi/DomainDisplay.cgi # DomainDisplay tool
http://www.imgt.org/IMGTScientificChart/Numbering/IMGTGsuperfamily.html # Link for numbering

There is a feature to convert IMGT's old-style MHC names into the current standard used by the HLA database
By default, translation is DISABLED but this can be easily ENABLED by commenting out sections flanked with three hashtags ###

"""

from html.parser import HTMLParser
from html.entities import name2codepoint
import re, sys, os, urllib.request, urllib.parse, urllib.error

species = {"Homsap": "homo_sapiens", "Musmus": "mus_musculus"}
common = {"Homsap": "human", "Musmus": "mouse"}
domains = [
    "G-ALPHA",
    "G-ALPHA1",
    "G-ALPHA2",
    "G-BETA",
    "C-LIKE",
    "B2M",
    "G-ALPHA1-LIKE",
    "G-ALPHA2-LIKE",
]


class MHCParser(HTMLParser):
    currenttag = None
    currentnamedent = None

    def handle_starttag(self, tag, attrs):
        self.currenttag = tag
        for a in attrs:
            if "alleleid" in a[1] and tag == "a":
                # if a[1] == "allelename" and tag == "td":
                self.allelename = True

    def handle_endtag(self, tag):
        self.currenttag = None

    def handle_data(self, data):
        split = data.split("\n")

        # Species names are under em tags
        if self.currenttag == "em":
            split = split[0]
            self.species = split

            # If species isn't human or mouse, skip
            if self.species not in species:
                self.species = None

            # If species is currently not logged, then put them in dict
            if self.species in species and self.species not in self._data:
                self._data[self.species] = dict()

        # If we get an em tag with no species, skip
        if not self.species:
            return

        # a tags are unusual; they contain allele names (in the first instance) but contain other accession stuff afterward
        # Get the first a tag assume as allele name, then skip
        if self.currenttag == "a" and self.species in species:
            split = split[0]

            if split and self.allelename:
                self.allele = split
                self.allelename = False

        # Domain names are in the td tag; get the domains
        # If it's an appropriate domain, then stick in along with allele name. Sometimes the same allele will have both a G- and C- domain
        if self.currenttag == "td":
            split = split[0].strip()

            if split in domains:
                self.domain = split

                if not self.allele:
                    return

                # only allow C-LIKE domains if allele is B2M
                B2M_pattern = r"B2M.*"
                if self.domain == "C-LIKE" and not bool(
                    re.match(B2M_pattern, self.allele)
                ):
                    return

                # remove HLA-DM and HLA-DO alleles since these are not peptide presenting
                HLA_D_MO_pattern = r"HLA-D[MO].*"
                if bool(re.match(HLA_D_MO_pattern, self.allele)):
                    return

                # hack to deal with GA being annotated as GB in imgt domain display file as well as missing 'GB' entries
                GA_pattern = r"HLA-D[RPQ]A.*"
                GB_pattern = r"HLA-D[RPQ]B.*"
                if bool(re.match(GA_pattern, self.allele)) and self.domain != "C-LIKE":
                    self.domain = "G-ALPHA"
                if bool(re.match(GB_pattern, self.allele)) and self.domain != "C-LIKE":
                    self.domain = "G-BETA"

                if self.allele and self.allele not in self._data[self.species]:
                    self._data[self.species][self.allele] = {}

                self._data[self.species][self.allele][self.domain] = ""

            # elif split and split == "C-LIKE":
            #     self.domain = None

        # Once we've established a domain, then get the sequence
        if self.domain:
            if (
                self.currenttag == "pre"
                or self.currenttag == "span"
                or self.currenttag == None
                or self.currenttag == "b"
            ):
                split = split[0].strip()
                if self.allele and self.allele not in self._data[self.species]:
                    self._data[self.species][self.allele] = {}
                if self.domain not in self._data[self.species][self.allele]:
                    self._data[self.species][self.allele][self.domain] = ""

                self._data[self.species][self.allele][self.domain] += split

        # Set the prevtag variable to what it is currently; this is for sequences that are flanked by IMGT's N-linked glycosylation sites
        self.prevtag = self.currenttag
        self.prevallele = self.allele

    def rip_sequences(self, htmlstring):
        """
        Method for this subclass that automates the return of data
        """
        self.reset()
        self._data = dict()
        self.currenttag = None
        self.currentnamedent = None

        self.pre = False

        self.prevtag = None
        self.species = None
        self.allele = None
        self.prevallele = None
        self.allelename = False
        self.domain = None

        self.feed(htmlstring)

        return self._data


def cut_seq(seq, c_like=False, domain=""):
    """
    MHC sequences in IMGT are already aligned, so just use the defined columns of the given IMGT alignment
    """

    if c_like:
        seq = seq.replace(" ", "")
        seq = seq[8:122]
        if len(seq) < 114:
            seq += "-" * (114 - len(seq))
        return seq

    seq = seq.replace(" ", "")  # There's a gap between 49.7 and 50
    seq = seq[10:116]  # Get sequences 1 - 92 with insertions

    # CD1/MR1 sequences are shorter
    if domain in ["GA1L", "MR1"]:
        if len(seq) < 99:
            seq += "-" * (99 - len(seq))
        elif len(seq) >= 99:
            seq = seq[:99]

    elif domain in ["GA2L", "MR2"]:
        if len(seq) < 102:
            seq += "-" * (102 - len(seq))
        else:
            seq = seq[:102]
    else:
        # If we have a shorter sequence, then fill it with gaps in the end
        if len(seq) < 106:
            seq += "-" * (106 - len(seq))
        else:
            seq = seq[:106]

    return seq


def parse_mhc_data(data_dir):
    # Set up an MHC Parser
    parser = MHCParser()

    # Parse sequences
    print("Obtaining sequences...")
    print(data_dir)
    parser.rip_sequences(
        open(
            os.path.join(data_dir, "IMGT_sequence_files/htmlfiles/domaindisplay.html")
        ).read()
    )
    # parser.rip_sequences(open("/home/quast/Projects/STCRDab/ANARCI/build_pipeline/IMGT_sequence_files/htmlfiles/domaindisplay.html").read())

    ### Convert alleles into the 2010 scheme -- comment this out if we want to stick to IMGT's old annotation scheme.
    ### This file was obtained from ftp://ftp.ebi.ac.uk/pub/databases/imgt/mhc/hla/Nomenclature_2009.txt
    # names = open('nomenclature_2009.txt')
    # names.readline() # skip the header
    # allele_conversion = dict([ l.split() for l in names ])
    ###

    # Write FASTA files and stockholm files thereafter
    print("Parsing FASTA, STOCKHOLM, and allele files...")

    # mhc_alleles is a dictionary that will be used for ANARCI to trace alleles back from the protein sequence
    mhc_alleles = {}

    # Iterate through sepecies
    for sp in parser._data:

        translated = species[sp]
        common_name = common[sp]

        # dom_length = {"GA1": 0, "GA2": 0, "GA": 0, "GB": 0}
        dom_length = {
            "GA1": 0,
            "GA2": 0,
            "GA": 106,
            "GB": 0,
        }  # hack to deal with weird domain name issue
        # Remember that B2M is a C-LIKE domain
        domain_name = {
            "GA1": "G-ALPHA1",
            "GA2": "G-ALPHA2",
            "GA": "G-ALPHA",
            "GB": "G-BETA",
            "B2M": "C-LIKE",
            "GA1L": "G-ALPHA1-LIKE",
            "GA2L": "G-ALPHA2-LIKE",
            "MR1": "G-ALPHA1-LIKE",
            "MR2": "G-ALPHA2-LIKE",
        }

        # The parser._data dictionary is indexed by the full domain name (e.g. GA = G-ALPHA)
        # when we shorten this down to write stockholm alignments, we'll use the short form, GA
        for dom in ("GA", "GB", "GA1", "GA2", "B2M", "GA1L", "GA2L", "MR1", "MR2"):

            if dom not in mhc_alleles:
                mhc_alleles[dom] = {}

            # Acqure pad length based on name, domain and allele
            pad_length = (
                max([len(translated + "_XXX_" + allele) for allele in parser._data[sp]])
                + 1
            )
            mhc_alleles[dom][common_name] = {}
            domain = domain_name[dom]

            if dom == "B2M":
                clike = True
            else:
                clike = False

            # Iterate through alleles and write to fasta and sto files
            for allele in parser._data[sp]:
                if domain not in parser._data[sp][allele]:
                    continue

                # Bit of a hack for MR1/CD1 sequences...
                if dom == "MR1" and "CD1" in allele:
                    continue
                elif dom == "GA1L" and "MR1" in allele:
                    continue
                elif dom == "MR2" and "CD1" in allele:
                    continue
                elif dom == "GA2L" and "MR1" in allele:
                    continue

                seq = parser._data[sp][allele][domain]
                # For C-LIKE domains, we should only use B2 microglobulin because this is in a separate chain.
                if dom == "B2M" and "B2M" not in allele:
                    continue

                myseq = cut_seq(seq, c_like=clike, domain=dom)
                # For CD1 domains, IMGT sequences seem to have an X in them? ignore these.
                if "X" in myseq:
                    continue

                ### Convert if necessary, otherwise comment out if we use IMGT scheme ###
                # if common_name == "human" and allele.split("-")[1] in allele_conversion:
                #    allele = "HLA-" + allele_conversion[allele.split("-")[1]]
                ###

                # Store information of allele in mhc_alleles dictionary
                if allele not in mhc_alleles[dom][common_name]:
                    mhc_alleles[dom][common_name][allele] = ""

                mhc_alleles[dom][common_name][allele] += myseq.replace(".", "-")
                dom_length[dom] = len(myseq)

    # Clean up MHC alleles since there's lots of duplicates
    sk_g1_human = sorted(mhc_alleles["GA1"]["human"].keys())
    sk_g2_human = sorted(mhc_alleles["GA2"]["human"].keys())
    sk_g1_mouse = sorted(mhc_alleles["GA1"]["mouse"].keys())
    sk_g2_mouse = sorted(mhc_alleles["GA2"]["mouse"].keys())

    sk_g_human = set(sk_g1_human) & set(sk_g2_human)
    sk_g_mouse = set(sk_g1_mouse) & set(sk_g2_mouse)

    dicts = [
        mhc_alleles["GA1"]["human"],
        mhc_alleles["GA2"]["human"],
        mhc_alleles["GA1"]["mouse"],
        mhc_alleles["GA2"]["mouse"],
    ]
    for i, alleleset in enumerate([sk_g_human, sk_g_human, sk_g_mouse, sk_g_mouse]):
        tmp = {}
        for allele in alleleset:
            if dicts[i][allele] not in tmp:
                tmp[allele] = dicts[i][allele]
        dicts[i] = dict([(v, k) for k, v in list(tmp.items())])

    # Open fasta and sto files
    mhc_data_dir = os.path.join(data_dir, "curated_alignments", "mhcalignments")
    os.makedirs(mhc_data_dir, exist_ok=True)
    for common_name in ["human", "mouse"]:
        for dom in ["B2M", "GA1L", "GA2L", "MR1", "MR2", "GA", "GB", "GA1", "GA2"]:
            if len(mhc_alleles[dom][common_name]) == 0:
                continue
            fasta = open(
                os.path.join(mhc_data_dir, "%s_%s.fasta" % (common_name, dom)), "w"
            )
            sto = open(
                os.path.join(mhc_data_dir, "%s_%s.sto" % (common_name, dom)), "w"
            )

            print("# STOCKHOLM 1.0\n#=GF ID %s_%s" % (common_name, dom), file=sto)

            for allele in mhc_alleles[dom][common_name]:
                myseq = mhc_alleles[dom][common_name][allele]
                print(">%s|%s" % (allele, dom), file=fasta)
                print(myseq, file=fasta)
                print(
                    (common_name + "_" + dom + "_" + allele).ljust(pad_length),
                    myseq.replace(".", "-").replace(":", "-"),
                    file=sto,
                )

            # Print the end of the STOCKHOLM ALIGNMENT file
            print("#=GC RF".ljust(pad_length), "x" * dom_length[dom], file=sto)
            print("//", file=sto)

            fasta.close()
            sto.close()

    # Serialise the dictionary to a python file that can be imported in ANARCI.
    with open(
        os.path.join(data_dir, "curated_alignments/mhc_alleles.py"), "w"
    ) as mhcout:
        print("mhc_alleles = " + repr(mhc_alleles), file=mhcout)

    # Combine all .sto files
    with open(os.path.join(mhc_data_dir, "ALLMHC.sto"), "w") as outfile:
        for filename in os.listdir(mhc_data_dir):
            if filename.endswith(".sto") and "ALLMHC" not in filename:
                with open(os.path.join(mhc_data_dir, filename), "r") as infile:
                    outfile.write(infile.read())

    with open(os.path.join(mhc_data_dir, "ALLMHC.sto"), "r") as infile, open(
        os.path.join(data_dir, "curated_alignments", "ALL.stockholm"), "a"
    ) as outfile:
        outfile.write(infile.read())
