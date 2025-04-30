# from ..constants import data_path
from .download_data import download_data
from .parse_mhc_data import parse_mhc_data
from .format_alignments import format_alignments

import os, shutil, site, subprocess
import pyhmmer
from tempfile import TemporaryDirectory

ANARCI_LOC = os.path.join(site.getsitepackages()[0], "anarci")
DATA_PATH = os.path.join(ANARCI_LOC, "dat/HMMs")
ANARCI_SRC_LOC = os.path.join(site.getsitepackages()[0], "anarci/anarci")


def run_hmmer(in_path, out_path):
    alphabet = pyhmmer.easel.Alphabet.amino()
    print("Loading MSA from {}".format(in_path))
    with pyhmmer.easel.MSAFile(in_path, digital=True, alphabet=alphabet) as msa_file:
        msas = list(msa_file)

    builder = pyhmmer.plan7.Builder(alphabet, architecture="hand")
    background = pyhmmer.plan7.Background(alphabet)

    print("Building HMMs from {} MSAs".format(len(msas)))
    hmms = []
    with open(out_path, "wb") as output_file:
        for msa in msas:
            hmm, _, _ = builder.build_msa(msa, background)
            hmm.write(output_file)
            hmms.append(hmm)
    print("Pressing HMMs")
    pyhmmer.hmmpress(hmms, out_path)
    print("Saved HMMs to {}".format(out_path))


def build_models():
    """
    Download germline data from IMGT and build HMM models.
    Intermediate files are written to a temporary directory; final HMMs and germline data will be copied to install location before cleanup.
    """

    with TemporaryDirectory() as temp_dir:
        # Create subdirectories
        html_dir = os.path.join(temp_dir, "IMGT_sequence_files", "htmlfiles")
        fasta_dir = os.path.join(temp_dir, "IMGT_sequence_files", "fastafiles")
        curated_dir = os.path.join(temp_dir, "curated_alignments")
        hmm_dir = os.path.join(temp_dir, "HMMs")

        os.makedirs(html_dir, exist_ok=True)
        os.makedirs(fasta_dir, exist_ok=True)
        os.makedirs(
            os.path.join(curated_dir, "muscle_alignments"), exist_ok=True
        )  # Need an extra subdirectory here
        os.makedirs(hmm_dir, exist_ok=True)

        try:

            # Download data and prepare alignment files

            print("Downloading data from IMGT.")

            download_data(html_dir, fasta_dir)

            format_alignments(fasta_dir, curated_dir)

            parse_mhc_data(temp_dir)

            # Build HMMs using pyhmmer

            print("Building HMMs.")

            run_hmmer(
                os.path.join(curated_dir, "ALL.stockholm"),
                os.path.join(hmm_dir, "ALL.hmm"),
            )

        except Exception as e:
            print(f"Error during build process: {e}\nRetrieving backup models.")
            import urllib.request
            import warnings

            filenames = [
                "ALL.hmm.h3f",
                "ALL.hmm.h3i",
                "ALL.hmm.h3m",
                "ALL.hmm.h3p",
                "germlines.py",
                "mhc_alleles.py",
            ]
            for fn in filenames:
                url = f"https://github.com/npqst/anarci-backup-models/raw/refs/heads/main/{fn}"
                destination = (
                    os.path.join(curated_dir, fn)
                    if fn.endswith(".py")
                    else os.path.join(hmm_dir, fn)
                )
                urllib.request.urlretrieve(url, destination)
            warnings.warn(
                "Error downloading and building anarci models. Backup models have been downloaded. This may effect the licence."
            )

        # Copy HMMs and germlines to ANARCI install location
        shutil.copytree(os.path.join(hmm_dir), DATA_PATH, dirs_exist_ok=True)
        shutil.copy(os.path.join(curated_dir, "germlines.py"), ANARCI_SRC_LOC)
        shutil.copy(os.path.join(curated_dir, "mhc_alleles.py"), ANARCI_SRC_LOC)

        print(f"HMMs copied from {os.path.join(hmm_dir)} to {DATA_PATH}")
        print(
            f"Germlines copied from {os.path.join(curated_dir, 'germlines.py')} to: {ANARCI_SRC_LOC}"
        )
        print(
            f"MHC alleles copied from {os.path.join(curated_dir, 'mhc_alleles.py')} to: {ANARCI_SRC_LOC}"
        )

    print("Finished building HMMs.")
