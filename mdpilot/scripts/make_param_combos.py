#! /usr/bin/env python3

import numpy as np
import pandas as pd
from pathlib import Path
from typing import List
from numbers import Number
from itertools import product
import os

import typer


def main(
    param_names: List[str],
    param_values: List[List[Number] | List[str]],
    outfile_path: Path = Path(os.getcwd()),
    index_by: List[int] = None,
):
    """
    Create a csv file with all combinations of parameters.

    Parameters
    ----------
    param_names : List[str]
        Names of parameters , these should match the names of the variables in the LAMMPS script (in-file)
    param_values : List[List[Number] | List[str]]
        List of lists of parameter values
    outfile_path : Path
        Path to output file where the combinations will be saved. Default is current working directory.
    index_by : List[int], optional
        List of integers that tell the function how to generate the combinations. If the entry is -1, then
        the parameter is included when calculating all combinations. If an integer is given, then that parameter is always matched
        to the value in that list.

    Example:
    param_names = ["Temp", "Interval" "Lattice_const"]
    param_values = [[10, 20, 30], [1, 2], [5.5, 5.4, 5.3]]
    outfile_path = "C:/Users/<username>/Desktop"
    index_by = [-1, -1, 0]

    This will generate the following combinations. Note how the lattice constant is always pegged to the temperature.
    10 1 5.5
    10 2 5.5
    20 1 5.4
    20 2 5.4
    30 1 5.3
    30 2 5.3
    """

    assert len(param_names) == len(param_values), f"Number of parameter names ({len(param_names)}) does not match number of parameter values ({len(param_values)})"
    assert len(index_by) == len(param_names), f"Length of index_by ({len(index_by)}) does not match number of parameters ({len(param_names)})"

    if index_by == None:
        index_by = -1*np.ones(len(param_names))
    else:
        index_by = np.array(index_by)

    param_values = np.array(param_values, dtype = object)
    param_names = np.array(param_names)

    combos = product(*param_values[index_by == -1])
    n_combos = np.prod([len(param_values[i]) for i in range(len(param_values)) if index_by[i] == -1])
    data = {param_names[i] : np.zeros(n_combos) for i in range(len(param_names))}

    for i, combo in enumerate(combos):
        for j, param_name in enumerate(param_names):
            if index_by[j] == -1:
                data[param_name][i] = combo[j]
            else:
                combo_np = np.array(combo)
                other_idx = np.where(param_values[index_by[j]] == combo_np[index_by[j]])[0][0]
                data[param_name][i] = param_values[j][other_idx]

    df = pd.DataFrame(data)
    df.to_csv(os.path.join(outfile_path, "param_combos.csv"), index=False)


if __name__ == "__main__":
    typer.run(main)