"""
Script: plot-z-scores.py

Description:
    This script simulates a standard analysis workflow to check the internal consistency of the 
    DeepMIP database. Inputs files are global netCDF files and the results are displayed
    in overview tables for each DeepMIP experiment.
    Processing steps include:
    - construct filenames for each DeepMIP experiment, model and variable combination
    - check if specific files exist
    - regridding models to a common grid using CDO
    - calculate the global mean/min/max of regridded files
    - performing sanity checks on resulting netCDF files
    - select consistent vertical levels for each variable
    - compare global mean values across the DeepMIP ensemble
    - generate an overview table per experiment listing results for all variables and models
    - all tables are process in parallel using ProcessPoolExecutor to speed up total computation time

Requirements:
    - Python libraries (os, sys, pandas, numpy, xarray, tqdm, matplotlib).
    - CDO (Climate Data Operators) with Python bindings.
    - DeepMIP dictionaries (exp_dict, variable_dict, model_dict)
    - sufficient disk space for regridded and mean files.

Conda environment setup:
    To ensure the availability of dependencies, create a Conda environment using:
    conda create -n check-database -c conda-forge netcdf4 cdo python-cdo xarray matplotlib tqdm

Usage:
    python3 plot_z-scores.py

"""
import os
import sys
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from itertools import product
import time
from cdo import Cdo

cdo = Cdo()

from dictionaries.deepmip_eocene_p1_experiments import exp_dict
from dictionaries.deepmip_eocene_p1_models import model_dict
from dictionaries.deepmip_variables import variable_dict

# define some global user input
DBDIR       = "/data/deepmip-eocene-p1"
VERSION     = "v1.0"
GRID        = "r180x90"
REGRID_DIR  = f"{DBDIR}/validation_tables/data"
# create separate tables for atmopshere and ocean variables
table_list  = ["atmos", "ocean"]
# create separate tables for means and time_series
time_list   = ["mean", "time_series"]

def construct_filename(e_key, v_key, m_key, model_info, variable_info, time_key):
    if time_key == "mean":
        directory = "climatology"
    elif time_key == "time_series":
        directory = "time_series"

    if variable_info["dimensions"] > 2:
        return f"{DBDIR}/{model_info['family']}/{m_key}/{e_key}/{VERSION}/{directory}/{v_key}_{m_key}_{e_key}_v1.0.{time_key}.nc"
    # time invariant boundary conditions
    else:
        return f"{DBDIR}/{model_info['family']}/{m_key}/{e_key}/{VERSION}/{directory}/{v_key}_{m_key}_{e_key}_v1.0.nc"


def check_file_exists(filename):
    return os.path.exists(filename)


def regrid_file(input_file, time_key, grid_def="r180x90"):
    # create the output filename/path
    regridded_file = os.path.join(
        REGRID_DIR, os.path.basename(input_file).replace(".nc", f".{grid_def}.nc")
    )

    # check whether the regridded file already exists
    if not os.path.exists(regridded_file):
        # if not, perform the regridding and save the regridded file
        try:
            if time_key == "mean":
                # regrid annual mean
                cdo.remapbil(
                    grid_def, input=cdo.timmean(input=input_file), output=regridded_file
                )
            elif time_key == "time_series":
                # regrid last available year
                cdo.remapbil(
                    grid_def,
                    input=cdo.seltimestep("1189/1200", input=input_file),
                    output=regridded_file,
                )
        except Exception as e:
            print(f"Error regridding {input_file}: {str(e)}")
            sys.exit()

    return regridded_file


# calculate global mean/min/max of regridded files
def calculate_global_mean_min_max(input_file, v_key):
    # create the output filename/paths
    mean_file = os.path.join(
        REGRID_DIR, os.path.basename(input_file).replace(".nc", ".mean.nc")
    )
    min_file = os.path.join(
        REGRID_DIR, os.path.basename(input_file).replace(".nc", ".min.nc")
    )
    max_file = os.path.join(
        REGRID_DIR, os.path.basename(input_file).replace(".nc", ".max.nc")
    )
    combined_file = os.path.join(
        REGRID_DIR, os.path.basename(input_file).replace(".nc", ".mean_min_max.nc")
    )

    # check whether the combined file already exists
    if not os.path.exists(combined_file):
        # if not, perform the calculations and save the files
        cdo.fldmean(
            input=f"-chname,{v_key},{v_key}_mean {input_file}", output=mean_file
        )
        cdo.fldmin(input=f"-chname,{v_key},{v_key}_min {input_file}", output=min_file)
        cdo.fldmax(input=f"-chname,{v_key},{v_key}_max {input_file}", output=max_file)

        # merge the mean, min, and max files into a single file
        cdo.merge(input=f"{mean_file} {min_file} {max_file}", output=combined_file)

    return combined_file


# load global mean/min/max values of regridded files and perform sanity checks
def process_mean_min_max(input_file, v_key, variable_info):
    # load dataset
    ds = xr.open_dataset(input_file, decode_times=False)

    # check 1: current variable should be in DataSet
    da_gm = ds[f"{v_key}_mean"]

    # check 2: number of dimensions should match the dictionary definition
    if da_gm.ndim != variable_info["dimensions"]:
        print(
            f"Error: {v_key} in {input_file} has {da_gm.ndim} dimensions, but should have {variable_info['dimensions']}"
        )
        sys.exit()

    # check 3: number of timestep should be 1 (annual mean) or 12 (monthly mean)
    # identify the time dimension name
    if variable_info["dimensions"] > 2:
        time_dim_name = get_dimension_name(da_gm, "T")
        if da_gm[time_dim_name].size not in [1, 12]:
            print(
                f"Error: {v_key} in {input_file} has {da_gm[time_dim_name].size} timesteps, but should have 1 or 12"
            )
            sys.exit()

    # after checks are passed, select the correct vertical level
    if variable_info["dimensions"] <= 3:
        # calculate annual mean of single level variables and boundary conditions
        mean_value = np.nanmean(ds[f"{v_key}_mean"].values)
        min_value = np.nanmin(ds[f"{v_key}_min"].values)
        max_value = np.nanmax(ds[f"{v_key}_max"].values)

    elif variable_info["dimensions"] == 4:
        # select target vertical level:
        # 500 hPa for atmosphere variables on pressure levels
        # first level for atmosphere variables on model levels
        # 1000 m for ocean variables on depth levels
        vertical_dim_name = get_dimension_name(da_gm, "Z")
        vertical_units = da_gm[vertical_dim_name].attrs["units"]
        if vertical_units in ["Pa"]:
            ds_level = ds.sel({vertical_dim_name: 50000}, method="nearest")
        elif vertical_units in ["hPa", "mbar"]:
            ds_level = ds.sel({vertical_dim_name: 500}, method="nearest")
        elif vertical_units in ["m", "meters"]:
            ds_level = ds.sel({vertical_dim_name: 1000}, method="nearest")
        elif vertical_units in ["centimeters"]:
            ds_level = ds.sel({vertical_dim_name: 100000}, method="nearest")
        elif v_key in ["ua", "va", "wa"]:
            # select first level for variables on model levels
            ds_level = ds.isel({vertical_dim_name: 0})
        else:
            print(
                f"Error: {v_key} in {input_file} has unknown vertical units {vertical_units} in dimension {vertical_dim_name}"
            )
            sys.exit()

        mean_value = np.nanmean(ds_level[f"{v_key}_mean"].values)
        min_value = np.nanmin(ds_level[f"{v_key}_min"].values)
        max_value = np.nanmax(ds_level[f"{v_key}_max"].values)

    # return np.round(mean_value,1), np.round(min_value,1), np.round(max_value,1)
    return float(mean_value), float(min_value), float(max_value)


def get_dimension_name(da, axis_value):
    """
    Identify the dimension name in the given data array by checking the axis attribute.
    """
    for dim in da.dims:
        if da[dim].attrs.get("axis") == axis_value:
            return dim

    raise ValueError(f"No valid dimension name found with attribute :axis = '{axis_value}'.")


def compute_group_z_scores(df):
    """
    Compute Z-scores for each element in df relative to the median and standard
    deviation of its respective [min, mean, max] group.
    """
    # exclude first and last columns
    df = df.iloc[:, 1:-3]

    # initialize a DataFrame to store z-scores
    z_scores = pd.DataFrame(index=df.index, columns=df.columns)

    # loop through each group of three columns
    for i in range(3):
        subgroup = df.iloc[:, i::3]

        # xompute median and standard deviation for the subgroup
        medians = subgroup.median(axis=1)
        std_devs = subgroup.std(axis=1)

        # xompute Z-scores with handling of division by zero
        subgroup_z_scores = subgroup.apply(
            lambda x: (x - medians) / (std_devs + (std_devs == 0)), axis=0
        )

        # assign computed z-scores to the respective columns in the z_scores DataFrame
        z_scores.iloc[:, i::3] = subgroup_z_scores

    return np.absolute(z_scores)

def draw_table(df, title, realm):

    fig_width = 15
    column_width = 1.0 / len(df.columns)

    # some settings are different for atmosphee and ocean tables due to different number of variables
    if realm == "atmos":
        fig_height = 9.3
        separator_height_min = 0.048
        separator_height_max = 0.981
        header_line_height = 0.954
        model_label_height = 0.97
        cbar_y = 0.905
        title_y = 1.02
        cbar_height = 0.015
    elif realm == "ocean":
        fig_height = 4.1
        separator_height_min = 0.055
        separator_height_max = 1.0
        header_line_height = 0.898
        model_label_height = 0.98
        cbar_y = 0.98
        title_y = 1.07
        cbar_height = 0.03

    fig, ax = plt.subplots(
        figsize=(fig_width, fig_height)
    ) 

    ax.axis("tight")
    ax.axis("off")

    z_scores = compute_group_z_scores(df)

    # define colormap
    norm = mcolors.Normalize(
        vmin=0, vmax=3.0
    )
    cmap = (
        cm.RdYlGn_r
    )  # using red-yellow-green colormap; low values -> green, high -> red
    cmap.set_over("pink")

    the_table = ax.table(
        cellText=df.values,
        colLabels=df.columns.get_level_values(1),
        rowLabels=df.index,
        colWidths=[column_width for x in df.columns],
        cellLoc="center",
        loc="center",
    )

    # adding a row for model names
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(6)

    # manually set the position and content of the header text
    unique_models = df.columns.get_level_values(0).unique()
    num_sub_columns = 3  # mean/min/max
    for i, model_name in enumerate(unique_models):
        if model_name == "unit":
            continue
        # calculate the position above the middle of the respective mean/min/max columns
        pos = (i * num_sub_columns - 0.5) / len(df.columns)
        ax.text(
            pos,
            model_label_height,
            model_name,
            size=10,
            ha="center",
            va="center",
            transform=ax.transAxes,
        )

        # draw thicker lines around model sub-columns
        line_l = mlines.Line2D(
            [pos - 1.5 * column_width, pos - 1.5 * column_width],
            [separator_height_min, separator_height_max],
            color="black",
            linewidth=2,
            transform=ax.transAxes,
        )
        line_r = mlines.Line2D(
            [pos + 1.5 * column_width, pos + 1.5 * column_width],
            [separator_height_min, separator_height_max],
            color="black",
            linewidth=2,
            transform=ax.transAxes,
        )
        ax.add_line(line_l)
        ax.add_line(line_r)
    line_header = mlines.Line2D(
        [0.0, 1.0],
        [header_line_height, header_line_height],
        color="black",
        linewidth=1,
        transform=ax.transAxes,
    )
    ax.add_line(line_header)

    # iterate over cells and modify border line properties
    for i, cell in the_table.get_celld().items():
        row, col = i
        cell.set_edgecolor("grey")
        cell.set_linewidth(0.5) 

    # loop over each cell in the DataFrame
    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            if j == 0 or j >= len(df.columns) - 3:
                if j == 0:
                    the_table[i + 1, j].set_facecolor("lightgray")
                else:
                    the_table[i + 1, j].set_facecolor(cmap(0))
                    the_table[i + 1, j].set_text_props(fontweight="bold", color="w")

                if j == 0 and df.index[i] in [
                    "pr",
                    "evspsbl",
                    "wfo",
                    "uo",
                    "vo",
                    "wo",
                    "difvtrbo",
                    "difvmo",
                ]:
                    the_table[i + 1, j].set_fontsize(4)
                else:
                    the_table[i + 1, j].set_fontsize(6)
                continue
            # color cell by z-score
            z_val = z_scores.iloc[i, j - 1]
            cell_color = cmap(norm(z_val))
            if z_val > 3.0:
                the_table[i + 1, j].set_facecolor("pink")
            else:
                if np.isnan(df.iloc[i, j]):
                    the_table[i + 1, j].set_facecolor("lightgrey")
                else:
                    the_table[i + 1, j].set_facecolor(cell_color)
            # round values
            formatted_value = f"{df.iloc[i, j]:.1f}"
            the_table[i + 1, j].get_text().set_text(formatted_value)

    # color the header row
    for (i, j), cell in the_table.get_celld().items():
        if i == 0:  # header row
            cell.set_text_props(fontweight="bold", color="w")
            cell.set_facecolor("dimgray")
        elif j == -1:  # first column
            cell.set_text_props(fontweight="bold", color="w")
            cell.set_facecolor("dimgray")

    plt.title(
        f"{title} validation table", fontsize=14, y=title_y
    ) 

    # define the position and dimensions of the new axes for colorbar
    # [left, bottom, width, height]
    cbar_ax = fig.add_axes([0.13, cbar_y, 0.14, cbar_height])

    # create the colorbar
    cb = plt.colorbar(
        mappable=cm.ScalarMappable(norm=norm, cmap=cmap),
        cax=cbar_ax,
        orientation="horizontal",
        ticks=[norm.vmin, norm.vmax],
        extend="max",
    )

    cb.set_label("|z-score|", labelpad=-10, y=0.5)

    plt.savefig(
        f"{DBDIR}/validation_tables/{title}_validation_table.pdf",
        format="pdf",
        bbox_inches="tight",
    )

    plt.close(fig) 

def process_single_table(task):
        
    # unpack the task tuple
    e_key, time_key, table_realm = task  

    table_vars = [
    key for key, val in variable_dict.items() if val["realm"] == table_realm
    and key not in ["msftmz", "msftbarot", "rsnscs", "rlnscs"]
    ]

    model_names_orig = [model["abbrv"] for model in model_dict.values()]
    model_names = model_names_orig.copy()
    model_names.append("median")

    table_columns = pd.MultiIndex.from_product(
        [model_names, ["min", "mean", "max"]], names=["model", "stat"]
    )

    # create an empty DataFrame
    overview_table = pd.DataFrame(index=table_vars, columns=table_columns)

    # adding a new column at position 0 (leftmost)
    overview_table.insert(0, "unit", 0)
    overview_table["unit"] = overview_table["unit"].astype(object)

    # loop over variables and models to check file exists and update the table
    for v_key in table_vars:
        variable_info = variable_dict[v_key]
        unit_dict = f"${variable_info['unit']}$"
        if unit_dict == "$%$":
            unit_dict = "$\\%$"
        overview_table.loc[v_key, "unit"] = unit_dict

        for m_key, model_info in model_dict.items():

            filename = construct_filename(
                e_key, v_key, m_key, model_info, variable_info, time_key
            )

            if check_file_exists(filename):
                # regrid the file to a common grid
                regridded_file = regrid_file(
                    filename, time_key, grid_def=GRID
                )

                # calculate global mean of regridded file
                gm_file = calculate_global_mean_min_max(
                    regridded_file, v_key
                )

                # load global mean value(s), perform some sanity checks and select correct level
                global_mean, global_min, global_max = process_mean_min_max(
                    gm_file, v_key, variable_info
                )

                # apply conversion factors for specific variables
                conversion_factors = {
                    "pr": (86400, "$mm day^{-1}$"),
                    "evspsbl": (86400, "$mm day^{-1}$"),
                    "wfo": (86400, "$mm day^{-1}$"),
                    "ps": (0.01, "$hPa$"),
                    "psl": (0.01, "$hPa$"),
                    "hus": (1000, "$1$"),
                    "uo": (100, "$cm s^{-1}$"),
                    "vo": (100, "$cm s^{-1}$"),
                    "wo": (86400, "$m day^{-1}$"),
                    "difvtrbo": (10000, "$cm^{-2} s^{-1}$"),
                    "difvmo": (10000, "$cm^{-2} s^{-1}$"),
                }

                if v_key in conversion_factors:
                    factor, unit = conversion_factors[v_key]
                    global_min *= factor
                    global_mean *= factor
                    global_max *= factor
                    overview_table.loc[v_key, "unit"] = unit

                # save values to the DataFrame
                overview_table.loc[
                    v_key, (model_info["abbrv"], "min")
                ] = global_min
                overview_table.loc[
                    v_key, (model_info["abbrv"], "mean")
                ] = global_mean
                overview_table.loc[
                    v_key, (model_info["abbrv"], "max")
                ] = global_max
        # calculate median values across the ensemble
        stats = ["min", "mean", "max"]
        for stat in stats:
            values = overview_table.loc[
                v_key, (model_names_orig, stat)
            ].values.astype(float)
            if not np.all(np.isnan(values)):  # xheck if all values are nan
                overview_table.loc[v_key, ("median", stat)] = np.round(
                    np.nanmedian(values), 1
                )
            else:
                overview_table.loc[v_key, ("median", stat)] = np.nan

    # display the table
    table_title = f"{e_key} {table_realm} {time_key}"
    draw_table(overview_table, table_title, table_realm)

def count_files(directory):
    num_files = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    return  round(num_files / 5)

def get_max_number_of_fields(tasks):
    file_count = 0
    for task in tasks:
        # unpack the task tuple
        e_key, time_key, table_realm = task  

        table_vars = [
        key for key, val in variable_dict.items() if val["realm"] == table_realm
        and key not in ["msftmz", "msftbarot", "rsnscs", "rlnscs"]
        ]

        for v_key in table_vars:
            variable_info = variable_dict[v_key]
            for m_key, model_info in model_dict.items():

                filename = construct_filename(
                    e_key, v_key, m_key, model_info, variable_info, time_key
                )

                if check_file_exists(filename):
                    file_count += 1
    return file_count

#################################################################################
# main program startes here
#################################################################################

def main():
    if not os.path.exists(REGRID_DIR):
        os.makedirs(REGRID_DIR)

    # process tables in parallel
    tasks = list(product(exp_dict.keys(), time_list, table_list))

    print("Overview of tables to be created:")
    for task in tasks:
        print(f"- Experiment: {task[0]}, Time: {task[1]}, Realm: {task[2]}")

    expected_total_variables = get_max_number_of_fields(tasks)

    print(f"Counting the total number of available model fields for processing ...")
    print(f"A total of {expected_total_variables} files will be processed to generate the {len(tasks)} overview tables.")
    print(f"This might take a while ...")

    # Start the executor and submit all tasks
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_single_table, task) for task in tasks]

        # Initialize the progress bar
        with tqdm(total=expected_total_variables, desc="Processing global fields", unit="field") as pbar:
            while not all(f.done() for f in futures):
                # Update the progress bar based on the number of files created
                current_file_count = count_files(REGRID_DIR)
                pbar.update(current_file_count - pbar.n)
                time.sleep(1)  # Sleep for a short while to not overwhelm the CPU

            # Check for exceptions in the completed futures
            for future in futures:
                try:
                    future.result()
                except Exception as exc:
                    print(f'Task generated an exception: {exc}')


if __name__ == "__main__":
    main()
