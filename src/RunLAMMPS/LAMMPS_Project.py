import os
import copy
import shutil

from .LAMMPS_Job import LAMMPS_Job
from ..FileIO.InFile import InFile

class LAMMPS_Project:
    '''
    - Project to be run on the local machine. 
    - Expects local version of LAMMPS to be accessible through the command line.
    '''

    def __init__(self, name : str, infile_path : str, basepath: str, only_make_plots: bool = False):
        '''
        name : Name of project
        infile_path : path to in file, contains file name and extension
        basepath : Root of file system for this project.
        outpath: Folder created inside of basepath labeled with project name.
        '''
        self.name = name
        self.infile_path = infile_path
        self.basepath = basepath
        self.only_make_plots = only_make_plots
        self.outpath = os.path.join(self.basepath,self.name)

        if not only_make_plots:
            self.__init_file_structure()

        '''
        In File: An object which can modify the variables inside an in-file. Contains
            other useful helper functions (e.g. to print variables out)
        Old Jobs: A list of Job objects created by previous instances of this project. Collected from
            output folder of the project.
        New Jobs: A list of Job objects created by the current instance of this project. 
        Job Tracker: An object that creates and maintains a text file of which Jobs
            have been run and assigns unique IDs to each run of a Job to ensure
            that no data is overwritten.
        '''
        self.in_file = InFile(self.infile_path)
        self.jobs = {}



    def __init_file_structure(self) -> None:
        '''
        Creates a folder to store all output from every job associated with this project.
        '''
        if os.path.exists(self.basepath):
            try:
                os.mkdir(self.outpath)
                #Copy in-file to project folder
                shutil.copy2(self.infile_path, self.outpath)
                #Reset infile path to be the one in the project folder
                self.infile_path = os.path.join(self.outpath,os.path.basename(self.infile_path))
            except FileExistsError: 
                raise RuntimeError(f"A project with this name already exists in : {self.basepath}")
            except PermissionError: raise PermissionError(f"Python does not have permission to create: {self.outpath}")
        else:
            raise RuntimeError(f"{self.basepath} does not exist")


    # def __collect_old_jobs(self) -> dict:
    #     '''
    #     If this project has been executed previously there will be Job folders
    #     inside of 'outpath'. This function collects the names of those jobs.
    #     '''
    #     old_jobs = {}
    #     for path in os.listdir(self.outpath):
    #         if os.path.isdir(os.path.join(self.outpath,path)):
    #             old_job_name = os.path.basename(path)
    #             old_jobs[old_job_name] = "old_job"
    #     return old_jobs


    def new_job(self, name: str, n_seeds :int, seed_variables : list, changed_vars : dict = None) -> None:
        '''
        Creates job if no job with 'name' exists in the project folder.

        Name: Name of job to create or load from project structure
        Changed_Vars: Variables to change in the in-file, will be ignored if
            job already existed in file structure.
        '''
        name = name.strip()

        # #Check if a job with this name was created before
        # if name in self.old_jobs.keys():
        #     self.active_jobs[name] = LAMMPS_Job(self, name)
        #     print("Found job with same name in file structure. Re-activating old job with its orignal variables.")
        #     return


        #Check if a job with this name already exists in the current project instance
        if (name in self.jobs.keys()):
            print("=====================================================================")
            print(f"A job with name {name} already exists in the current project instance. This job will not be created.")
            print("=====================================================================\n")
            return

        job_variables = copy.deepcopy(self.in_file.free_variables)
        if changed_vars is not None:
            for key,val in changed_vars.items():
                try:
                    job_variables[key] = val
                except KeyError:
                    raise KeyError(f"{key} is not a modifiable variable in the in-file at {self.infile_path}")
                
        
        self.jobs[name] = LAMMPS_Job(self, name, n_seeds, seed_variables, job_variables)

    # def run_all_jobs(self, lammps_env_var = "lmp") -> None:
    #     if len(self.jobs) > 0:
    #         print("===============================")
    #         print(f"Queued Jobs: {list(self.jobs.keys())}")
    #         print("===============================\n")
    #         for _,job in self.jobs.items():
    #             exit_status = job.run(lammps_env_var)
    #             if exit_status == 0:
    #                 print(f"{job.name} completed successfully."); print()
    #             else:
    #                 print(f"{job.name} failed. Exited with code {exit_status}."); print()
    #     else:
    #         print("No active yet. See create_job() & activate_old_job().")
    
    def run_job(self, job_name, lammps_env_var = "lmp"):
        if self.only_make_plots:
            raise RuntimeError("Flag only_make_plots is set to True")
        try:
            for seed in range(self.jobs[job_name].n_seeds):
                exit_status = self.jobs[job_name].run(lammps_env_var, seed)
                if exit_status != 0:
                    print(f"{job_name} failed. Exited with code {exit_status} on seed {seed}."); print()
            print(f"{job_name} completed successfully."); print()
        except KeyError:
            raise KeyError(f"No job with name {job_name}")

