#!/usr/bin/env python3
import sys
import os
import subprocess
from dictionaries.deepmip_eocene_p1_models import model_dict
from dictionaries.deepmip_variables import variable_dict

# Configuration parameters to be set by user
DBDIR = "/Volumes/external_Samsung-SSD/ceda/deepmip-eocene-p1"
OUTDIR = os.path.join(DBDIR, "regridded_fields")
VERSION = "v1.0"
TARGET_GRID = "r360x180"
ATM_REGRIDDING = "remapbil"
OCN_REGRIDDING = "remapnn"
VARIABLES = ["tas", "pr", "tos"]

def log(level, message):
    print(f"[{level}] {sys.argv[0]} - {message}")

def check_requirements():
    if not os.path.isdir(DBDIR):
        log("ERROR", f"Required directory {DBDIR} not found.")
        sys.exit(1)
    if subprocess.run(["which", "cdo"], capture_output=True).returncode != 0:
        log("ERROR", "CDO command could not be found. Please install CDO.")
        sys.exit(1)
    if subprocess.run(["which", "python3"], capture_output=True).returncode != 0:
        log("ERROR", "Python 3 is not available. Please install Python 3.")
        sys.exit(1)

def regrid_variable(in_dir, out_dir, var, realm):
    """
    Regrid a given variable using CDO based on its realm (atmospher or ocean).
    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    os.chdir(in_dir)
    files = [f for f in os.listdir(in_dir) if f.startswith(var) and f.endswith(".mean.nc")]

    if len(files) == 1:
        input_file = files[0]
        output_file = f"{os.path.splitext(input_file)[0]}.{TARGET_GRID}.nc"
        if realm == "atmos":
            subprocess.run(["cdo", f"-{ATM_REGRIDDING},{TARGET_GRID}", input_file, os.path.join(out_dir, output_file)])
        elif realm == "ocean":
            subprocess.run(["cdo", f"-{OCN_REGRIDDING},{TARGET_GRID}", input_file, os.path.join(out_dir, output_file)])
            if var == "tos":
                filled_output_file = f"{os.path.splitext(output_file)[0]}.filled.nc"
                subprocess.run(["cdo", "-setmisstonn", os.path.join(out_dir, output_file), os.path.join(out_dir, filled_output_file)])
    elif len(files) > 1:
        log("ERROR", f"More than one file found for variable {var}.")
        sys.exit(1)
    else:
        log("INFO", f"No file found for variable {var} in {in_dir}. Skipping!")

def calculate_ensemble_mean(out_dir, exp, var):
    """
    Calculate the annual mean ensemble mean for a given experiment and variable combination.
    """
    files = [os.path.join(out_dir, f) for f in os.listdir(out_dir) if f.startswith(var) and f.endswith(f"{exp}_{VERSION}.mean.{TARGET_GRID}.nc")]
    if files:
        annual_mean_files = [f"{file}_annual_mean.nc" for file in files]
        for file, annual_mean_file in zip(files, annual_mean_files):
            subprocess.run(["cdo", "yearmean", file, annual_mean_file])
        
        ensmean_file = os.path.join(out_dir, f"{var}_{exp}_ensemble_mean.{TARGET_GRID}.nc")
        subprocess.run(["cdo", "ensmean"] + annual_mean_files + [ensmean_file])
        log("INFO", f"Ensemble mean calculated for variable {var} and experiment {exp}")
    else:
        log("INFO", f"No files found for variable {var} and experiment {exp} to calculate ensemble mean.")

def get_model_keys():
    """
    get model keys from the DeepMIP model dictionary
    """
    for key, value in model_dict.items():
        yield key, value['family'], value['exps']

def get_realm(variable):
    """
    get realm of a given variable from the DeepMIP model dictionary.
    """
    return variable_dict.get(variable, {}).get('realm', 'Variable not found')

def main():
    check_requirements()
    for key, family, experiments in get_model_keys():
        for exp in experiments:
            in_dir = os.path.join(DBDIR, family, key, exp, VERSION, "climatology")
            for var in VARIABLES:
                realm = get_realm(var)
                if realm != "Variable not found":
                    log("INFO", f"Processing model {key} and variable {var} for experiment {exp} ...")
                    regrid_variable(in_dir, OUTDIR, var, realm)
                else:
                    log("ERROR", f"Variable {var} not found in the DeepMIP-Eocene model dataset.")
                    sys.exit(1)
    # Calculate ensemble mean for each experiment and variable combination
    for exp in experiments:
        for var in VARIABLES:
            calculate_ensemble_mean(OUTDIR, exp, var)

if __name__ == "__main__":
    main()