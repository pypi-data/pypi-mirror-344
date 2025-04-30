import json
import unittest
import re


# parser fasta files to anarci python API input
def parse_fasta_to_tuples(file_path: str):
    with open(file_path, "r") as f:
        fasta_str = f.read()
    sequences = []
    entries = re.split(r"^>(.+)", fasta_str, flags=re.MULTILINE)[1:]
    for i in range(0, len(entries), 2):
        header = entries[i].strip()
        sequence = entries[i + 1].replace("\n", "").strip()
        sequences.append((header, sequence))
    return sequences


# convert all nested tuples to lists:
def tuple_to_list(d):
    if isinstance(d, tuple):
        return list(map(tuple_to_list, d))
    elif isinstance(d, list):
        return list(map(tuple_to_list, d))
    else:
        return d


def assert_germlines(val_germlines, germlines):
    """
    Compare germlines in the validation file with the output from ANARCI.
    """
    if val_germlines is None and germlines is None:
        return True
    assert list(val_germlines.keys()) == list(germlines.keys())
    for key in val_germlines.keys():

        assert val_germlines[key] == tuple_to_list(germlines[key])
    return True


class TestAnarcriOutput(unittest.TestCase):
    def test_anarci_output(self):
        from anarci import anarci

        FASTA_FILES = [
            "./test_files/ig_test_seqs.fa",
            "./test_files/tcr_test_seqs.fa",
            "./test_files/8rro_mhc_class_i.fa",
            "./test_files/9b7b_mhc_class_ii.fa",
        ]
        VAL_FILES = [
            "./validation_files/ig_seqs_out.json",
            "./validation_files/tcr_seqs_out.json",
            "./validation_files/8rro_mhc_class_i_out.json",
            "./validation_files/9b7b_mhc_class_ii_out.json",
        ]

        for fasta_file, val_file in zip(FASTA_FILES, VAL_FILES):
            with open(val_file, "r") as f:
                val_data = json.load(f)
            sequences = parse_fasta_to_tuples(fasta_file)
            results = anarci(sequences, scheme="imgt", assign_germline=True)
            results = tuple_to_list(results)  # because json loads as lists not tuples
            numbering, alignment_details, hit_tables = results
            val_numbering, val_alignment_details, val_hit_tables = val_data

            for i, _ in enumerate(numbering):
                assert numbering[i] == val_numbering[i]
                if val_alignment_details[i] is not None:
                    assert all(
                        [
                            (
                                (
                                    val_alignment_details[i][0][k]
                                    == alignment_details[i][0][k]
                                    if k != "germlines"
                                    else assert_germlines(
                                        val_alignment_details[i][0][k],
                                        alignment_details[i][0][k],
                                    )
                                )
                            )
                            for k in val_alignment_details[i][0].keys()
                        ]
                    )
                else:
                    assert alignment_details[i] is None
                assert hit_tables[i] == val_hit_tables[i]
