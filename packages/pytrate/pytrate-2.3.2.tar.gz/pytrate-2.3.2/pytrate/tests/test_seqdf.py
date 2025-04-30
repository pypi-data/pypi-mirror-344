import numpy as np
import pandas as pd
import pytest

from pytrate import helper


class TestSeqDf:
    """
    General tests for SeqDf.
    """

    def test_df_codes_values(self, seqdf):
        """
        df_codes should contain values from 0-20 that correspond to the index in the
        aminoAcidsAndGap tuple.
        """
        assert seqdf.df_codes.loc["a", 1] == helper.aminoAcidsAndGap.index("N")

    def test_df_codes_values_gap(self):
        """
        Test a df_codes value that corresponds to a gap character.
        """
        seqdf = helper.SeqDf(
            pd.DataFrame(
                {
                    1: ["N", "N", "-", "A", "N"],
                    2: ["C", "S", "S", "C", "S"],
                    3: ["A", "A", "A", "A", "A"],
                    4: ["A", "N", "N", "A", "N"],
                },
                index="a b c d e".split(),
            )
        )
        assert seqdf.df_codes.loc["c", 1] == helper.aminoAcidsAndGap.index("-")

    def test_unrecognised_amino_acid(self):
        """
        An unrecognised amino acid should raise a ValueError.
        """
        with pytest.raises(ValueError, match=r"unrecognised amino acid\(s\): X"):
            helper.SeqDf(
                pd.DataFrame(
                    {
                        1: ["N", "N", "X", "A", "N"],
                        2: ["C", "S", "S", "C", "S"],
                        3: ["A", "A", "A", "A", "A"],
                        4: ["A", "N", "N", "A", "N"],
                    },
                    index="a b c d e".split(),
                )
            )


class TestAminoAcidSequencePairs:
    def test_containing_x(self):
        seqdf = helper.SeqDf(
            pd.DataFrame({1: ["N", "X"], 2: ["N", "X"]}, index=["a", "b"]),
            allow_unknown_aa=True,
        )
        pairs = seqdf.amino_acid_changes_sequence_pairs([("a", "b")], symmetric=True)
        assert {helper.SymmetricAminoAcidPair("N", "X")} == pairs


class TestAminoAcidMatrix:
    def test_returns_df(self, seqdf):
        assert isinstance(seqdf.amino_acid_matrix(sequence_pairs=[]), pd.DataFrame)

    def test_columns_as_expected(self, seqdf):
        matrix = seqdf.amino_acid_matrix(sequence_pairs=(("a", "b"), ("c", "d")))
        assert list(matrix.columns) == list(helper.aminoAcidsAndGap)

    def test_index_as_expected(self, seqdf):
        matrix = seqdf.amino_acid_matrix(sequence_pairs=(("a", "b"), ("c", "d")))
        assert list(matrix.index) == list(helper.aminoAcidsAndGap)

    def test_value_correct_single_pair(self, seqdf):
        """
        Single pair is passed.
        """
        matrix = seqdf.amino_acid_matrix(sequence_pairs=(("a", "b"),))
        expect = pd.DataFrame(
            np.full((21, 21), False),
            index=list(helper.aminoAcidsAndGap),
            columns=list(helper.aminoAcidsAndGap),
        )
        expect.loc["N", "N"] = True
        expect.loc["C", "S"] = True
        expect.loc["A", "A"] = True
        expect.loc["A", "N"] = True
        assert (expect == matrix).all().all()

    def test_value_correct_two_pairs(self, seqdf):
        """
        Pass two pairs.
        """
        matrix = seqdf.amino_acid_matrix(sequence_pairs=(("a", "b"), ("c", "d")))
        expect = pd.DataFrame(
            np.full((21, 21), False),
            index=list(helper.aminoAcidsAndGap),
            columns=list(helper.aminoAcidsAndGap),
        )
        # pair (a, b)
        expect.loc["N", "N"] = True
        expect.loc["C", "S"] = True
        expect.loc["A", "A"] = True
        expect.loc["A", "N"] = True

        # pair (c, d)
        expect.loc["N", "A"] = True
        expect.loc["S", "C"] = True
        expect.loc["A", "A"] = True
        expect.loc["N", "A"] = True

        assert (expect == matrix).all().all()

    def test_single_pair_single_site(self, seqdf):
        matrix = seqdf.amino_acid_matrix(sequence_pairs=[("a", "b")], sites=[1])
        expect = pd.DataFrame(
            np.full((21, 21), False),
            index=list(helper.aminoAcidsAndGap),
            columns=list(helper.aminoAcidsAndGap),
        )
        expect.loc["N", "N"] = True
        assert (expect == matrix).all().all()

    def test_single_pair_two_sites(self, seqdf):
        matrix = seqdf.amino_acid_matrix(sequence_pairs=[("a", "b")], sites=[1, 2])
        expect = pd.DataFrame(
            np.full((21, 21), False),
            index=list(helper.aminoAcidsAndGap),
            columns=list(helper.aminoAcidsAndGap),
        )
        expect.loc["N", "N"] = True
        expect.loc["C", "S"] = True
        assert (expect == matrix).all().all()

    def test_two_pairs_two_sites(self, seqdf):
        matrix = seqdf.amino_acid_matrix(
            sequence_pairs=[("a", "b"), ("c", "d")], sites=[1, 2]
        )
        expect = pd.DataFrame(
            np.full((21, 21), False),
            index=list(helper.aminoAcidsAndGap),
            columns=list(helper.aminoAcidsAndGap),
        )
        expect.loc["N", "N"] = True
        expect.loc["C", "S"] = True
        expect.loc["N", "A"] = True
        expect.loc["S", "C"] = True
        assert (expect == matrix).all().all()


class TestSiteAminoAcidCombinations:
    def test_tuples_returned(self, seqdf):
        combinations = seqdf.site_aa_combinations(
            symmetric_aa=False, sequence_pairs=[("a", "b")]
        )
        assert all(isinstance(comb, tuple) for comb in combinations)

    def test_value_single_pair_asymmetric(self, seqdf):
        combinations = seqdf.site_aa_combinations(
            symmetric_aa=False, sequence_pairs=[("a", "b")]
        )
        expect = {(1, "NN"), (2, "CS"), (3, "AA"), (4, "AN")}
        assert expect == set(combinations)

    def test_value_two_pairs_asymmetric(self, seqdf):
        combinations = seqdf.site_aa_combinations(
            symmetric_aa=False, sequence_pairs=[("a", "b"), ("c", "d")]
        )
        expect = {
            (1, "NN"),
            (2, "CS"),
            (3, "AA"),
            (4, "AN"),
            (1, "NA"),
            (2, "SC"),
            (4, "NA"),
        }
        assert expect == set(combinations)

    def test_value_two_pairs_symmetric(self, seqdf):
        combinations = seqdf.site_aa_combinations(
            symmetric_aa=True, sequence_pairs=[("a", "b"), ("c", "d")]
        )
        expect = {(1, "NN"), (1, "AN"), (2, "CS"), (3, "AA"), (4, "AN")}
        assert expect == set(combinations)

    def test_gap_present(self):
        seqdf = helper.SeqDf(
            pd.DataFrame(
                {
                    1: ["N", "N", "-", "A", "N"],
                    2: ["C", "S", "S", "C", "S"],
                    3: ["A", "A", "A", "A", "A"],
                    4: ["A", "N", "N", "A", "N"],
                },
                index="a b c d e".split(),
            )
        )
        combinations = seqdf.site_aa_combinations(
            symmetric_aa=True, sequence_pairs=[("c", "d")]
        )
        expect = {(4, "AN"), (3, "AA"), (2, "CS"), (1, "-A")}
        assert expect == set(combinations)


class TestSiteAminoAcidChangesSequencePairs:

    def test_returns_set(self, seqdf):
        output = seqdf.site_amino_acid_changes_sequence_pairs([("a", "b")])
        assert isinstance(output, set)

    def test_single_pair(self, seqdf):
        expect = {
            helper.SiteAminoAcidPair.from_str(s) for s in ("N1N", "C2S", "A3A", "A4N")
        }
        output = seqdf.site_amino_acid_changes_sequence_pairs([("a", "b")])
        assert expect == output

    def test_two_pairs(self, seqdf):
        expect = {
            helper.SiteAminoAcidPair.from_str(s)
            for s in ("N1N", "C2S", "S2C", "A3A", "A4N", "N4A")
        }
        output = seqdf.site_amino_acid_changes_sequence_pairs([("a", "b"), ("b", "a")])
        assert expect == output
