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


class TestAnarci(unittest.TestCase):

    def test_anarci_import(self):
        from anarci import anarci

    def test_example_sequences(self):
        sequences = [
            (
                "12e8:H",
                "EVQLQQSGAEVVRSGASVKLSCTASGFNIKDYYIHWVKQRPEKGLEWIGWIDPEIGDTEYVPKFQGKATMTADTSSNTAYLQLSSLTSEDTAVYYCNAGHDYDRGRFPYWGQGTLVTVSAAKTTPPSVYPLAP",
            ),
            (
                "12e8:L",
                "DIVMTQSQKFMSTSVGDRVSITCKASQNVGTAVAWYQQKPGQSPKLMIYSASNRYTGVPDRFTGSGSGTDFTLTISNMQSEDLADYFCQQYSSYPLTFGAGTKLELKRADAAPTVSIFPPSSEQLTSGGASV",
            ),
            (
                "scfv:A",
                "DIQMTQSPSSLSASVGDRVTITCRTSGNIHNYLTWYQQKPGKAPQLLIYNAKTLADGVPSRFSGSGSGTQFTLTISSLQPEDFANYYCQHFWSLPFTFGQGTKVEIKRTGGGGSGGGGSGGGGSGGGGSEVQLVESGGGLVQPGGSLRLSCAASGFDFSRYDMSWVRQAPGKRLEWVAYISSGGGSTYFPDTVKGRFTISRDNAKNTLYLQMNSLRAEDTAVYYCARQNKKLTWFDYWGQGTLVTVSSHHHHHH",
            ),
            (
                "lysozyme:A",
                "KVFGRCELAAAMKRHGLDNYRGYSLGNWVCAAKFESNFNTQATNRNTDGSTDYGILQINSRWWCNDGRTPGSRNLCNIPCSALLSSDITASVNCAKKIVSDGNGMNAWVAWRNRCKGTDVQAWIRGCRL",
            ),
            (
                "HLA:A",
                "GSHSMRYFYTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDRNTRNVKAQSQTDRVDLGTLRGYYNQSEAGSHTIQMMYGCDVGSDGRFLRGYRQDAYDGKDYIALKEDLRSWTAADMAAQTTKHKWEAAHVAEQWRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQK",
            ),
            (
                "B2M:A",
                "IQRTPKIQVYSRHPAENGKSNFLNCYVSGFHPSDIEVDLLKNGERIEKVEHSDLSFSKDWSFYLLYYTEFTPTEKDEYACRVNHVTLSQPKIVKWDRDM",
            ),
            (
                "HLA-DR",
                "EEHVIIQAEFYLNPDQSGEFMFDFDGDEIFHVDMAKKETVWRLEEFGRFASFEAQGALANIAVDKANLEIMTKRSNYTPITNVPPEVTVLTNSPVELREPNVLICFIDKFTPPVVNVTWLRNGKPVTTGVSETVFLPREDHLFRKFHYLPFLPSTEDVYDCRVEHWGLDEPLLKHWEF",
            ),
        ]

        results = anarci.anarci(sequences, scheme="imgt", output=False)

        numbering, alignment_details, hit_tables = results
        print(alignment_details)
        assert (
            len(numbering)
            == len(alignment_details)
            == len(hit_tables)
            == len(sequences)
        )

    def test_MR1_numbering_case(self):
        from anarci import number

        sequence = [
            (
                "MR1",
                "MRTHSLRYFRLGVSDPIHGVPEFISVGYVDSHPITTYDSVTRQKEPRAPWMAENLAPDHWERYTQLLRGWQQMFKVELKRLQRHYNHSGSHTYQRMIGCELLEDGSTTGFLQYAYDGQDFLIFNKDTLSWLAVDNVAHTIKQAWEANQHELLYQKNWLEEECIAWLKRFLEYGKDTLQRTEPPLVRVNRKETFPGVTALFCKAHGFYPPEIYMTWMKNGEEIVQEIDYGDILPSGDGTYQAWASIELLYSCHVEHSGVHMVLQV",
            )
        ]
        numbering = anarci.number(
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

    def test_assign_germline(self):
        sequences = [
            (
                "12e8:H",
                "EVQLQQSGAEVVRSGASVKLSCTASGFNIKDYYIHWVKQRPEKGLEWIGWIDPEIGDTEYVPKFQGKATMTADTSSNTAYLQLSSLTSEDTAVYYCNAGHDYDRGRFPYWGQGTLVTVSAAKTTPPSVYPLAP",
            ),
            (
                "12e8:L",
                "DIVMTQSQKFMSTSVGDRVSITCKASQNVGTAVAWYQQKPGQSPKLMIYSASNRYTGVPDRFTGSGSGTDFTLTISNMQSEDLADYFCQQYSSYPLTFGAGTKLELKRADAAPTVSIFPPSSEQLTSGGASV",
            ),
            (
                "scfv:A",
                "DIQMTQSPSSLSASVGDRVTITCRTSGNIHNYLTWYQQKPGKAPQLLIYNAKTLADGVPSRFSGSGSGTQFTLTISSLQPEDFANYYCQHFWSLPFTFGQGTKVEIKRTGGGGSGGGGSGGGGSGGGGSEVQLVESGGGLVQPGGSLRLSCAASGFDFSRYDMSWVRQAPGKRLEWVAYISSGGGSTYFPDTVKGRFTISRDNAKNTLYLQMNSLRAEDTAVYYCARQNKKLTWFDYWGQGTLVTVSSHHHHHH",
            ),
            (
                "lysozyme:A",
                "KVFGRCELAAAMKRHGLDNYRGYSLGNWVCAAKFESNFNTQATNRNTDGSTDYGILQINSRWWCNDGRTPGSRNLCNIPCSALLSSDITASVNCAKKIVSDGNGMNAWVAWRNRCKGTDVQAWIRGCRL",
            ),
            (
                "HLA:A",
                "GSHSMRYFYTSVSRPGRGEPRFIAVGYVDDTQFVRFDSDAASQRMEPRAPWIEQEGPEYWDRNTRNVKAQSQTDRVDLGTLRGYYNQSEAGSHTIQMMYGCDVGSDGRFLRGYRQDAYDGKDYIALKEDLRSWTAADMAAQTTKHKWEAAHVAEQWRAYLEGTCVEWLRRYLENGKETLQRTDAPKTHMTHHAVSDHEATLRCWALSFYPAEITLTWQRDGEDQTQDTELVETRPAGDGTFQK",
            ),
            (
                "B2M:A",
                "IQRTPKIQVYSRHPAENGKSNFLNCYVSGFHPSDIEVDLLKNGERIEKVEHSDLSFSKDWSFYLLYYTEFTPTEKDEYACRVNHVTLSQPKIVKWDRDM",
            ),
            (
                "HLA-DR",
                "EEHVIIQAEFYLNPDQSGEFMFDFDGDEIFHVDMAKKETVWRLEEFGRFASFEAQGALANIAVDKANLEIMTKRSNYTPITNVPPEVTVLTNSPVELREPNVLICFIDKFTPPVVNVTWLRNGKPVTTGVSETVFLPREDHLFRKFHYLPFLPSTEDVYDCRVEHWGLDEPLLKHWEF",
            ),
        ]

        results = anarci.anarci(sequences, scheme="imgt", assign_germline=True)
