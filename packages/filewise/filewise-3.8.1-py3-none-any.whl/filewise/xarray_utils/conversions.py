#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import xarray as xr

#------------------------#
# Import project modules #
#------------------------#

from filewise.xarray_utils.xarray_obj_handler import _save_ds_as_nc
from paramlib.global_parameters import CLIMATE_FILE_EXTENSIONS
from pygenutils.arrays_and_lists.conversions import flatten_to_string
from pygenutils.operative_systems.os_operations import exit_info, run_system_command
from pygenutils.strings.string_handler import (
    find_substring_index,
    get_obj_specs,
    modify_obj_specs
)

#------------------#
# Define functions #
#------------------#

# Xarray objects #
#----------------#

def grib2nc(grib_file_list, on_shell=False, option_str=None):
    """
    Converts a GRIB file or list of GRIB files to netCDF format. The conversion
    can be executed either via shell commands or programmatically using xarray.
    
    Parameters
    ----------
    grib_file_list : str or list of str
        The file path(s) of the GRIB file(s) to be converted.
    on_shell : bool, optional
        If True, the conversion will be handled through shell commands using 
        the 'grib_to_netcdf' tool. If False, the conversion will be done 
        programmatically using xarray.
    option_str : str, optional
        Additional options to pass to the shell command for 'grib_to_netcdf'. 
        This parameter is only used if 'on_shell' is set to True.
        
    Returns
    -------
    None
        Converts the GRIB file(s) to netCDF format and saves the output 
        netCDF file(s) in the same directory as the GRIB files.

    Notes
    -----
    - When 'on_shell' is True, the function builds and runs a shell command 
      that calls the 'grib_to_netcdf' tool, with optional flags.
    - When 'on_shell' is False, xarray is used to directly open the GRIB file 
      and convert it to netCDF format.
    - The function will prompt for input in the case of multiple GRIB files if 
      'on_shell' is True.
    """

    # Shell-based conversion #
    #-#-#-#-#-#-#-#-#-#-#-#-#-
    
    if on_shell:
        # Handle single GRIB file
        if isinstance(grib_file_list, str):
            nc_file_new = modify_obj_specs(grib_file_list, "ext", EXTENSIONS[0])
        
        # Handle list of GRIB files
        else:
            grib_allfile_info_str = flatten_to_string(grib_file_list)
            
            # Prompt user for the netCDF file name without extension
            nc_file_new_noext = input("Please introduce a name "
                                      "for the netCDF file, "
                                      "WITHOUT THE EXTENSION: ")
            
            # Validate the file name using RegEx
            allowed_minimum_char_idx = find_substring_index(nc_file_new_noext,
                                                            REGEX_GRIB2NC,
                                                            advanced_search=True)
            
            while allowed_minimum_char_idx == -1:
                print("Invalid file name.\nIt can contain alphanumeric characters, "
                      "as well as the following non-word characters: {. _ -}")
                nc_file_new_noext = input("Please introduce a valid name: ")
                allowed_minimum_char_idx = find_substring_index(nc_file_new_noext,
                                                                REGEX_GRIB2NC,
                                                                advanced_search=True)
            
            # Modify the file name to have the .nc extension
            nc_file_new_noext = modify_obj_specs(nc_file_new_noext,
                                                 obj2modify="ext",
                                                 new_obj=EXTENSIONS[0])
        
        # Construct the shell command for conversion
        grib2nc_template = "grib_to_netcdf "
        if option_str:
            grib2nc_template += f"{option_str} "
        grib2nc_template += f"-o {nc_file_new} {grib_allfile_info_str}"
        
        # Execute the shell command
        process_exit_info = run_system_command(grib2nc_template,
                                               capture_output=True,
                                               encoding="utf-8")
        exit_info(process_exit_info)

    # Programmatic conversion #
    #-#-#-#-#-#-#-#-#-#-#-#-#-#
    
    else:
        # Ensure grib_file_list is a list
        if isinstance(grib_file_list, str):
            grib_file_list = [grib_file_list]

        # Convert each GRIB file in the list to netCDF
        for grib_file in grib_file_list:
            grib_file_noext = get_obj_specs(grib_file, "name_noext", EXTENSIONS[0])
            ds = xr.open_dataset(grib_file, engine="cfgrib")
            _save_ds_as_nc(ds, grib_file_noext)

            
#--------------------------#
# Parameters and constants #
#--------------------------#

# Valid file extensions #
EXTENSIONS = CLIMATE_FILE_EXTENSIONS[::3]
  
# RegEx control for GRIB-to-netCDF single file name #
REGEX_GRIB2NC = r"^[a-zA-Z0-9\._-]$"
