#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import os
import numpy as np

#------------------#
# Define functions #
#------------------#

# Helpers #
#---------#

def _fetch_path_items(path, glob_bool=True):
    """
    Converts a path into an os-based path and handles globbing.

    Parameters
    ----------
    path : str
        The directory path to search within.
    glob_bool : bool, optional
        If True, finds all files and directories recursively. Defaults to True.
        
    Returns
    -------
    list
        A list of all files and directories found in the specified path.
    """
    if glob_bool:
        items = []
        for dirpath, dirnames, filenames in os.walk(path):
            items.extend([os.path.join(dirpath, dirname) for dirname in dirnames])
            items.extend([os.path.join(dirpath, file) for file in filenames])
        return items
    else:
        return [os.path.join(path, item) for item in os.listdir(path)]
    
    
# Switch-case dictionary to modify patterns based on 'match_type' argument 
def _add_glob_left(patterns):
    return [f"*{pattern}" for pattern in patterns]

def _add_glob_right(patterns):
    return [f"{pattern}*" for pattern in patterns]

def _add_glob_both(patterns):
    return [f"*{pattern}*" for pattern in patterns]

def _whole_word(patterns):
    return patterns  # No modification for whole word match


# Main functions #
#----------------#

# File Operations #
#~~~~~~~~~~~~~~~~~#

def find_files(patterns, search_path, match_type="ext", top_only=False, dirs_to_exclude=None):
    """
    Searches for files based on extensions or glob patterns with various matching types.

    Parameters
    ----------
    patterns : str or list
        File extensions or glob patterns to search for.
    search_path : str
        The directory path to search within.
    match_type : str, optional
        The type of matching to apply. Options include:
        - "ext": match based on file extensions.
        - "glob_left": match with a wildcard at the beginning of the pattern.
        - "glob_right": match with a wildcard at the end of the pattern.
        - "glob_both": match with wildcards at both the beginning and the end of the pattern.
        - "ww": match the exact whole word (no wildcards).
        Defaults to "ext".
    top_only : bool, optional
        If True, only searches in the top directory without subdirectories. 
        Defaults to False.
    dirs_to_exclude : str or list, optional
        Directory or list of directories to exclude from the search.
        Defaults to None.
    
    Returns
    -------
    list of str
        A list of files matching the specified patterns.

    Raises
    ------
    ValueError
        If an invalid `match_type` is provided.
    """
    if isinstance(patterns, str):
        patterns = [patterns]
    if isinstance(dirs_to_exclude, str):
        dirs_to_exclude = [dirs_to_exclude]

    modify_pattern_func = MATCH_PATTERN_MODIFIER.get(match_type)
    if not modify_pattern_func:
        raise ValueError(f"Invalid match_type '{match_type}'. Choose one from {MTD_KEYS}")
    
    patterns = modify_pattern_func(patterns)

    if top_only:
        files = _fetch_path_items(search_path, glob_bool=False)
    else:
        files = _fetch_path_items(search_path)

    if dirs_to_exclude:
        files = [file for file in files if not any(excluded in file for excluded in dirs_to_exclude)]

    match_func = MATCH_TYPE_DICT.get(match_type)
    if not match_func:
        raise ValueError(f"Invalid match_type '{match_type}'. Choose one from {MTD_KEYS}")

    return list(np.unique([file for file in files if match_func(file, patterns)]))


# Directory Operations #
#~~~~~~~~~~~~~~~~~~~~~~#

def find_dirs_with_files(patterns, search_path, match_type="ext", top_only=False, dirs_to_exclude=None):
    """
    Finds directories containing files that match the given patterns with various matching types.

    Parameters
    ----------
    patterns : str or list
        File extensions or glob patterns to search for.
    search_path : str
        The directory path to search within.
    match_type : str, optional
        The type of matching to apply. Options include:
        - "ext": match based on file extensions.
        - "glob_left": match with a wildcard at the beginning of the pattern.
        - "glob_right": match with a wildcard at the end of the pattern.
        - "glob_both": match with wildcards at both the beginning and the end of the pattern.
        - "ww": match the exact whole word (no wildcards).
        Defaults to "ext".
    top_only : bool, optional
        If True, only searches in the top directory without subdirectories.
        Defaults to False.
    dirs_to_exclude : str or list, optional
        Directory or list of directories to exclude from the search.
        Defaults to None.
    
    Returns
    -------
    list of str
        A list of directories containing files matching the specified patterns.

    Raises
    ------
    ValueError
        If an invalid `match_type` is provided.
    """
    if isinstance(patterns, str):
        patterns = [patterns]
    if isinstance(dirs_to_exclude, str):
        dirs_to_exclude = [dirs_to_exclude]

    modify_pattern_func = MATCH_PATTERN_MODIFIER.get(match_type)
    if not modify_pattern_func:
        raise ValueError(f"Invalid match_type '{match_type}'. Choose one from {MTD_KEYS}")
    
    patterns = modify_pattern_func(patterns)

    if top_only:
        files = _fetch_path_items(search_path, glob_bool=False)
    else:
        files = _fetch_path_items(search_path)

    if dirs_to_exclude:
        files = [file for file in files if not any(excluded in file for excluded in dirs_to_exclude)]

    match_func = MATCH_TYPE_DICT.get(match_type)
    if not match_func:
        raise ValueError(f"Invalid match_type '{match_type}'. Choose one from {MTD_KEYS}")

    dirs = [os.path.dirname(file) for file in files if match_func(file, patterns)]
    return list(np.unique(dirs))


# Extensions and Directories Search #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def find_items(search_path, skip_ext=None, top_only=False, task="extensions", dirs_to_exclude=None):
    """
    Finds all unique file extensions or directories in the specified path.

    Parameters
    ----------
    search_path : str
        The directory path to search within.
    skip_ext : str or list, optional
        Extensions to skip while searching. Defaults to None.
    top_only : bool, optional
        If True, only searches in the top directory without subdirectories.
        Defaults to False.
    task : {"extensions", "directories"}, default "extensions"
        - "extensions": to find file extensions
        - "directories" to find directories
    dirs_to_exclude : str or list, optional
        Directory or list of directories to exclude from the search.
        Defaults to None.
    
    Returns
    -------
    list of str
        A list of unique file extensions or directories.
    """
    if skip_ext is None:
        skip_ext = []
    if isinstance(skip_ext, str):
        skip_ext = [skip_ext]
    if isinstance(dirs_to_exclude, str):
        dirs_to_exclude = [dirs_to_exclude]

    if top_only:
        items = _fetch_path_items(search_path, glob_bool=False)
    else:
        items = _fetch_path_items(search_path)

    if dirs_to_exclude:
        items = [item for item in items if not any(excluded in item for excluded in dirs_to_exclude)]

    if task == "extensions":
        extensions = [os.path.splitext(file)[1] for file in items 
                      if os.path.isfile(file) and os.path.splitext(file)[1] not in skip_ext]
        return list(np.unique(extensions))
    elif task == "directories":
        dirs = [item for item in items if os.path.isdir(item)]
        return list(np.unique(dirs))
    else:
        raise ValueError("Invalid task. Use 'extensions' or 'directories'.")
        
#--------------------------#
# Parameters and constants #
#--------------------------#

# Switch-case dictionaries #
#--------------------------#

# Define a switch-case dictionary to handle 'match_type' options
MATCH_TYPE_DICT = {
    "ext": lambda file, patterns: any(file.endswith(f".{ext}") for ext in patterns),
    "glob_left": lambda file, patterns: any(pattern in file for pattern in patterns),
    "glob_right": lambda file, patterns: any(pattern in file for pattern in patterns),
    "glob_both": lambda file, patterns: any(pattern in file for pattern in patterns),
    "ww": lambda file, patterns: any(pattern == file for pattern in patterns)
}

MTD_KEYS = list(MATCH_TYPE_DICT.keys())

MATCH_PATTERN_MODIFIER = {
    "ext": lambda patterns: patterns,
    "glob_left": _add_glob_left,
    "glob_right": _add_glob_right,
    "glob_both": _add_glob_both,
    "ww": _whole_word
}