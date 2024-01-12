#! /usr/bin/env python3

import pandas as pd
from pathlib import Path
from rich import print as echo
from typing import List

from mdpilot.src import LAMMPS_Project

import typer
app = typer.Typer()



@app.command()
def main(
    param_names: List[str],
    param_ranges: List[range],
):


if __name__ == "__main__":
    app()