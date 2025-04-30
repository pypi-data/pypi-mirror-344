import unittest

# force import of anarci from conda env rather than local file version:
import sys
import importlib.util

spec = importlib.util.spec_from_file_location(
    "anarci",
    "/home/quast/miniconda3/envs/test_anarci_install/lib/python3.12/site-packages/anarci/__init__.py",
)
anarci = importlib.util.module_from_spec(spec)
sys.modules["anarci"] = anarci
spec.loader.exec_module(anarci)


class TestAnarciEdgecases(unittest.TestCase):
    def test_ambiguous_B2M_numbering(self):
        from anarci import number

        sequence = [
            (
                "B2M",
                "MIQRTPKIQVYSRHPANGKFLNCYVSGFHPSDIEVDKNGRIEKVEHSDLSFSKDWSFYLLYYTFTPTEKYACRVNHVTLSQPKIVKWDRD",
            )
        ]
        numbering = number(
            sequence[0][1],
            allow=set(
                [
                    "B",
                    "A",
                    "D",
                    "G",
                    "GA1",
                    "GA2",
                    "GA1L",
                    "GA2L",
                    "GA",
                    "GB",
                    "B2M",
                    "MH1",
                    "MR1",
                    "MR2",
                ]
            ),
        )

        print(numbering)
