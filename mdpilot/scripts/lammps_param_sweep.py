#! /usr/bin/env python3

import numpy as np
import os
from joblib import Parallel, delayed
import time
from pathlib import Path
from rich import print as echo

from mdpilot.src import LAMMPS_Project

import typer
app = typer.Typer()


def run(project, job_names, np, ncores, lmp_command): #Run all active jobs
    start_time = time.time()
    max_parallel_jobs = int(ncores//np)
    cmd = f"mpirun -np {np} {lmp_command}"
    if len(job_names) <= max_parallel_jobs:
        Parallel(n_jobs = max_parallel_jobs)(delayed(project.run_job)(job, cmd) for job in job_names)
    else: #chunk jobs into smaller arrays smaller than "max_parallel_jobs"
        job_names_chunked = [job_names[i:i + max_parallel_jobs] for i in range(0, len(job_names), max_parallel_jobs)]
        n_chunks = len(job_names_chunked)
        for i,chunk in enumerate(job_names_chunked):
            echo("===============");print(f"Batch {i+1} of {n_chunks}"); print("===============")
            Parallel(n_jobs = len(chunk))(delayed(project.run_job)(job, cmd) for job in chunk)
    echo("---All jobs took %s seconds ---" % (time.time() - start_time))

def setup(infile_path : Path, base_path : Path,  project_name : str, param_combos_path : Path, vel_seed_name : str):

    project = LAMMPS_Project(project_name, infile_path, base_path)

    temps = [100,300,500,700,900,1100,1300]

    lattice_const_mapping = {100: 5.4333, 200: 5.4353, 300 : 5.4373, 400 : 5.4393, 500: 5.4411, 600 : 5.4428, 700 : 5.4446, 800: 5.4464, 900: 5.448, 1000: 5.4496}
    dt = 1e-3
    n_runs = 40
    job_names = []

    for i in range(len(temps)):
         T = temps[i]
         job_name = f"T{T}"
         job_names.append(job_name)
         #project.new_job(job_name, n_runs, ["velocity_seed"], {"T": T , "lattice_const" : lattice_const_mapping[T]})
         project.new_job(job_name, n_runs, [vel_seed_name], {"T": T})
    
    return project, job_names

@app.command()
def main(
    infile_path: Path,
    base_path: Path,
    project_name: str,
    np: int,
    ncores: int,
    lmp_command: str = "lmp",
    vel_seed_name: str = "velocity_seed",
):
    proj, job_names = setup(infile_path, base_path, project_name, param_combos_path, vel_seed_name)
    run(proj, job_names, np, ncores, lmp_command)

if __name__ == "__main__":
    app()