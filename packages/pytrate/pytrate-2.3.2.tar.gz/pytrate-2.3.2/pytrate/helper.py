import logging
import re
import reprlib
from abc import ABC
from collections import namedtuple, defaultdict
from functools import cached_property, lru_cache
from itertools import product, chain, combinations
from pathlib import Path
from typing import Callable, Generator, Iterable, Literal, Optional, Iterator, Any

import arviz as az
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm
import xarray as xr
from adjustText import adjust_text
from Bio import SeqIO
from pandas.api.types import CategoricalDtype
from scipy import odr
from scipy.stats import pearsonr
from sklearn.model_selection import GroupKFold

try:
    import nutpie
except ImportError:
    logging.warning("nutpie not installed")


"""
1 letter amino acid codes, sorted by biophysical property.
"""
aminoAcidsByProperty = (
    # Hydrophobic
    "W",
    "Y",
    "F",
    "M",
    "L",
    "I",
    "V",
    "A",
    # Special
    "P",
    "G",
    "C",
    # Polar uncharged
    "Q",
    "N",
    "T",
    "S",
    # Charged (-)
    "E",
    "D",
    # Charged (+)
    "H",
    "K",
    "R",
)

"""
1 letter amino acid codes, sorted alphabetically.
"""
aminoAcids = (
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
)

"""
1 letter amino acid codes, sorted alphabetically, including a gap character.
"""
aminoAcidsAndGap = (
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
    "-",
)

"""
1 letter amino acid codes, sorted alphabetically, including gap and unknown amino acid
character.
"""
aminoAcidsAndGapAndUnknown = (
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
    "X",
    "-",
)


_KNOWN_AMINO_ACIDS = frozenset(aminoAcidsAndGapAndUnknown)

normal_lcdf = pm.distributions.dist_math.normal_lcdf
UncensoredCensoredTuple = namedtuple(
    "UncensoredCensoredTuple", ("uncensored", "censored", "combined")
)
TrainTestTuple = namedtuple("TrainTestTuple", ("train", "test"))


def string_to_series(string: str) -> pd.Series:
    """
    Expand characters in a string to individual items in a series.
    """
    return pd.Series(list(string))


def expand_sequences(series: pd.Series) -> pd.DataFrame:
    """
    Expand Series containing sequences into DataFrame.

    Notes:
        Any elements in series that cannot be expanded will be dropped.

    Args:
        series (pd.Series)

    Returns:
        pd.DataFrame: Columns are sequence sites, indexes match
            series.index.
    """
    df = series.apply(string_to_series)
    df.columns = list(range(df.shape[1]))
    df.columns += 1
    return df[df.notnull().all(axis=1)]


def df_from_fasta(path: str, sites: Optional[list[int]] = None) -> pd.DataFrame:
    """
    Read a fasta file.

    Args:
        path: Path to fasta file.
        sites: Optional 1-indexed list of sites to include.

    Returns:
        DataFrame. Indexes are record IDs in upper case, columns are sites.
    """
    with open(path, "r") as handle:
        data = {record.id: record.seq for record in SeqIO.parse(handle, "fasta")}

    df = pd.DataFrame.from_dict(data, orient="index")
    df.columns = list(range(1, df.shape[1] + 1))

    if sites is not None:
        df = df[list(sites)]

    return df


def test_known_aa(aa: str) -> None:
    """
    Test if a string is a known amino acid.
    """
    if aa not in _KNOWN_AMINO_ACIDS:
        raise ValueError(f"unrecognized amino acid: {aa}")


class GlycosylationChange:

    def __init__(
        self,
        gain_or_loss: Literal["gain", "loss"],
        site: int,
        subs: list[str],
        root_motif: str,
        mut_motif: str,
    ):
        self.gain_or_loss = gain_or_loss
        self.site = site
        self.subs = subs
        self.root_motif = root_motif
        self.mut_motif = mut_motif
        try:
            self.sign = {"gain": "+", "loss": "-"}[self.gain_or_loss]
        except KeyError:
            raise ValueError("gain_or_loss must be 'gain' or 'loss'")

    def __str__(self) -> str:
        return f"{self.site}{self.sign}g"

    def __eq__(self, other) -> bool:
        """
        Glycosylation changes are equivalent if they occur at the same site and are both losses /
        gains.
        """
        return (self.site == other.site) and (self.gain_or_loss == other.gain_or_loss)


@lru_cache
class SiteAminoAcidPair:
    def __init__(self, a: str, site: int, b: str) -> None:
        """
        A pair of amino acids and a site.

        Args:
            a,b: Amino acids
            site: Site
        """
        for item in a, b:
            test_known_aa(item)

        self.a = a
        self.b = b
        self.site = int(site)

        self.items = self.a, self.site, self.b

    def __repr__(self) -> str:
        return f"{self.a}{self.site}{self.b}"

    @staticmethod
    def from_str(string: str) -> "SiteAminoAcidPair":
        a, site, b = re.match(r"(\w{1})(\d)(\w{1})", string).groups()
        return SiteAminoAcidPair(a, site, b)

    def __str__(self) -> str:
        return f"{self.a}{self.site}{self.b}"

    def __eq__(self, other: "SiteAminoAcidPair") -> bool:
        return self.items == other.items

    def __hash__(self) -> int:
        return hash(self.items)


class AminoAcidPair(ABC):
    """
    A pair of amino acids.
    """

    def __init__(self, a: str, b: str) -> None:
        for item in a, b:
            test_known_aa(item)

    def __str__(self) -> str:
        return "".join(self.pair)

    def __eq__(self, other: "AminoAcidPair") -> bool:
        return self.pair == other.pair

    def __getitem__(self, item: int) -> str:
        return self.pair[item]

    def __hash__(self) -> int:
        return hash(self.pair)


@lru_cache
class SymmetricAminoAcidPair(AminoAcidPair):
    """
    A pair of amino acids. Symmetric means that it doesn't matter which order a and b are
    supplied in. I.e. NK == KN.
    """

    def __init__(self, a: str, b: str) -> None:
        super().__init__(a, b)
        self.pair = tuple(sorted((a, b)))

    def __repr__(self) -> str:
        return f"SymmetricAminoAcidPair({self.pair})"


@lru_cache
class AsymmetricAminoAcidPair(AminoAcidPair):
    """
    A pair of amino acids. Asymmetric means that the order of a and b matters, so NK !=
    KN.
    """

    def __init__(self, a: str, b: str) -> None:
        super().__init__(a, b)
        self.pair = a, b

    def __repr__(self) -> str:
        return f"AsymmetricAminoAcidPair({self.pair})"


class SeqDf:
    def __init__(self, df: pd.DataFrame, allow_unknown_aa: bool = False) -> None:
        """
        DataFrame containing amino acid sequences.

        Args:
            df: Columns are amino acid sites, rows are antigens or sera, cells
                contain amino acids.
            allow_unknown_aa: Allow unknown amino acids, represented by an `'X'` character.
        """
        self.characters = (
            aminoAcidsAndGapAndUnknown if allow_unknown_aa else aminoAcidsAndGap
        )
        self._unknown_aa_allowed = allow_unknown_aa

        if unknown_aa := set(np.unique(df.values)) - set(self.characters):
            if not allow_unknown_aa:
                raise ValueError(f"unrecognised amino acid(s): {', '.join(unknown_aa)}")

        self.df = df

        # Categorical DataFrame and codes
        self.df_cat = df.astype(CategoricalDtype(list(self.characters), ordered=False))
        self.df_codes = pd.DataFrame(
            {site: self.df_cat[site].cat.codes for site in self.df_cat}
        )

    def __repr__(self) -> None:
        return f"SeqDf(df={reprlib.repr(self.df)})"

    def __str__(self) -> None:
        return str(self.df)

    @classmethod
    def from_fasta(
        cls,
        path: str,
        sites: Optional[list[int]] = None,
        allow_unknown_aa: bool = False,
    ) -> "SeqDf":
        """Make a SeqDf from a fasta file.

        Args:
            path: Path to fasta file.
            sites: Optional 1-indexed sites to include.
            allow_unknown_aa: Allow unknown amino acids, represented by an 'X' character.

        Returns:
            SeqDf
        """
        return cls(
            df_from_fasta(path=path, sites=sites),
            allow_unknown_aa=allow_unknown_aa,
        )

    @classmethod
    def from_series(cls, series: pd.Series, allow_unknown_aa: bool = False) -> "SeqDf":
        """Make SeqDf from a series.

        Args:
            series (pd.Series): Each element in series is a string. See
                mapdeduce.helper.expand_sequences for more details.
            allow_unknown_aa: Allow unknown amino acids, represented by an 'X' character.

        Returns:
            (SeqDf)
        """
        return cls(expand_sequences(series), allow_unknown_aa=allow_unknown_aa)

    def remove_invariant(self) -> "SeqDf":
        """
        Remove sites (columns) that contain only one amino acid.
        """
        mask = self.df.apply(lambda x: pd.unique(x).shape[0] > 1)
        n = (~mask).sum()
        logging.info(f"removed {n} invariant sequence sites")
        new = self.df.loc[:, self.df.columns[mask]]
        return SeqDf(new, allow_unknown_aa=self._unknown_aa_allowed)

    def keep_sites(self, sites: list[int]) -> "SeqDf":
        """
        Keep only a subset of sites.
        """
        return SeqDf(self.df.loc[:, sites], allow_unknown_aa=self._unknown_aa_allowed)

    def amino_acid_changes_sequence_pairs(
        self, sequence_pairs: Iterable[tuple[str, str]], symmetric: bool
    ) -> set[AminoAcidPair]:
        """
        All amino acid changes that occur between pairs of sequences.

        Args:
            sequence_pairs: Pairs of sequence names.
            symmetric: If True, AB considered the same as BA. SymmetricAminoAcidPair
                instances are returned.
        """
        aa_idx = np.argwhere(self.amino_acid_matrix(sequence_pairs).values)
        Aa = SymmetricAminoAcidPair if symmetric else AsymmetricAminoAcidPair
        return set(Aa(self.characters[i], self.characters[j]) for i, j in aa_idx)

    def site_amino_acid_changes_sequence_pairs(
        self, sequence_pairs: Iterable[tuple[str, str]]
    ) -> set[SiteAminoAcidPair]:
        """
        All site - amino acid pairs that occur between pairs of sequences.

        Args:
            sequence_pairs: Pairs of sequence names.

        Implementation note:
            Slow but clean...
        """
        return set(
            SiteAminoAcidPair(self.df.loc[a, site], site, self.df.loc[b, site])
            for site in self.df.columns
            for a, b in set(sequence_pairs)
        )

    def amino_acid_matrix(
        self,
        sequence_pairs: Iterable[tuple[str, str]],
        sites: Optional[list[int]] = None,
        names: tuple[str, str] = ("antigen", "serum"),
    ) -> pd.DataFrame:
        """
        Generate an amino acid matrix based on the given sequence pairs.

        Args:
            sequence_pairs (Iterable[tuple[str, str]]): A collection of sequence pairs,
                where each pair consists of an antigen sequence and a serum sequence.
            sites (Optional[list[int]], optional): A list of sites to consider in
                the matrix. If None, all sites in the sequence pairs will be
                considered. Defaults to None.
            names (tuple[str, str], optional): A tuple of names for the antigen and serum
                sequences. Defaults to ("antigen", "serum").

        Returns:
            pd.DataFrame: A DataFrame representing the amino acid matrix, where each row
            and column corresponds to an amino acid and the values indicate whether the
            amino acids at the corresponding sites in the sequence pairs are found in
            the data.
        """

        aa = np.full((len(self.characters), len(self.characters)), False)

        sites = list(self.df_codes) if sites is None else sites
        df_codes = self.df_codes[sites]

        for pair in sequence_pairs:
            if len(pair) != 2:
                raise ValueError(f"sequence_pairs must contain pairs, found: {pair}")

            idx = df_codes.loc[list(pair)].values
            # (2x faster not to call np.unique(idx))
            aa[idx[0], idx[1]] = True

        return pd.DataFrame(
            aa,
            index=pd.Index(self.characters, name=f"{names[0]}_aa"),
            columns=pd.Index(self.characters, name=f"{names[1]}_aa"),
        )

    def site_aa_combinations(
        self, symmetric_aa: bool, sequence_pairs: Iterator[tuple[str, str]]
    ) -> Generator[tuple[int, tuple[str, str]], None, None]:
        """
        Generate combinations of amino acid pairs for each site in the dataset.

        Args:
            symmetric_aa (bool): Flag indicating whether to use symmetric amino acid pairs.
            sequence_pairs (Iterator[tuple[str, str]]): Iterator of sequence pairs.

        Yields:
            tuple[int, tuple[str, str]]: A tuple containing the site and amino acid
            pair.
        """
        Aa = SymmetricAminoAcidPair if symmetric_aa else AsymmetricAminoAcidPair
        for site in self.df:
            aa_mat = self.amino_acid_matrix(sequence_pairs=sequence_pairs, sites=[site])
            for a, b in self.amino_acid_matrix_to_pairs(aa_mat):
                yield site, str(Aa(a, b))

    @staticmethod
    def amino_acid_matrix_to_pairs(aa_mat: pd.DataFrame) -> Iterator[tuple[str, str]]:
        """
        Converts an amino acid matrix into pairs of amino acids.

        Args:
            aa_mat (pd.DataFrame): The amino acid matrix.

        Returns:
            Iterator[tuple[str, str]]: An iterator of pairs of amino acids.

        """
        row_aa_idx, col_aa_idx = np.where(aa_mat)
        return zip(aa_mat.index[row_aa_idx], aa_mat.index[col_aa_idx])


def plot_forest_sorted(
    data: az.InferenceData | xr.DataArray,
    var_name: str,
    dim: str = None,
    tail: Optional[int] = None,
    head: Optional[int] = None,
    ax: mpl.axes.Axes = None,
    **kwds,
) -> mpl.axes.Axes:
    """
    Plot parameters of an inference data object sorted by their median value.

    Args:
        data: Any object that can be converted to arviz.InferenceData.
        var_name: The variable to plot.
        **kwds: Passed to arviz.plot_forest
    """
    ax = plt.gca() if ax is None else ax

    post = az.extract(data)
    median = post[var_name].median(dim="sample")
    sorted_param = post[var_name].sortby(median)

    if tail is not None and head is not None:
        raise ValueError("at least one of head and tail must be None")
    elif tail is not None:
        sorted_param = sorted_param[:tail]
    elif head is not None:
        sorted_param = sorted_param[len(sorted_param) - head :]

    non_sample_dims = set(post[var_name].dims) - {"sample"}
    if len(non_sample_dims) == 1:
        (dim,) = non_sample_dims
    else:
        raise ValueError("multiple dims present, pass a dim for labelling")

    az.plot_forest(
        data,
        var_names=var_name,
        coords={dim: sorted_param[dim]},
        combined=True,
        ax=ax,
        **kwds,
    )

    return ax


def plot_aa_matrix(
    idata: az.InferenceData,
    ax: Optional[mpl.axes.Axes] = None,
    force_upper_left: bool = False,
    vmin: float = -3.0,
    vmax: float = 3.0,
    include_unknown_aa: bool = False,
) -> tuple[mpl.axes.Axes, mpl.cm.ScalarMappable]:
    """
    Show the amino acid parameters as a matrix.

    Args:
        idata: Inference data containing b_aa variable.
        ax: Plot on this axes.
        force_upper_left: Push all the coloured squares in to the upper left corner of
            the plot. (Implementation note: this would happen by default if amino acids
            were sorted by their site in the aminoAcidsByProperty tuple, rather than
            alphabetically when amino acid pairs get defined in
            CrossedSiteAaModel.aa_uniq.)
        v{min,max}: Set the boundary of the colormap.
        include_unknown_aa: Include 'X' as an amino acid.
    """
    aas = list(reversed(aminoAcidsByProperty))
    if include_unknown_aa:
        aas.append("X")
    aas.append("-")

    post = az.extract(idata)
    b_aa_med = post["b_aa"].mean("sample").to_dataframe().squeeze()

    norm = mpl.colors.Normalize(vmin, vmax)
    mappable = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.RdBu)

    ax = plt.gca() if ax is None else ax

    seen = set()

    rect_kwds = dict(width=1.0, height=1.0, clip_on=False)

    for aa_pair, _b_aa in b_aa_med.items():

        if (aa_pair[0] == "X" or aa_pair[1] == "X") and not include_unknown_aa:
            continue

        j, i = aas.index(aa_pair[0]), aas.index(aa_pair[1])

        if force_upper_left:
            i, j = sorted((i, j))
            if (i, j) in seen:
                raise ValueError(
                    "forcing values in upper left would over write (maybe you are using "
                    "force_upper_left with asymmetric amino acids)"
                )

        congruence = j == i
        ax.add_artist(
            mpl.patches.Rectangle(
                (i, j),
                facecolor=mpl.cm.RdBu(norm(_b_aa)),
                lw=0.5 if congruence else 0,
                zorder=15 if congruence else 10,
                edgecolor="black",
                **rect_kwds,
            )
        )
        seen.add((i, j))

    for ij in product(range(len(aas)), range(len(aas))):
        if ij not in seen:
            ax.add_artist(
                mpl.patches.Rectangle(ij, facecolor="lightgrey", zorder=5, **rect_kwds)
            )

    lim = 0, len(aas)
    ticks = np.arange(0.5, len(aas) + 0.5)
    ax.set(
        xlim=lim,
        ylim=lim,
        aspect=1,
        xticks=ticks,
        yticks=ticks,
        xticklabels=aas,
        yticklabels=aas,
    )
    ax.grid(False, "major", "both")

    kwds = dict(c="white", zorder=12)
    for x in 3, 5, 9, 12, 17, 20:
        ax.axvline(x, **kwds)
        ax.axhline(x, **kwds)

    return ax, mappable


def plot_aa_matrix_error_bars(
    idata: az.InferenceData,
    ax: Optional[mpl.axes.Axes] = None,
    include_unknown_aa: bool = False,
):
    if ax is None:
        _, ax = plt.subplots(figsize=(5, 5))

    post = az.extract(idata)

    hdi = az.hdi(idata)

    aa_terms = post["aa"]

    aas = list(reversed(aminoAcidsByProperty))
    if include_unknown_aa:
        aas.append("X")
    aas.append("-")

    half_y_range = max(abs(hdi["b_aa"].min()), hdi["b_aa"].max())
    y_range = (half_y_range * 2).values
    yticks = np.arange(len(aas)) * y_range
    xticks = np.arange(len(aas))

    norm = mpl.colors.Normalize(vmin=-half_y_range, vmax=half_y_range)

    def plot_errorbar(x: float, y: float, hdi: tuple[float, float], c: str, **kwds):
        ax.plot((x, x), hdi, c=c, zorder=10, solid_capstyle="butt", **kwds)
        ax.plot(
            (x, x),
            (y - 0.05, y + 0.05),
            c="black",
            zorder=15,
            solid_capstyle="butt",
            **kwds,
        )

    for y, aa_y in zip(yticks, aas):
        for x, aa_x in enumerate(aas):
            if aa_y != aa_x:
                # Small bar for each term that's present
                terms = aa_y + aa_x, aa_x + aa_y  # E.g. "XY", "YX"
                for term, xoffset in zip(terms, (-0.25, 0.25)):
                    if term in aa_terms:
                        mean = post["b_aa"].sel(aa=term).mean()
                        plot_errorbar(
                            x=x + xoffset,
                            y=mean + y,
                            hdi=hdi["b_aa"].sel(aa=term) + y,
                            c=mpl.cm.RdBu(norm(mean)),
                            lw=6,
                        )

            else:
                # Single wider bar for matching amino acids
                term = aa_y + aa_x
                if term in aa_terms:
                    mean = post["b_aa"].sel(aa=term).mean()
                    plot_errorbar(
                        x=x,
                        y=mean + y,
                        hdi=hdi["b_aa"].sel(aa=term) + y,
                        c=mpl.cm.RdBu(norm(mean)),
                        lw=12,
                    )

                # Grey box surrounding matching amino acids
                ax.add_artist(
                    mpl.patches.Rectangle(
                        xy=(x - 0.5, y - half_y_range),
                        width=1,
                        height=y_range,
                        facecolor="darkgrey",
                        edgecolor=None,
                        zorder=5,
                        clip_on=False,
                        linewidth=0.5,
                    ),
                )

    ax.set_facecolor("lightgrey")
    ax.grid(False, axis="both", which="both")
    kwds = dict(c="white", lw=0.5, zorder=6)
    for ytick in yticks:
        ax.axhline(ytick - half_y_range, **kwds)
        ax.axhline(ytick, c="darkgrey", lw=0.25, linestyle="--")
    for xtick in xticks:
        ax.axvline(xtick - 0.5, **kwds)

    # Thicker lines to demark amino acid groups
    kwds = dict(c="white", zorder=12)
    for x in 3, 5, 9, 12, 17, 20:
        ax.axvline(x - 0.5, **kwds)
        ax.axhline(x * y_range - half_y_range, **kwds)

    plt.yticks(yticks, aas)
    plt.xticks(xticks, aas)
    plt.xlim(-0.5, len(aas) - 0.5)
    plt.ylim(-half_y_range, yticks[-1] + half_y_range)


def hdi_scatter_data(
    data: az.InferenceData | xr.DataArray,
    varname: Optional[str] = None,
    hdi_prob: float = 0.95,
    sort: Optional[Literal["ascending", "descending"]] = None,
    sortby: Literal["mean", "lower", "higher"] = "mean",
    head: Optional[int] = None,
    tail: Optional[int] = None,
) -> tuple[xr.DataArray, np.ndarray]:
    """
    Calculate mean and HDI error bars for a variable in an InferenceData object.

    Args:
        idata: az.InferenceData. InferenceData object to extract from.
        varname: str. Name of the variable to extract. Required if data is az.InferenceData.
        hdi_prob: float, optional. Probability to use for the HDI calculation (default=0.95).
        sort: str, optional. If 'ascending' or 'descending', sort the values by their mean.
        sortby: str. How should values be sorted? 'lower' and 'upper' refer to the lower and upper
            bounds of the HDI. Only relevant is sort is not None.
        head: int, optional. Show only this many of the highest values.
        tail: int, optional. Show only this many of the lowest values.

    Returns:
        2-tuple containing:
            mean: xr.DataArray. Mean of the variable.
            hdi_err: np.ndarray. Shape (2, len(variable)) containing the HDI error bars
                as (lower, upper).
    """
    if isinstance(data, az.InferenceData):
        hdi = az.hdi(data, hdi_prob=hdi_prob)[varname]
        mean = az.extract(data)[varname].mean("sample")

    else:
        hdi = az.hdi(data, hdi_prob=hdi_prob)[data.name]

        try:
            mean = data.mean("sample")
        except ValueError:
            mean = data.stack({"sample": ["chain", "draw"]}).mean("sample")

    if sort is not None:

        # Get values to sort by
        if sortby == "mean":
            values = mean
        elif sortby == "lower":
            values = hdi.sel(hdi="lower")
        elif sortby == "higher":
            values = hdi.sel(hdi="higher")
        else:
            raise ValueError("sortby should be one of 'mean', 'lower', 'higher'")

        # Get index that sorts
        if sort == "ascending":
            idx = np.argsort(values).values

        elif sort == "descending":
            idx = np.argsort(-values).values

        else:
            raise ValueError("sort must be 'ascending' or 'descending'")

        if head is not None and tail is not None:
            raise ValueError("pass either head or tail, not both")

        elif head is not None:
            if sort == "ascending":
                idx = idx[-head:]
            elif sort == "descending":
                idx = idx[:head]

        elif tail is not None:
            if sort == "ascending":
                idx = idx[:tail]
            elif sort == "descending":
                idx = idx[-tail:]

        mean = mean[idx]
        hdi = hdi.isel(site=idx)

    return mean, np.stack([(mean - hdi[..., 0]).values, (hdi[..., 1] - mean.values)])


def plot_hdi_scatter(
    y_data: az.InferenceData | xr.DataArray,
    var_name: Optional[str] = None,
    x_data: Optional[az.InferenceData | xr.DataArray] = None,
    var_name_x: Optional[str] = None,
    ax: Optional[mpl.axes.Axes] = None,
    highlight_site: Optional[int] = None,
    highlight_kwds: Optional[dict[str, Any]] = None,
    hdi_as_area: bool = False,
    area_kwds: Optional[dict] = None,
    xtick_skip: Optional[int] = None,
    data_kwds: Optional[dict] = None,
    **kwds,
) -> mpl.axes.Axes:
    """
    Plot two variables in an InferenceData object against each other, using HDI error bars.

    Args:
        y_data: az.InferenceData or xr.DataArray. The y data to plot.
        var_name: str. Name of the variable to plot. Must be passed for az.InferenceData objects.
        x_data: az.InferenceData or xr.DataArray. The x data to plot. If not provided, then
            y data is plotted with uniformly spaced x data.
        var_name_x: str. Name of the variable to plot on the x-axis (if different from var_name).
        ax: Optional[mpl.axes.Axes], optional. Axes to plot on. If None, a new figure
            is created (default).
        highlight_site: int, optional. If provided, highlight this site in red.
        highlight_kwds: dict, optional. Passed to plt.scatter for the highlighted point.
        hdi_as_area: bool. Plot the width of the HDIs as an area rather than individual lines. Only
            applies when x_data is None. Only applies when x_data is not provided.
        area_kwds: dict. Passed to axes.Axes.fill_between.
        xtick_skip: Use this to add xticklabels if only y_data is passed. This integer defines how
            frequently to plot xticks. I.e. set to 1 to show all xticklabels, or 10 to show every
            tenth, say.
        data_kwds: dict, optional. Passed to `hdi_scatter_data`. Keys include `hdi_prob`, `sort`,
            `sortby`, `head`, `tail`. See `hdi_scatter_data` for more details.
        **kwds: Passed to ax.errorbar.

    Returns:
        mpl.axes.Axes
    """
    # Data
    data_kwds = {} if data_kwds is None else data_kwds
    y, yerr = hdi_scatter_data(y_data, var_name, **data_kwds)
    x, xerr = (
        (xr.DataArray(np.arange(len(y)), coords=dict(site=y.coords["site"])), None)
        if x_data is None
        else hdi_scatter_data(x_data, var_name_x or var_name, **data_kwds)
    )

    # Plotting
    ax = ax or plt.gca()

    if hdi_as_area:
        if x_data is not None:
            raise ValueError("hdi_as_area only applies when x_data not provided")

        area_defaults = dict(color="lightgrey", linewidth=0, zorder=5)
        area_kwds = area_kwds or {}
        ax.fill_between(
            x, y1=y - yerr[0], y2=y + yerr[1], **{**area_defaults, **area_kwds}
        )
        ax.plot(x, y, c="black", lw=0.5, zorder=10)

    else:
        errorbar_defaults = dict(
            c="black",
            ecolor="grey",
            elinewidth=0.75,
            fmt="o",
            markeredgecolor="white",
            zorder=10,
        )
        ax.errorbar(x, y, yerr, xerr, **{**errorbar_defaults, **kwds})

    highlight_defaults = dict(fc="red", s=50, zorder=15)
    highlight_kwds = {**highlight_defaults, **(highlight_kwds or {})}

    if highlight_site is not None:
        if isinstance(highlight_site, int):
            highlight_site = (highlight_site,)

        highlight_site = list(set(highlight_site) & set(y.coords["site"].values))

        ax.scatter(
            x.sel(site=highlight_site), y.sel(site=highlight_site), **highlight_kwds
        )

    if x_data is None and xtick_skip is not None:
        ticks = x[::xtick_skip]
        labels = y.coords["site"].values[::xtick_skip]
        ax.set_xticks(ticks, labels)

    return ax


class CrossValidationFoldResult:
    def __init__(
        self,
        idata: az.InferenceData,
        y_true: np.ndarray,
        train: UncensoredCensoredTuple,
        test: UncensoredCensoredTuple,
    ) -> None:
        """
        The results of a single train/test cross validation fold.

        Args:
            idata: The inference data object. Should have a `posterior_predictive`
                attribute.
            y_true: Measured responses of the test set.
            train: Tuple of masks used to define training data.
            test: Tuple of masks used to define testing data.
        """
        self.idata = idata
        self.y_pred = (
            idata.posterior_predictive["obs_u"].mean(dim="draw").mean(dim="chain")
        )
        self.y_true = y_true
        self.err = (self.y_pred - self.y_true).values
        self.err_abs = np.absolute(self.err)
        self.err_sqr = self.err**2
        self.mean_err_sqr = np.mean(self.err_sqr)
        self.mean_err_abs = np.mean(self.err_abs)
        self.train = train
        self.test = test

    def __repr__(self) -> str:
        return f"CrossValidationFoldResult({self.idata})"

    def __str__(self) -> str:
        return (
            f"mean squared error: {self.mean_err_sqr}\n"
            f"mean absolute error: {self.mean_err_abs}"
        )

    def plot_predicted_titers(
        self, ax=None, jitter: float = 0.2, ylabel: str = "Predicted log titer"
    ) -> None:
        """
        Plot predicted vs true log titer values.

        Args:
            ax: Matplotlib ax.
            jitter: Size of jitter to add to x-axis values.
            ylabel: Y-axis label.
        """
        ax = plt.gca() if ax is None else ax
        jitter = np.random.uniform(-jitter / 2, jitter / 2, len(self.y_true))
        ax.scatter(
            self.y_true + jitter,
            self.y_pred,
            lw=0.5,
            clip_on=False,
            s=15,
            edgecolor="white",
        )
        ax.set(
            aspect=1,
            xlabel="True log titer",
            ylabel=ylabel,
            xticks=np.arange(0, 10, 2),
            yticks=np.arange(0, 10, 2),
        )
        ax.axline((0, 0), slope=1, c="lightgrey", zorder=0)


class CrossValidationResults:
    def __init__(self, results: Iterable[CrossValidationFoldResult]) -> None:
        self.results = tuple(results)

    @property
    def df_error(self) -> pd.DataFrame:
        """
        DataFrame containing absolute error, squared error, raw error for each predicted
        titer in each fold.
        """
        return pd.concat(
            [
                pd.DataFrame(
                    {
                        "absolute_error": self.results[i].err_abs,
                        "squared_error": self.results[i].err_sqr,
                        "raw_error": self.results[i].err,
                    }
                ).assign(fold=i)
                for i in range(len(self.results))
            ]
        )

    def plot_predicted_titers(
        self, figsize: tuple[float, float] = (15.0, 10.0)
    ) -> np.ndarray:
        _, axes = plt.subplots(
            ncols=len(self.results), sharex=True, sharey=True, figsize=figsize
        )
        for result, ax in zip(self.results, axes):
            result.plot_predicted_titers(ax=ax, ylabel="Predicted log titer")
            ax.text(
                0,
                1,
                f"Mean abs. err={result.mean_err_abs:.2f}",
                transform=ax.transAxes,
                va="top",
                fontsize=8,
            )
            ax.label_outer()
        return axes


class ModelBase(ABC):
    def __init__(
        self,
        sequences: pd.DataFrame | SeqDf,
        titers: pd.Series,
        covariates: Optional[pd.DataFrame] = None,
        allow_unknown_aa: bool = False,
    ) -> None:
        """
        Data and methods that are shared by CrossedSiteAaModel and
        CombinedSiteAaModel.

        Args:
            sequences:
            titers:
            covariates:
            allow_unknown_aa: Only has an effect if sequences is a DataFrame such that a
                new SeqDf instance gets generated.
        """
        try:
            self.seqdf = sequences.remove_invariant()
        except AttributeError:
            self.seqdf = SeqDf(
                sequences, allow_unknown_aa=allow_unknown_aa
            ).remove_invariant()

        self.titers = pd.Series(titers, dtype=str)
        self.n_titers = self.titers.shape[0]
        self.n_sites = self.seqdf.df.shape[1]

        # Check have all sequences for antigens and sera in titers
        antigens = self.titers.index.get_level_values("antigen")
        sera = self.titers.index.get_level_values("serum")
        for virus in *antigens, *sera:
            if virus not in self.seqdf.df.index:
                raise ValueError(f"{virus} not in sequences")

        self.Y = np.array([Titer(t).log_value for t in self.titers])

        # Titer table contains <10 and <20 values
        self.c = self.titers.str.contains("<").values  # 'c'ensored
        self.u = ~self.c  # 'u'ncensored

        # Add 0.5 to the censored values
        # For censored titers it is known that the true log value must be below half way
        # to the next highest titer (this is what using normal_lcdf achieves).
        # E.g. a titer of '10' has a log value of 0. A titer of '<10' has a log_value of
        # -1. But we know that the true log value must be below half way between -1 and
        # 0, i.e. less than -0.5.
        self.Y[self.c] += 0.5

        # Keep track of the order of antigens and sera
        self.ags, self.srs = [
            pd.Categorical(self.titers.index.get_level_values(level))
            for level in ("antigen", "serum")
        ]

        # Covariates
        if covariates is not None:
            if len(self.titers) != len(covariates):
                raise ValueError("covariates and titers have different length")

            elif not (self.titers.index == covariates.index).all():
                raise ValueError("covariates and titers must have identical indexes")

            else:
                self.covs = covariates.values
                self.cov_names = list(covariates.columns)

        else:
            self.covs = None

    def __repr__(self):
        return (
            f"ModelBase(sequences={self.seqdf}, titers={self.titers}, "
            f"covariates={self.covs})"
        )

    @property
    def titer_summary(self) -> pd.DataFrame:
        """
        Summarise what titers are in the dataset, what their log values are, whether they
        are censored/uncensored and their count.
        """
        return (
            pd.DataFrame(
                set(zip(self.Y, self.titers, self.c, self.u)),
                columns=["log_titer", "titer", "censored", "uncensored"],
            )
            .sort_values("log_titer")
            .set_index("titer")
            .join(self.titers.value_counts())
            .reset_index()
        )

    @classmethod
    def from_chart(cls, chart: "maps.Chart", sites: list[int]) -> "ModelBase":
        """
        Make an instance from a maps.Chart object.

        Args:
            chart:
            sites: Only include these sites in the regression.
        """
        ag_seqs = {ag.name: list(ag.sequence) for ag in chart.antigens}
        sr_seqs = {sr.name: list(sr.sequence) for sr in chart.sera}

        df_seq = pd.DataFrame.from_dict({**ag_seqs, **sr_seqs}, orient="index")
        df_seq.columns += 1

        df_seq = df_seq[sites]

        return cls(sequences=df_seq, titers=chart.table_long)

    @cached_property
    def uncensored_model(self) -> pm.Model:
        """
        Treat all data as uncensored.

        This was implemented in order to generate a posterior predictive for the censored
        data. For censored data the posterior predictive is computed as if the data
        were uncensored. I.e., it's only the likelihood (that uses the censored response)
        that requires special handling.
        """
        with pm.Model(coords=self.coords) as model:
            variables = self.make_variables()
            sigma = pm.Exponential("sd", 1)
            mu = self.calculate_titer(suffix="u", mask=None, **variables)
            Y_u = pm.Data("Y_u", self.Y)
            pm.Normal("obs_u", mu=mu, sigma=sigma, observed=Y_u)

        return model

    def fit(self, netcdf_path: Optional[str] = None, **kwds) -> az.InferenceData:
        """
        Fit the model using variational inference.

        Args:
            netcdf_path: Path to save inference data NetCDF object. Attempt to load a
                file with this name before sampling.
            **kwds: Passed to pymc.fit
        """
        try:
            return az.from_netcdf(netcdf_path)
        except (FileNotFoundError, TypeError):
            with self.model:
                mean_field = pm.fit(
                    n=kwds.pop("n", 100_000),
                    callbacks=[
                        pm.callbacks.CheckParametersConvergence(
                            diff="absolute", tolerance=0.01
                        )
                    ],
                    **kwds,
                )

            idata = mean_field.sample(1_000)
            idata.attrs["mean_field_hist"] = mean_field.hist
            if netcdf_path is not None:
                az.to_netcdf(idata, netcdf_path)
            return idata

    def sample(
        self, netcdf_path: Optional[str] = None, use_nutpie: bool = False, **kwds
    ) -> az.InferenceData:
        """
        Sample from the model posterior.

        Args:
            netcdf_path: Path to save inference data NetCDF object. Attempt to load a
                file with this name before sampling.
            use_nutpie: Use nutpie NUTS implementation.
            **kwds: Passed to pymc.sample or nutpie.sample.
        """
        try:
            idata = az.from_netcdf(netcdf_path)
            logging.info(f"inference data loaded from {netcdf_path}")

        except (FileNotFoundError, TypeError):

            if use_nutpie:
                logging.info("sampling using nutpie...")
                compiled = nutpie.compile_pymc_model(self.model)
                idata = nutpie.sample(compiled, **kwds)

            else:
                logging.info("sampling using pymc...")
                with self.model:
                    idata = pm.sample(**kwds)

            if isinstance(netcdf_path, str):
                try:
                    # wrap this in a try / except so that idata is _always_ returned
                    az.to_netcdf(idata, netcdf_path)
                    logging.info(f"inference data saved to {netcdf_path}")

                except (FileNotFoundError, TypeError):
                    logging.warning(f"couldn't save netcdf file to {netcdf_path}")

        # Drop redundant variables from non-centered parametrisations and that contain
        # log probabilities.
        return delete_unused_variables(idata)

    @cached_property
    def model(self) -> pm.Model:
        with pm.Model(coords=self.coords) as model:
            variables = self.make_variables()
            sigma = pm.Exponential("sd", 1.0)

            # Censored data (less than titers)
            Y_c = pm.Data("Y_c", self.Y[self.c])
            mu_c = self.calculate_titer(suffix="c", mask=self.c, **variables)

            # using pm.Censored here causes loss to be nan when calling pm.fit
            pm.Potential("obs_c", normal_lcdf(mu=mu_c, sigma=sigma, x=Y_c))

            # Uncensored data (numeric titers)
            Y_u = pm.Data("Y_u", self.Y[self.u])
            mu_u = self.calculate_titer(suffix="u", mask=self.u, **variables)
            pm.Normal("obs_u", mu=mu_u, sigma=sigma, observed=Y_u)

        return model

    def data_shape(self, model: pm.Model) -> dict[str, tuple]:
        """shapes of data currently set on a model."""
        shapes = {}
        for suffix in "u", "c":
            for variable in "site_aa", "aa", "ags", "srs", "Y":
                key = f"{variable}_{suffix}"
                if key in model:
                    shapes[key] = self.model[key].eval().shape
        return shapes

    def log_data_shape(self, model: pm.Model) -> None:
        """Log shapes of data currently set on a model."""
        logging.info(f"current data shapes: {self.data_shape(model)}")

    def grouped_cross_validation(
        self,
        n_splits: int,
        variational_inference: bool = False,
        netcdf_prefix: Optional[str] = None,
        vi_kwds: Optional[dict] = None,
        sample_kwds: Optional[dict] = None,
    ) -> CrossValidationResults:
        """
        Run cross validation.

        Args:
            n_splits: Number of train/test folds to generate.
            variational_inference: Fit using variational inference rather than sampling
                from a posterior.
            netcdf_prefix: Save an InferenceData object for each fold to disk with this
                prefix. Prefixes have "-fold{i}.nc" appended where 'i' indexes the fold.
                If files already exist then load them instead of sampling.
            vi_kwds: Keyword arguments passed to pymc.fit if variational inference is
                being used.
            sample_kwds: Keyword arguments passed to pymc.sample if variational inference
                is not being used.
        """
        folds = self.grouped_train_test_sets(n_splits=n_splits)

        vi_kwds = {} if vi_kwds is None else vi_kwds
        sample_kwds = {} if sample_kwds is None else sample_kwds

        results = []

        for i, (train, test) in enumerate(folds):
            netcdf_path = f"{netcdf_prefix}-fold{i}.nc"
            with self.model:
                logging.info(
                    "setting training data "
                    f"#uncensored={sum(train.uncensored)} "
                    f"#censored={sum(train.censored)}"
                )
                self.set_data(train.censored, suffix="c")
                self.set_data(train.uncensored, suffix="u")
                self.log_data_shape(self.model)
                idata = (
                    self.fit(netcdf_path=netcdf_path, **vi_kwds)
                    if variational_inference
                    else self.sample(netcdf_path=netcdf_path, **sample_kwds)
                )

            # Generate posterior predictive samples on the test data
            with self.uncensored_model:
                logging.info(
                    "setting testing data (all test data treated as uncensored) "
                    f"#combined={sum(test.combined)} "
                )
                # self.set_data(np.zeros_like(test.combined, dtype=bool), suffix="c")
                self.set_data(test.combined, suffix="u")
                self.log_data_shape(self.uncensored_model)
                idata.extend(pm.sample_posterior_predictive(idata, progressbar=False))

            results.append(
                CrossValidationFoldResult(
                    idata, y_true=self.Y[test.combined], train=train, test=test
                )
            )

        return CrossValidationResults(results)

    def make_train_test_sets(
        self, random_seed: int, test_proportion: float = 0.1
    ) -> None:
        """
        Attach boolean arrays to this instance that define train and test sets for censored and
        uncensored data.

        Args:
            random_seed: Passed to np.random.seed for repeatable datasets.
            test_proportion: Proportion of titers used for the test set.

        The following attributes are attached:
            `mask_test`,`mask_train`: Boolean ndarrays. All titers are either in mask_test or
                mask_train.
            `mask_train_c`,`mask_train_u`: Boolean ndarrays. Censored (c) and uncensored (u)
                titers for the training set. All titers in the training set are in one of
                these arrays.
            `mask_test_c`,`mask_test_u`: Boolean ndarrays. Censored (c) and uncensored (u)
                titers for the test set. All titers in the test set are in one of these
                arrays.
        """
        if not 0 < test_proportion < 1:
            raise ValueError("test_proportion should be between 0-1.")

        np.random.seed(random_seed)

        n_test = int(np.round(test_proportion * self.n_titers))
        idx_test = np.random.choice(
            np.arange(self.n_titers), replace=False, size=n_test
        )
        self.mask_test = np.repeat(False, self.n_titers)
        self.mask_test[idx_test] = True
        self.mask_train = ~self.mask_test

        self.mask_train_u, self.mask_train_c, *_ = self.make_censored_uncensored_masks(
            self.mask_train
        )

        self.mask_test_u, self.mask_test_c, *_ = self.make_censored_uncensored_masks(
            self.mask_test
        )

    def grouped_train_test_sets(self, n_splits: int) -> Generator[
        TrainTestTuple[UncensoredCensoredTuple, UncensoredCensoredTuple],
        None,
        None,
    ]:
        """
        Generate train and test sets of uncensored and censored arrays. The titers are
        grouped by the serum/antigen pair used such that all titers from a single
        serum/antigen pair will appear in the same train or test split. I.e. testing will
        never involve testing a titer that has also appeared in the training set.

        Arrays are boolean masks the same length as the number of titers in the dataset.

        sklearn.model_selection.GroupKFold is used which is deterministic and therefore
        does not require setting a random seed to generate repeatable folds.

        Args:
            n_splits: Number of folds.

        Returns:
            4-tuple containing: (uncensored training, censored training, uncensored testing,
             censored testing).
        """
        gkf = GroupKFold(n_splits=n_splits)
        for train, test in gkf.split(range(self.n_titers), groups=self.titers.index):
            mask_train = self.indexes_to_mask(train)
            mask_test = self.indexes_to_mask(test)
            yield TrainTestTuple(
                train=self.make_censored_uncensored_masks(mask_train),
                test=self.make_censored_uncensored_masks(mask_test),
            )

    def make_censored_uncensored_masks(
        self, mask: np.ndarray
    ) -> UncensoredCensoredTuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Given a boolean mask return the same mask but decomposed into censored and
        uncensored titers.

        Args:
            mask: 1D array containing True and False.

        Returns:
            3-tuple of boolean masks:
                - uncensored
                - censored
                - combination (the logical 'or' of censored and uncensored, also equal to
                  the input mask)
        """
        if len(mask) != self.n_titers:
            raise ValueError(
                f"mask length different to n. titers ({len(mask)} vs {self.n_titers})"
            )
        if any(set(mask) - {True, False}):
            raise ValueError("mask must only contain True and False")
        if mask.ndim != 1:
            raise ValueError("mask must be 1D")

        uncensored = np.logical_and(self.u, mask)
        censored = np.logical_and(self.c, mask)
        combined = np.logical_or(uncensored, censored)

        assert all(combined == mask)

        return UncensoredCensoredTuple(
            uncensored=uncensored, censored=censored, combined=combined
        )

    def indexes_to_mask(self, indexes: np.ndarray) -> np.ndarray:
        """
        Convert an array containing integer indexes to boolean masks.

        If indexes contains [2, 4, 6] and there are 9 titers in the dataset, this would
        return: [False, False, True, False, True, False, True, False, False, False].

        Args:
            indexes: Array of integers.
        """
        mask = np.full(self.n_titers, False)
        mask[indexes] = True
        return mask


def geom_mean(a: float | int, b: float | int) -> float:
    """
    Calculate the geometric mean of two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        float: The geometric mean of a and b.
    """
    return np.sqrt(a * b)


def noncentered_normal(*args, **kwargs) -> None:
    raise NameError(
        "this function is now pytrate.helper.hierarchical_noncentered_normal"
    )


def hierarchical_noncentered_normal(
    name: str,
    dims: str,
    hyper_mu: float = 0.0,
    hyper_sigma: float = 0.5,
    hyper_lam: float = 2.0,
    lognormal: bool = False,
) -> "pytensor.tensor.TensorVariable":
    """
    Construct a non-center parametrised hierarchical normal distribution. Equivalent to:

        mu = Normal('name'_mu, hyper_mu, hyper_sigma)
        sigma = Exponential('name'_sigma, hyper_lam)
        Normal(name, mu, sigma, dims=dims)

    Args:
        name: Variable name.
        dims: Dimensions of the model for the variable.
        hyper_{mu,sigma,lam}: Hyperpriors.
        lognormal: Make this a lognormal variable.
    """
    mu = pm.Normal(f"{name}_mu", mu=hyper_mu, sigma=hyper_sigma)
    sigma = pm.Exponential(f"{name}_sigma", lam=hyper_lam)
    z = pm.Normal(f"_{name}_z", mu=0.0, sigma=1.0, dims=dims)
    return (
        pm.Deterministic(name, np.exp(z * sigma + mu), dims=dims)
        if lognormal
        else pm.Deterministic(name, z * sigma + mu, dims=dims)
    )


def hierarchical_normal(
    name: str,
    dims: str,
    hyper_mu: float = 0.0,
    hyper_sigma: float = 0.5,
    hyper_lam: float = 2.0,
) -> "pytensor.tensor.TensorVariable":
    """
    Hierarchical normal distribution. Equivalent to:

        mu = Normal(`name`_mu, hyper_mu, hyper_sigma)
        sigma = Exponential(`name`_sigma, hyper_lam)
        Normal(name, mu, sigma, dims=dims)

    See also `pytrate.hierarchical_noncentered_normal`.

    Args:
        name: Variable name.
        dims: Dimensions of the model for the variable.
        hyper_{mu,sigma,lam}: Hyperpriors.
    """
    mu = pm.Normal(f"{name}_mu", mu=hyper_mu, sigma=hyper_sigma)
    sigma = pm.Exponential(f"{name}_sigma", lam=hyper_lam)
    return pm.Normal(name, mu=mu, sigma=sigma, dims=dims)


class NDFactor:
    """
    Multi-dimensional factors.
    """

    def __init__(self, values: list[tuple]):

        self.values = tuple(sorted(set(values)))
        self._indexes = dict((value, i) for i, value in enumerate(self.values))
        self.labels = ["-".join(map(str, items)) for items in self.values]

    def __repr__(self) -> str:
        return f"Factor({self.values})"

    def __len__(self):
        return len(self.values)

    def make_index(self, df: pd.DataFrame) -> list[int]:
        """
        Returns the index for each row in the given DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame for which to generate indices.

        Returns:
            list[int]: A list of indices corresponding to each row in the DataFrame.
        """

        return [self.index(tuple(row)) for row in df.values]

    def index(self, value) -> int:
        return self._indexes[value]


def merge_maximal_subgroup_subs(ag_subs: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    Finds maximal subgroups of antigens based on their unique substitutions.

    Args:
        ag_subs (dict[str, list[str]]): A dictionary mapping antigen IDs to lists of substitutions.

    Returns:
        dict[str, list[str]]: A dictionary mapping antigen IDs to lists of maximal subgroups of
        substitutions. Each maximal subgroup is represented as a string joined by '+' characters.
        The subgroups are sorted lexicographically based on the components of each substitution.
    """

    maximal_subsets = find_maximal_subsets(ag_subs.values())

    d = defaultdict(list)

    for ag, subs in ag_subs.items():

        unique_subs = set(subs)

        # Loop through all maximal subsets, if the maximal subset is present in this antigens unique
        # substitutions, then add this maximal subset to this antigen.
        for maximal_subset in maximal_subsets:
            if maximal_subset.issubset(unique_subs):
                d[ag].append(
                    "+".join(
                        sorted(
                            maximal_subset,
                            key=lambda x: int(re.search(r"(\d+)", x).groups()[0]),
                        )
                    )
                )

    return {k: sorted(v) for k, v in d.items()}


def find_maximal_subsets(sets: list[set]) -> set[frozenset]:
    """
    Find the maximal subsets of items that always appear together in a group of sets.

    Args:
        sets (list[set]): Group of sets.
        max_combinations (Optional[int]): The maximum number of combinations of items to check.

    Returns:
        set[frozenset]: A set of frozensets representing the maximal subsets of items that always
            appear together.
    """
    # Step 1: Create a dictionary to map each item to the sets it appears in
    item_to_sets = defaultdict(set)
    for i, s in enumerate(sets):
        for item in s:
            item_to_sets[item].add(i)

    # Step 2: Identify all possible combinations of items and track their occurrences
    comb_to_sets = defaultdict(set)

    for s in sets:
        for size in range(2, len(s) + 1):
            for comb in combinations(s, size):
                comb_set = frozenset(comb)
                for i, s2 in enumerate(sets):
                    if comb_set.issubset(s2):
                        comb_to_sets[comb_set].add(i)

    # Step 3: Identify maximal sets of items that always appear together
    valid_subsets = set()
    for comb, indices in comb_to_sets.items():
        if all(item_to_sets[item] == indices for item in comb):
            valid_subsets.add(comb)

    # Step 4: Filter out subsets that are part of larger valid subsets
    maximal_subsets = set(valid_subsets)
    for subset in valid_subsets:
        for larger_subset in valid_subsets:
            if subset != larger_subset and subset.issubset(larger_subset):
                maximal_subsets.discard(subset)

    # Step 5: Add singletons that are not part of any valid subset
    all_items_in_subsets = set(chain.from_iterable(maximal_subsets))
    all_items = set(item for s in sets for item in s)
    singletons = {item for item in all_items if item not in all_items_in_subsets}

    # Convert singletons to frozensets and add to maximal_subsets
    maximal_subsets.update(frozenset([singleton]) for singleton in singletons)

    return maximal_subsets


def sub_components(sub: str) -> tuple[int, str, str]:
    """Components of a substitution."""
    return sub_pos(sub), sub_aa0(sub), sub_aa1(sub)


def sub_pos(sub: str) -> int:
    """A substitution's position."""
    return int(re.match(r"^[A-Z](\d+)[A-Z](\(g[+-]\))?$", sub).groups()[0])


def sub_aa0(sub: str) -> str:
    """A substitution's amino acid lost."""
    return re.match(r"^([A-Z])\d+[A-Z](\(g[+-]\))?$", sub).groups()[0]


def sub_aa1(sub: str) -> str:
    """A substitution's amino acid gained."""
    return re.match(r"^[A-Z]\d+([A-Z])(\(g[+-]\))?$", sub).groups()[0]


class Titer:
    """
    A titer from a 2-fold dilution series using a 1:10 starting dilution.
    """

    def __init__(self, titer):
        self.titer = str(titer).replace(" ", "")
        if self.titer[0] == ">":
            raise NotImplementedError("gt titers not implemented")
        self.is_threshold = self.titer[0] == "<"
        self.is_inbetween = "/" in self.titer

    def __repr__(self) -> str:
        return f"Titer({self.titer})"

    def __str__(self) -> str:
        return self.titer

    @property
    def log_value(self) -> float:
        """
        Calculates the log value of the titer.

        Returns:
            float: The log value of the titer.

        Raises:
            NotImplementedError: If the titer 'greater than'.

        Note:
            If the titer is a 'less than', the log value is the log value of the titer value minus
            one. If the titer is a regular value, the log value is the log value of the titer
            divided by 10.

        Examples:
            >>> Titer("1280").log_value
            7.0
            >>> Titer("<10").log_value
            -1.0
            >>> Titer("20/40").log_value
            1.5
        """
        if self.is_inbetween:
            a, b = self.titer.split("/")
            return (Titer(a).log_value + Titer(b).log_value) / 2
        elif self.is_threshold:
            return Titer(self.titer[1:]).log_value - 1
        else:
            return np.log2(float(self.titer) / 10)


def aa_pairs_with_reversed(aa_pairs: Iterable[str]) -> set[tuple[str, str]]:
    """
    Select pairs of amino acid pairs where the reversed amino acid pair is also
    present. In this example "AN" is returned, with "NA" because both "AN" and "NA" are
    in the input:

    Args:
        aa_pairs: Amino acid pairs.

    Returns:
        set[tuple[str, str]]: A set of tuples of amino acid pairs where the reversed amino
        acid pair is also present.

    Examples:
        >>> aa_pairs_with_reversed(["QR", "AN", "TS", "ST", "KN", "NA"])
        {("AN", "NA"), ("ST", "TS")}
    """
    return set(
        tuple(sorted((pair, f"{pair[1]}{pair[0]}")))
        for pair in aa_pairs
        if f"{pair[1]}{pair[0]}" in aa_pairs and pair[0] != pair[1]
    )


def plot_reversed_amino_acid_effects_scatter(
    idata: az.InferenceData,
    ax: Optional[mpl.axes.Axes] = None,
    label_threshold: float = 1.0,
    text_kwds: Optional[dict] = None,
) -> mpl.axes.Axes:
    """
    Plot the effects of amino acid pairs and their reverse. E.g. the effect of "NK" and
    "KN" are plotted as a single point where the x-axis value represents the "KN" value
    and the y-axis value is the "NK" value.

    The regression line that is plotted is an orthogonal least squares fit (Deming
    regression). The parameters that are reported are the slope and intercept of this
    model (m and c), an a Pearson correlation coefficient (r), and p-value.

    Args:
        idata: Inference data object.
        ax: Matplotlib ax.
        label_threshold: Label amino acid pairs whose absolute difference in x and y
            values is greater than this value.
    """
    text_kwds = dict() if text_kwds is None else text_kwds
    ax = plt.gca() if ax is None else ax
    post = az.extract(idata)
    hdi = az.hdi(idata)

    kwds = dict(c="black")
    line_kwds = dict(alpha=0.5, linewidth=0.35)

    pairs_of_pairs = aa_pairs_with_reversed(post.coords["aa"].values)

    xy = np.array(
        [
            post["b_aa"].sel(aa=[pair_a, pair_b]).mean(dim="sample").values
            for pair_a, pair_b in pairs_of_pairs
        ]
    )

    labels = []
    for i, (pair_a, pair_b) in enumerate(pairs_of_pairs):
        x, y = xy[i]
        x_hdi, y_hdi = hdi["b_aa"].sel(aa=[pair_a, pair_b])

        ax.scatter(x, y, s=5, **kwds)
        ax.plot((x, x), y_hdi, **kwds, **line_kwds)
        ax.plot(x_hdi, (y, y), **kwds, **line_kwds)

        if abs(x - y) > label_threshold:
            labels.append(ax.text(x, y, f"{pair_a}/{pair_b}", **text_kwds))

    adjust_text(labels, x=xy[:, 0], y=xy[:, 1])

    ax.axline((0, 0), (1, 1), c="grey", lw=0.5)
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(base=2))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(base=2))
    ax.set(aspect=1, xlabel="ab", ylabel="ba")

    # Deming regression
    dr = reversed_amino_acid_effects_orthogonal_least_squares_regression(idata)
    text = f"r={dr['r']:.2f}\nm={dr['m']:.2f}\nc={dr['c']:.2f}\np={dr['p']:.2f}"
    ax.text(1, 1, text, transform=ax.transAxes, va="top", fontsize=8)
    ax.axline((0, dr["c"]), slope=dr["m"], c="black")

    return ax


def reversed_amino_acid_effects_orthogonal_least_squares_regression(
    idata: az.InferenceData,
) -> dict[str, float]:
    """
    Orthogonal Least squares regression on the amino acid pairs that are estimated both
    ways round. (E.g. there are estimates for "NK" as well as "KN").

    Args:
        idata: Inference data object.

    Returns:
        dict containing:
            m: Model slope.
            c: Model intercept.
            r: Pearson correlation coefficient.
            p: p-value of the Pearson correlation coefficient.

        r and p are independent of the regression. See:
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html
    """
    post = az.extract(idata)
    arr = np.array(
        [
            post["b_aa"].sel(aa=[pair_a, pair_b]).mean(dim="sample").values
            for pair_a, pair_b in aa_pairs_with_reversed(post.coords["aa"].values)
        ]
    )

    def f(p, x):
        return p[0] * x + p[1]

    od_reg = odr.ODR(odr.Data(arr[:, 0], arr[:, 1]), odr.Model(f), beta0=[1.0, 0.0])
    out = od_reg.run()

    pearsonr_result = pearsonr(arr[:, 0], arr[:, 1])
    return dict(
        m=out.beta[0],
        c=out.beta[1],
        r=pearsonr_result.statistic,
        p=pearsonr_result.pvalue,
    )


def delete_unused_variables(idata: az.InferenceData) -> az.InferenceData:
    """
    Remove variables from an InferenceData object that are from non-centered parametrisations
    and that contain log probabilities.

    Args:
        idata: Inference data object.

    Returns:
        Inference data object with unused variables removed.
    """
    for group in idata.groups():

        dataset = getattr(idata, group)

        dropped = dataset.drop_vars(
            [
                var
                for var in dataset.data_vars
                if re.match("^_.*_z$", var) or re.match(".*log__$", var)
            ]
        )

        setattr(idata, group, dropped)

    return idata


def sample_pymc(
    model: pm.Model,
    filename: Optional[str] = None,
    delete_unused: Optional[bool] = True,
    verbose: bool = True,
    **kwds,
) -> az.InferenceData:
    """
    Samples from a PyMC model and returns the inference data. At first this function tries to load
    the inference data from disk. If the file doesn't exist, then sample from the model instead, and
    save to disk using filename.

    Args:
        model (pm.Model): The PyMC model to sample from.
        filename (str | None): The path to the file where the inference data will be saved.
            Directory must exist. Must have a '.nc' suffix. Pass None to force model sampling.
        delete_unused (bool): When saving inference data objects, delete logp data and variables
            created for non-centered parametrisations.
        verbose (bool): Print messages saying if a posterior is being loaded from disk or sampled.
        **kwds: Additional keyword arguments to be passed to the `pymc.sample`.

    Returns:
        az.InferenceData: The inference data generated by PyMC.
    """
    if not isinstance(model, pm.Model):
        raise TypeError("model should be a pymc.Model instance")

    try:
        idata = az.from_netcdf(filename)

    except FileNotFoundError:

        path = Path(filename)

        if not path.suffix == ".nc":
            raise ValueError(f"filename should end in '.nc': {filename}")

        elif not path.parent.exists():
            raise ValueError(f"directory doesn't exist for: {filename}")

        else:

            if verbose:
                print(f"{filename} not found, sampling from model")

            with model:
                idata = pm.sample(**kwds)

            az.to_netcdf(idata, filename)

    except TypeError:

        if filename is not None:
            raise TypeError("filename should be None or str")

        if verbose:
            print("no filename passed, sampling from model")

        with model:
            idata = pm.sample(**kwds)

    else:
        if verbose:
            print(f"loaded {filename}")

    return delete_unused_variables(idata) if delete_unused else idata


def rename_coordinates(
    dataset: xr.Dataset, dim: str, mapping: dict[str, str] | Callable[[str], str]
) -> xr.Dataset:
    """
    Renames coordinates in a given dataset.

    Args:
        dataset (xr.Dataset): The dataset to rename coordinates in.
        dim (str): The name of the dimension to rename coordinates for.
        mapping (dict[str, str] or callable): A dictionary mapping the current coordinate values to
            the new coordinate values or a function.

    Returns:
        xr.Dataset: The dataset with renamed coordinates.
    """
    return dataset.assign_coords(
        **{
            dim: [
                mapping(k) if callable(mapping) else mapping[k]
                for k in dataset.coords[dim].values
            ]
        }
    )


def unpack(values: Iterable[Iterable[Any]]) -> Generator[Any, None, None]:
    """
    Unpacks a collection of iterables into a single iterable.

    Args:
        values: A collection of iterables to be unpacked.

    Yields:
        Elements from the unpacked iterables.
    """
    for value in values:
        yield from value


def find_glycosylation_sites(sequence: str) -> list[int]:
    """
    0-based indices of glycosylation motifs (NX{ST}) in string, where X is not proline.

    Args:
        sequence (str): The protein sequence in which to search for glycosylation motifs.

    Returns:
        list[int]: A list of indices in the protein sequence where glycosylation motifs are
            present.
    """
    return [match.start() for match in re.finditer(r"(?=(N[^P][ST]))", sequence)]


def find_substitutions(
    seq1: str,
    seq2: str,
    append_glyc_changes: bool = False,
    unify_glyc_changes: bool = False,
) -> Generator[str, None, None]:
    """
    List of substitution differences (format: 'aXb') between two protein sequences.

    Args:
        seq1 (str): The first protein sequence.
        seq2 (str): The second protein sequence.
        append_glyc_changes (bool): If a substitution is necessary to cause a glycosylation change,
            append '+g' / '-g' to the substitution if they cause a gain / loss of glycosylation.
            Mutually exclusive to unify_glyc_changes (default=False)
        unify_glyc_changes (bool): If a substitution is necessary to cause a glycosylation change,
            return a string representing that glycosylation change and not the substitution. E.g. if
            A156T caused a glycosylation change at site 154 then '154+g' would be yielded.
            Mutually exclusive to append_glyc_changes (default=False).

    Returns:
        list[str]: A list of strings representing the differences between the two sequences. Each
            string has the form "aXb", where "a" is the residue at the corresponding position in
            the first sequence, "X" is the 1-indexed position of the difference, and "b" is the
            residue at the corresponding position in the second sequence.
    """
    seq1 = seq1.upper()
    seq2 = seq2.upper()

    if append_glyc_changes and unify_glyc_changes:
        raise ValueError("append and unify glyc_changes can't both be True")

    elif append_glyc_changes or unify_glyc_changes:
        # dict mapping substitutions -> GlycosylationChange.
        # If multiple substitutions can cause a change then they will all appear in the dict
        glyc_changes = {
            sub: gc for gc in find_glycosylation_changes(seq1, seq2) for sub in gc.subs
        }

        for site, (a, b) in enumerate(zip(seq1, seq2), start=1):
            if a != b:
                sub = f"{a}{site}{b}"

                if sub in glyc_changes:
                    gc = glyc_changes[sub]
                    yield f"{sub}{gc.sign}g" if append_glyc_changes else str(gc)
                else:
                    yield sub

    else:
        for site, (a, b) in enumerate(zip(seq1, seq2), start=1):
            if a != b:
                yield f"{a}{site}{b}"


def find_glycosylation_changes(
    root_seq: str, mut_seq: str
) -> Generator[GlycosylationChange, None, None]:
    """
    Generate GlycosylationChange objects describing differences between glycosylation patterns of
    two protein sequences.

    Args:
        root_seq (str): The protein sequence of the root antigen.
        mut_seq (str): The protein sequence of the mutant antigen.

    Yields:
        GlycosylationChange: A named tuple describing the differences in glycosylation between the
            two sequences. The fields are:
            - gain_or_loss (str): "gain" if the glycosylation motif is present in the mutant but not
              in the root, "loss" otherwise.
            - subs (list[str]): A list of substrings representing the differences between the glycosylation
              motifs of the two sequences, e.g. "D1H".
            - root_motif (str): The motif in the root sequence.
            - mut_motif (str): The motif in the mutant sequence.
    """
    glyc_root = set(find_glycosylation_sites(root_seq))
    glyc_mut = set(find_glycosylation_sites(mut_seq))
    for index in glyc_root ^ glyc_mut:
        root_motif = root_seq[index : index + 3]
        mut_motif = mut_seq[index : index + 3]
        necessary_subs = subs_necessary_for_glyc_change(root_motif, mut_motif)
        yield GlycosylationChange(
            gain_or_loss="loss" if find_glycosylation_sites(root_motif) else "gain",
            site=index + 1,
            subs=[f"{a}{index + i + 1}{b}" for a, i, b in necessary_subs],
            root_motif=root_motif,
            mut_motif=mut_motif,
        )


def subs_necessary_for_glyc_change(
    root_motif: str, mut_motif: str
) -> list[tuple[str, int, str]]:
    """
    Given two 3 letter motifs return a list of substitutions that are necessary to cause the
    glycosylation difference between the root motif and the mutant motif. An error is raised if
    there is no glycosylation difference between root_motif and mut_motif.

    For instance, given the root and mutant motifs "NKT" and "NQA" the T -> A at the 3rd position is
    necessary and sufficient for the loss of glycosylation. The K -> Q at the 2nd position would not
    cause the loss of glycosylation.

    The only change at the 2nd position that could be implicated in the gain / loss would be the
    absence / presence of a proline.

    Args:
        root_motif (str): Three letter protein root sequence.
        mut_motif (str): Three letter protein mutant sequence.

    Returns:
        list[tuple[str, int, str], ...]: List of tuples containing the substitutions necessary
            for the change.
    """
    root_motif = root_motif.upper()
    mut_motif = mut_motif.upper()

    if len(root_motif) != 3 or len(mut_motif) != 3:
        raise ValueError(f"sequences not len 3: {root_motif}, {mut_motif}")

    root_state = find_glycosylation_sites(root_motif)
    mut_state = find_glycosylation_sites(mut_motif)

    if root_state == mut_state:
        raise ValueError(
            f"No difference in glycosylation between {root_motif} and {mut_motif}"
        )

    subs = []

    for i, (a, b) in enumerate(zip(root_motif, mut_motif)):

        if a == b:
            continue

        # Make a mutant sequence that has only this single aa change
        single_mut_seq = list(root_motif)
        single_mut_seq[i] = b
        single_mut_seq = "".join(single_mut_seq)

        if find_glycosylation_sites(single_mut_seq) == mut_state:
            subs.append((a, i, b))

    if not subs:
        raise NotImplementedError(
            "Combination of multiple aa changes necessary for glycosylation change between "
            f"{root_motif} and {mut_motif}"
        )
    else:
        return subs
