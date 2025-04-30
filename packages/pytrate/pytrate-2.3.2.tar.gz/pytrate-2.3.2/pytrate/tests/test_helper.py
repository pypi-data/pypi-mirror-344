from unittest import TestCase
import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
import xarray as xr

from pytrate import helper


class TestExpandSequences:
    def test_returns_df(self):
        series = pd.Series({"a": "NKT", "b": "NST", "c": "NTT"})
        assert isinstance(helper.expand_sequences(series), pd.DataFrame)

    def test_result_as_expected(self):
        series = pd.Series({"a": "NKT", "b": "NST", "c": "NTT"})
        expect = pd.DataFrame(
            {1: ["N", "N", "N"], 2: ["K", "S", "T"], 3: ["T", "T", "T"]},
            index=["a", "b", "c"],
        )
        assert (helper.expand_sequences(series) == expect).all().all()

    def test_index_correct(self):
        series = pd.Series({"a": "NKT", "b": "NST", "c": "NTT"})
        df = helper.expand_sequences(series)
        assert list(df.index) == ["a", "b", "c"]

    def test_columns_correct(self):
        series = pd.Series({"a": "NKT", "b": "NST", "c": "NTT"})
        df = helper.expand_sequences(series)
        assert list(df.columns) == [1, 2, 3]


class TestSiteAminoAcidPair:

    def test_unknown_site(self):
        with pytest.raises(ValueError, match="invalid literal"):
            helper.SiteAminoAcidPair("N", "xyz", "K")

    def test_unknown_aa(self):
        with pytest.raises(ValueError, match="unrecognized amino acid"):
            helper.SiteAminoAcidPair("J", 10, "K")

    def test_equivalent(self):
        assert helper.SiteAminoAcidPair("N", 145, "K") == helper.SiteAminoAcidPair(
            "N", 145, "K"
        )


class TestAsymmetricAminoAcidPair:
    def test_NN_eq_NN(self):
        """NN should equal NN."""
        assert helper.AsymmetricAminoAcidPair(
            "N", "N"
        ) == helper.AsymmetricAminoAcidPair("N", "N")

    def test_NK_not_equal_KN(self):
        """NK should not be equal to KN."""
        assert helper.AsymmetricAminoAcidPair(
            "N", "K"
        ) != helper.AsymmetricAminoAcidPair("K", "N")

    def test_str(self):
        """String should contain amino acids in the order they are passed."""
        aap = helper.AsymmetricAminoAcidPair("N", "K")
        assert str(aap) == "NK"

        aap = helper.AsymmetricAminoAcidPair("K", "N")
        assert str(aap) == "KN"


class TestSymmetricAminoAcidPair:
    def test_pair_sorted(self):
        """The pair attribute should contain the amino acids alphabetically sorted."""
        aap = helper.SymmetricAminoAcidPair("N", "K")
        assert aap.pair == ("K", "N")

        aap = helper.SymmetricAminoAcidPair("K", "N")
        assert aap.pair == ("K", "N")

    def test_str(self):
        """String should contain sorted amino acids in the pair."""
        aap = helper.SymmetricAminoAcidPair("N", "K")
        assert str(aap) == "KN"

        aap = helper.SymmetricAminoAcidPair("K", "N")
        assert str(aap) == "KN"

    def test_NN_eq_NN(self):
        """NN should equal NN."""
        assert helper.SymmetricAminoAcidPair("N", "N") == helper.SymmetricAminoAcidPair(
            "N", "N"
        )

    def test_NK_equal_KN(self):
        """NK should be equal to KN."""
        assert helper.SymmetricAminoAcidPair("N", "K") == helper.SymmetricAminoAcidPair(
            "K", "N"
        )


class TestBaseModel:
    def test_passing_dataframe_raises_value_error(self, seqdf):
        """Titers should only be allowed to be a pandas series."""
        with pytest.raises(ValueError):
            helper.ModelBase(sequences=seqdf, titers=pd.DataFrame())

    def test_has_seqdf(self):
        """Test the helper module has a SeqDf attribute."""
        assert hasattr(helper, "SeqDf")

    def test_raises_error_with_missing_seqs(self):
        """
        Test that a ValueError is raised if there is a sequence in titers that is not
        present in sequences.
        """
        sequences = pd.DataFrame(
            {
                1: ["N", "K", "S", "A"],
                2: ["N", "K", "S", "C"],
                3: ["N", "K", "S", "A"],
            },
            index="a b c d".split(),
        )
        titer_index = pd.MultiIndex.from_tuples(
            [("a", "b"), ("c", "e")], names=["antigen", "serum"]
        )
        titers = pd.Series([10, 20], index=titer_index)

        with pytest.raises(ValueError):
            helper.ModelBase(sequences=sequences, titers=titers)

    def test_covariates_different_length(self, seqdf, titers):
        """If covariates is not None and is a different length to titers, raise an error."""
        covariates = pd.DataFrame(
            np.random.randn(4, 3),
            columns=["cov1", "cov2", "cov3"],
            index=pd.MultiIndex.from_tuples(
                [("a", "b"), ("a", "c"), ("a", "d"), ("a", "e")]
            ),
        )

        msg = "covariates and titers have different length"
        with pytest.raises(ValueError, match=msg):
            helper.ModelBase(sequences=seqdf, titers=titers, covariates=covariates)

    def test_grouped_train_test_uncensored_splits(self, titer_reg_obj, subtests):
        """The uncensored train and test splits should combine to be the uncensored data."""
        for train, test in titer_reg_obj.grouped_train_test_sets(n_splits=3):
            with subtests.test():
                assert all(train.uncensored ^ test.uncensored == titer_reg_obj.u)

    def test_grouped_train_test_censored_splits(self, titer_reg_obj, subtests):
        """The censored train and test splits should combine to be the censored data."""
        for train, test in titer_reg_obj.grouped_train_test_sets(n_splits=3):
            with subtests.test():
                assert all(train.censored ^ test.censored == titer_reg_obj.c)

    def test_grouped_train_test_splits_uncensored_censored(
        self, titer_reg_obj, subtests
    ):
        """
        The logical and of all masks in a single train/test fold should be an array of
        True.
        """
        for train, test in titer_reg_obj.grouped_train_test_sets(n_splits=3):
            with subtests.test():
                combined_mask = (
                    train.censored ^ train.uncensored ^ test.censored ^ test.uncensored
                )
                expect = np.full(titer_reg_obj.n_titers, True)
                assert (combined_mask == expect).all()


class TestTiter:
    def test_titer_10(self):
        assert helper.Titer("10").log_value == 0

    def test_titer_10_int(self):
        """Should be able to pass an int."""
        assert helper.Titer(10).log_value == 0

    def test_titer_lt10(self):
        assert helper.Titer("<10").log_value == -1

    def test_titer_lt20(self):
        """The log value of <20 should be the log value of <10 +1."""
        assert helper.Titer("<20").log_value == (helper.Titer("<10").log_value + 1)

    def test_titer_lt10_leading_whitespace(self):
        assert helper.Titer(" <10").log_value == -1

    def test_titer_lt10_trailing_whitespace(self):
        assert helper.Titer("<10 ").log_value == -1

    def test_titer_lt10_central_whitespace(self):
        assert helper.Titer("< 10").log_value == -1

    def test_titer_gt10(self):
        with pytest.raises(NotImplementedError):
            assert helper.Titer(">10")

    def test_titer_40(self):
        assert helper.Titer("40").log_value == 2

    def test_intermediate_20_40(self):
        assert helper.Titer("20/40").log_value == 1.5

    def test_intermediate_40_80(self):
        assert helper.Titer("40/80").log_value == 2.5


class TestNDFactor(TestCase):

    def test_index_a_b(self):
        f = helper.NDFactor([("a", "b"), ("a", "c"), ("b", "c")])
        assert f.index(("a", "b")) == 0

    def test_index_a_c(self):
        f = helper.NDFactor([("a", "b"), ("a", "c"), ("b", "c")])
        assert f.index(("a", "c")) == 1

    def test_index_b_c(self):
        f = helper.NDFactor([("a", "b"), ("a", "c"), ("b", "c")])
        assert f.index(("b", "c")) == 2

    def test_make_index(self):
        f = helper.NDFactor([("a", "b"), ("a", "c"), ("b", "c")])
        df = pd.DataFrame([["a", "b"], ["a", "c"], ["b", "c"]])
        assert f.make_index(df) == [0, 1, 2]

    def test_labels(self):
        f = helper.NDFactor([("a", "b"), ("a", "c"), ("b", "c")])
        assert f.labels == ["a-b", "a-c", "b-c"]

    def test_labels_ints(self):
        f = helper.NDFactor([(1, 2), (1, 3), (2, 3)])
        assert f.labels == ["1-2", "1-3", "2-3"]


class TestFindGylcosylationSites(TestCase):

    def test_returns_list(self):
        """
        Should return a list of ints indicating the index of the first 'N' in the glycosylation
        motif.
        """
        assert helper.find_glycosylation_sites("ACDNNSD") == [3]

    def test_returns_empty_list(self):
        """Should return empty list if the sequence doesn't contain a glycosylation motif."""
        assert helper.find_glycosylation_sites("ACDNSD") == []

    def test_index(self):
        assert helper.find_glycosylation_sites("ACDNKSD")[0] == 3

    def test_X_is_proline(self):
        """Glycosylation motif is NX{ST}, where X is not proline."""
        assert helper.find_glycosylation_sites("ACDNPSD") == []

    def test_multiple(self):
        assert helper.find_glycosylation_sites("ANKTCGNSSP") == [1, 6]

    def test_overlapping(self):
        assert helper.find_glycosylation_sites("NNSS") == [0, 1]


class TestGlycosylationChanges(TestCase):

    def test_no_empty(self):
        assert list(helper.find_glycosylation_changes("", "")) == []

    def test_no_differences(self):
        assert list(helper.find_glycosylation_changes("AQCNKT", "AQCNKT")) == []

    def test_different_motifs(self):
        """Different motifs but at the same site."""
        assert list(helper.find_glycosylation_changes("AQCNKT", "AQCNRS")) == []

    def test_single_difference(self):
        assert len(list(helper.find_glycosylation_changes("AQCNKT", "AQCNKA"))) == 1

    def test_single_difference_site(self):
        gc = next(helper.find_glycosylation_changes("AQCNKT", "AQCNKA"))
        assert gc.site == 4

    def test_single_difference_sub(self):
        gc = next(helper.find_glycosylation_changes("AQCNKT", "AQCNKA"))
        assert gc.subs == ["T6A"]

    def test_single_difference_mut_motif(self):
        gc = next(helper.find_glycosylation_changes("AQCNKT", "AQCNKA"))
        assert gc.mut_motif == "NKA"

    def test_single_difference_root_motif(self):
        gc = next(helper.find_glycosylation_changes("AQCNKT", "AQCNKA"))
        assert gc.root_motif == "NKT"

    def test_multiple_subs_but_only_one_necessary(self):
        """K -> Q present, but only T -> necessary."""
        gc = next(helper.find_glycosylation_changes("NKT", "NQA"))
        assert gc.subs == ["T3A"]

    def test_single_difference_multiple_subs_gain_or_loss(self):
        gc = next(helper.find_glycosylation_changes("AQCNKT", "AQCNQA"))
        assert gc.gain_or_loss == "loss"


class TestSubsNecessaryForGlycChange(TestCase):

    def test_1(self):
        """Here, loss of T necessary to lose the glycosylation."""
        assert helper.subs_necessary_for_glyc_change("NKT", "NQA") == [("T", 2, "A")]

    def test_2(self):
        """
        Here both the T -> A and K -> P alone would be necessary and sufficient to result in a loss
        of glycosylation.
        """
        assert helper.subs_necessary_for_glyc_change("NKT", "NPA") == [
            ("K", 1, "P"),
            ("T", 2, "A"),
        ]

    def test_3(self):
        with pytest.raises(
            ValueError, match=r"No difference in glycosylation between NKT and NKS"
        ):
            helper.subs_necessary_for_glyc_change("NKT", "NKS")

    def test_1_reversed(self):
        assert helper.subs_necessary_for_glyc_change("NQA", "NKT") == [("A", 2, "T")]

    def test_2_reversed(self):
        """Here both subs are necessary for the gain. (Need to lose the P and gain the final T)."""
        with pytest.raises(NotImplementedError):
            helper.subs_necessary_for_glyc_change("NPA", "NKT")

    def test_3_reversed(self):
        with pytest.raises(ValueError):
            helper.subs_necessary_for_glyc_change("NKS", "NKT")

    def test_4(self):
        """Here, loss of N necessary to lose the glycosylation."""
        assert helper.subs_necessary_for_glyc_change("NKT", "AQT") == [("N", 0, "A")]

    def test_5(self):
        """Here all changes necessary."""
        with pytest.raises(NotImplementedError):
            helper.subs_necessary_for_glyc_change("APC", "NKT")

    def test_error_seqs_not_len_3(self):
        with pytest.raises(ValueError, match="sequences not len 3:"):
            helper.subs_necessary_for_glyc_change("ABCD", "NKT")


class TestFindSubstitutions(TestCase):

    def test_no_diffs(self):
        assert list(helper.find_substitutions("AKC", "AKC")) == []

    def test_one_diff(self):
        assert list(helper.find_substitutions("AKC", "ADC")) == ["K2D"]

    def test_multiple_diffs(self):
        assert list(helper.find_substitutions("AKC", "TDC")) == ["A1T", "K2D"]

    def test_diffs_at_start(self):
        assert list(helper.find_substitutions("AKC", "DKC")) == ["A1D"]

    def test_diffs_at_end(self):
        assert list(helper.find_substitutions("AKC", "AKD")) == ["C3D"]

    def test_diffs_at_start_and_end(self):
        assert list(helper.find_substitutions("AKC", "DKR")) == ["A1D", "C3R"]

    def test_glycosylation_gain(self):
        """If append_glyc_changes=True, then glycosylation gains should have '(+g)' appended."""
        subs = helper.find_substitutions("NKN", "NKT", append_glyc_changes=True)
        assert list(subs) == ["N3T+g"]

    def test_another_glycosylation_gain(self):
        """If append_glyc_changes=True, then glycosylation gains should have '(+g)' appended."""
        subs = helper.find_substitutions(
            "ABCDEFGNKNHIJK", "ABCDEFGNKSHIJR", append_glyc_changes=True
        )
        assert list(subs) == ["N10S+g", "K14R"]

    def test_glycosylation_loss(self):
        """If append_glyc_changes=True, then glycosylation losses should have '(g-)' appended."""
        subs = helper.find_substitutions("NKT", "NKN", append_glyc_changes=True)
        assert list(subs) == ["T3N-g"]

    def test_multiple_subs_necessary(self):
        """
        If multiple substitutions are necessary for the glyc change, a NotImplementedError should
        be raised.
        """
        with pytest.raises(NotImplementedError):
            list(helper.find_substitutions("AKR", "NKT", append_glyc_changes=True))

    def test_cant_pass_append_and_unify_glyc_changes(self):
        with pytest.raises(
            ValueError, match="append and unify glyc_changes can't both be True"
        ):
            list(
                helper.find_substitutions(
                    "NKT", "NKN", append_glyc_changes=True, unify_glyc_changes=True
                )
            )

    def test_unify_glyc_changes_loss(self):
        """
        Tests the behaviour of unify glyc changes.
        """
        subs = helper.find_substitutions("NKT", "NKN", unify_glyc_changes=True)
        assert list(subs) == ["1-g"]

    def test_unify_glyc_changes_loss_and_gain(self):
        """
        Test losing one glycosylation but gaining another.
        """
        subs = helper.find_substitutions(
            "GPNKTRRKS", "GPSKTRNKS", unify_glyc_changes=True
        )
        assert list(subs) == ["3-g", "7+g"]


class TestSubstitutionComponents(TestCase):

    def test_sub_components_1(self):
        assert helper.sub_components("N145K") == (145, "N", "K")

    def test_sub_components_2(self):
        assert helper.sub_components("E1N") == (1, "E", "N")

    def test_glycosylation_loss_ignored(self):
        assert helper.sub_components("N145K(g-)") == (145, "N", "K")

    def test_glycosylation_gain_ignored(self):
        assert helper.sub_components("N145T(g+)") == (145, "N", "T")


class TestHdiScatter(TestCase):

    def test_returns_tuple(self):
        """
        Test that hdi_scatter_data returns a tuple.
        """
        # make idata with 4 chains of 100 samples each
        idata = az.from_dict(posterior={"var1": np.random.randn(4, 100)})
        result = helper.hdi_scatter_data(idata, "var1")
        assert isinstance(result, tuple)

    def test_mean_is_dataarray(self):
        """
        Test that the mean returned by hdi_scatter_data is a DataArray.
        """
        idata = az.from_dict(posterior={"var1": np.random.randn(4, 100)})
        mean, _ = helper.hdi_scatter_data(idata, "var1")
        assert isinstance(mean, xr.DataArray)

    def test_hdi_err_is_ndarray(self):
        """
        Test that the hdi_err returned by hdi_scatter_data is an ndarray.
        """
        idata = az.from_dict(posterior={"var1": np.random.randn(4, 100)})
        _, hdi_err = helper.hdi_scatter_data(idata, "var1")
        assert isinstance(hdi_err, np.ndarray)

    def test_hdi_err_shape(self):
        """
        Test that the hdi_err returned by hdi_scatter_data has the correct shape.
        """
        idata = az.from_dict(posterior={"var1": np.random.randn(4, 100)})
        _, hdi_err = helper.hdi_scatter_data(idata, "var1")
        assert hdi_err.shape == (2,)

    def test_plot_hdi_scatter(self):
        """
        Test that plot_hdi_scatter creates a plot without errors.
        """
        x_idata = az.from_dict(posterior={"var1": np.random.randn(4, 100, 50)})
        y_idata = az.from_dict(posterior={"var1": np.random.randn(4, 100, 50)})
        ax = plt.gca()
        result_ax = helper.plot_hdi_scatter(x_idata, "var1", y_idata, ax=ax)
        assert result_ax is ax

    def test_hdi_scatter_data_with_xarray_dataset(self):
        """
        Test that hdi_scatter_data can handle being passed an xarray.Dataset.
        """
        data = xr.DataArray(
            np.random.randn(4, 50, 200), dims=("chain", "draw", "var1"), name="x"
        )
        mean, hdi_err = helper.hdi_scatter_data(data)
        assert isinstance(mean, xr.DataArray)
        assert isinstance(hdi_err, np.ndarray)
        assert hdi_err.shape == (2, 200)
