"""
@Author  : 梁彧祺
@File    : define_sequence_data.py
@Time    : 05/02/2025 12:47
@Desc    : Optimized SequenceData class with integrated color scheme & legend handling.
"""
# Only applicable to Python 3.7+, add this line to defer type annotation evaluation
from __future__ import annotations
# Define the public API at the top of the file
__all__ = ['SequenceData']

# Global variables and other imports that do not depend on pandas are placed here
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from docutils.parsers.rst import states
from matplotlib.colors import ListedColormap
import re


class SequenceData:
    """
    A class for defining and processing a sequence dataset for social sequence analysis.

    This class provides:
    - Sequence extraction & missing value handling.
    - Automatic alphabet (state space) management.
    - Efficient sequence-to-numeric conversion.
    - Color mapping & legend storage for visualization.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        time_type: str,
        time: list,
        states: list,
        labels: list = None,
        id_col: str = None,
        weights: np.ndarray = None,
        start: int = 1,
        missing_handling: dict = None,
        void: str = "%",
        nr: str = "*",
        custom_colors: list = None
    ):
        """
        Initialize the SequenceData object.

        :param data: DataFrame containing sequence data.
        :param time: List of columns containing time labels.
        :param time_type: Type of time labels (e.g., "year", "age").
        :param states: List of unique states (categories).
        :param alphabet: Optional predefined state space.
        :param labels: Labels for states (optional, for visualization).
        :param id_col: Column name for row identifiers, which is very important for hierarchical clustering.
        :param weights: Sequence weights (optional).
        :param start: Starting time index (default: 1).
        :param missing_handling: Dict specifying handling for missing values (left, right, gaps).
        :param void: Symbol for void elements (default: "%").
        :param nr: Symbol for missing values (default: "*").
        :param custom_colors: Custom color palette for visualization.
        """
        # Ensure time_type is either "year" or "age"
        if time_type not in ["year", "age"]:
            raise ValueError("time_type must be either 'year' or 'age'")

        # Import pandas here instead of the top of the file
        import pandas as pd

        self.data = data.copy()
        self.time = time

        if time_type == "year":
            self.time_type = "year"
        elif time_type == "age":
            self.time_type = "age"

        # Remove all non-numeric characters from the year labels, e.g., "Year2020" -> "2020", or "C1" -> "1"
        # self.cleaned_time = [re.sub(r'\D', '', str(year)) for year in time]
        # No longer support this feature as we encourage users to clean the time variables.
        # TODO: might implement a helper function for users to clean up their time variables.
        self.cleaned_time = time

        self.states = states
        self.alphabet = states or sorted(set(data[time].stack().dropna().unique()))
        self.labels = labels or states
        self.id_col = id_col
        self.ids = np.array(data[id_col].values) if self.id_col else data.index
        self.weights = weights
        self.start = start
        self.missing_handling = missing_handling or {"left": np.nan, "right": "DEL", "gaps": np.nan}
        self.void = void
        self.nr = nr
        self.custom_colors = custom_colors

        # Validate parameters
        self._validate_parameters()

        # Extract & process sequences
        self.seqdata = self._extract_sequences()
        self._process_missing_values()
        self._convert_states()

        # Assign colors & save legend
        self._assign_colors()

        # Automatically print dataset overview
        print("\n[>] SequenceData initialized successfully! Here's a summary:")
        self.describe()

    @property
    def values(self):
        """Returns sequence data as a NumPy array, similar to xinyi_original_seqdef()."""
        return self.seqdata.to_numpy(dtype=np.int32)

    def __repr__(self):
        return f"SequenceData({len(self.seqdata)} sequences, Alphabet: {self.alphabet})"

    def _validate_parameters(self):
        """Ensures correct input parameters."""
        # Check states, alphabet, labels
        if not self.states:
            raise ValueError("'states' must be provided.")
        if self.alphabet and set(self.alphabet) != set(self.states):
            raise ValueError("'alphabet' must match 'states'.")
        if self.labels and len(self.labels) != len(self.states):
            raise ValueError("'labels' must match the length of 'states'.")
        
        # Check ids
        if self.ids is not None:
            if len(self.ids) != len(self.data):
                raise ValueError("'ids' must match the length of 'data'.")

            if len(np.unique(self.ids)) != len(self.ids):
                raise ValueError("'ids' must be unique.")
        else:
            self.ids = np.arange(len(self.data))

        # Check weights
        if self.weights is not None:
            if len(self.weights) != len(self.data):
                raise ValueError("'weights' must match the length of 'data'.")
        else:
            self.weights = np.ones(self.data.shape[0])

    def _extract_sequences(self) -> pd.DataFrame:
        """Extracts only relevant sequence columns."""
        return self.data[self.time].copy()

    def _process_missing_values(self):
        """Handles missing values based on the specified rules."""
        # left, right, gaps = self.missing_handling.values()
        #
        # # Fill left-side missing values
        # if not pd.isna(left) and left != "DEL":
        #     self.seqdata.fillna(left, inplace=True)
        #
        # # Process right-side missing values
        # if right == "DEL":
        #     self.seqdata = self.seqdata.apply(lambda row: row.dropna().reset_index(drop=True), axis=1)
        #
        # # Process gaps (internal missing values)
        # if not pd.isna(gaps) and gaps != "DEL":
        #     self.seqdata.replace(self.nr, gaps, inplace=True)

        self.ismissing = self.seqdata.isna().any().any()

        if self.ismissing:
            self.states.append("Missing")

    def _convert_states(self):
        """
        Converts categorical states into numerical values for processing.
        Note that the order has to be the same as when the user defines the states of the class,
        as it is very important for visualization.
        Otherwise, the colors will be assigned incorrectly.

        For instance, self.states = ['Very Low', 'Low', 'Middle', 'High', 'Very High'], as the user defines when defining the class
        but the older version here is {'High': 1, 'Low': 2, 'Middle': 3, 'Very High': 4, 'Very Low': 5}
        """
        correct_order = self.states

        # Create the state mapping with correct order
        self.state_mapping = {state: idx + 1 for idx, state in enumerate(correct_order)}

        # Apply the mapping
        # If there are missing values, replace them with the last index + 1
        # And update the additional missing value as a new state in self.state and self.alphabet
        try:
            self.seqdata = self.seqdata.map(lambda x: self.state_mapping.get(x, len(self.states)))
        except AttributeError:
            self.seqdata = self.seqdata.applymap(lambda x: self.state_mapping.get(x, len(self.states)))

        if self.ids is not None:
            self.seqdata.index = self.ids

    def _assign_colors(self, reverse_colors=True):
        """Assigns a color palette using user-defined or default Spectral palette."""
        num_states = len(self.states)

        if self.custom_colors:
            if len(self.custom_colors) != num_states:
                raise ValueError("Length of custom_colors must match number of states.")
            color_list = self.custom_colors
        else:
            if num_states <= 20:
                color_list = sns.color_palette("Spectral", num_states)
            else:
                color_list = sns.color_palette("cubehelix", num_states)

            if reverse_colors:
                color_list = list(reversed(color_list))

        self.color_map = {state: color_list[i] for i, state in enumerate(self.states)}

    def get_colormap(self):
        """Returns a ListedColormap for visualization."""
        return ListedColormap([self.color_map[state] for state in self.states])

    def describe(self):
        """Prints an overview of the sequence dataset."""
        print(f"[>] Number of sequences: {len(self.seqdata)}")
        
        if self.ismissing:
            lengths = self.seqdata.apply(lambda row: (row != len(self.states)).sum(), axis=1)
            print(f"[>] Min/Max sequence length: {lengths.min()} / {lengths.max()}")

            # print some missing information
            missing_index = self.seqdata.stack()[self.seqdata.stack() == len(self.states)].index.get_level_values(0).tolist()
            missing_count = len(missing_index)
            print(f"[>] There are {missing_count} sequences with missing values, which are {missing_index}")

        else:
            print(f"[>] Min/Max sequence length: {self.seqdata.notna().sum(axis=1).min()} / {self.seqdata.notna().sum(axis=1).max()}")

        print(f"[>] Alphabet: {self.alphabet}")

    def get_legend(self):
        """Returns the legend handles and labels for visualization."""
        self.legend_handles = [plt.Rectangle((0, 0), 1, 1,
                                             color=self.color_map[state],
                                             label=state) for state in
                               self.states]
        return [handle for handle in self.legend_handles], self.states

    def to_dataframe(self) -> pd.DataFrame:
        """Returns the processed sequence dataset as a DataFrame."""
        return self.seqdata

    def plot_legend(self, save_as=None, dpi=200):
        """Displays the saved legend for sequence state colors."""
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.legend(handles=self.legend_handles, loc='center', title="States", fontsize=10)
        ax.axis('off')

        if save_as:
            plt.savefig(save_as, dpi=dpi)
            plt.show()
        else:
            plt.tight_layout()
            plt.show()

    # ------------------------------
    # The following are for multidomain sequence analysis, especially for seqdomassoc()

    @property
    def n_sequences(self):
        """Returns number of sequences (rows)."""
        return self.seqdata.shape[0]

    @property
    def n_steps(self):
        """Returns sequence length (columns)."""
        return self.seqdata.shape[1]

    @property
    def alphabet(self):
        """Returns state alphabet."""
        return self._alphabet

    @alphabet.setter
    def alphabet(self, val):
        self._alphabet = val

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, val):
        self._weights = val

    def flatten(self) -> np.ndarray:
        """Flatten all sequences into a 1D array (row-wise)."""
        return self.seqdata.values.flatten()

    def flatten_weights(self) -> np.ndarray:
        """
        Repeat weights across sequence length for 1D alignment with flatten().
        E.g., 5 sequences × 10 steps → repeat each weight 10 times.
        """
        return np.repeat(self.weights, self.n_steps)

    def to_numeric(self) -> np.ndarray:
        """Returns integer-coded sequence data as NumPy array."""
        return self.seqdata.to_numpy(dtype=np.int32)

    def get_xtabs(self, other: SequenceData, weighted=True) -> np.ndarray:
        """
        NumPy-only version of get_xtabs.
        Returns a raw NumPy matrix: shape (len(alphabet1), len(alphabet2))
        """
        if self.n_sequences != other.n_sequences or self.n_steps != other.n_steps:
            raise ValueError("Both SequenceData objects must have same shape.")

        v1 = self.flatten()
        v2 = other.flatten()

        n1 = len(self.alphabet)
        n2 = len(other.alphabet)

        table = np.zeros((n1, n2), dtype=np.float64)

        if weighted:
            w = self.flatten_weights()
            # Safe increment using integer indices
            # Numpy's index starts from 0, thus it is important to reduce by 1
            np.add.at(table, (v1 - 1, v2 - 1), w)
        else:
            np.add.at(table, (v1 - 1, v2 - 1), 1)

        return table





