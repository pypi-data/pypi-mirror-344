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
