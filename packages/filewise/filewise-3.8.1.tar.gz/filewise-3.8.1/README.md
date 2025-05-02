# filewise

**filewise** is a comprehensive Python package designed to streamline file operations, data manipulation, and format conversions. It provides a robust set of tools for handling various file types, data structures, and automated file management tasks.

## Features

- **File Operations**:
  - Bulk file renaming (automatic and manual modes)
  - File permission management
  - Path manipulation utilities
  - File content operations
- **Data Manipulation**:
  - Advanced pandas DataFrame operations
  - xarray dataset handling
  - JSON object manipulation
  - Data format conversions
- **Format Converters**:
  - PDF manipulation tools
  - File format conversion utilities
- **General Utilities**:
  - Code introspection tools
  - Object manipulation utilities
- **Scripts**:
  - File compression and copying
  - PDF manipulation and compression
  - Email to PDF conversion
  - File property modification

## Versioning

This package follows [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH):

- **MAJOR** version (e.g., 2.x.x to 3.x.x): Incompatible API changes
- **MINOR** version (e.g., 3.3.x to 3.4.x): New functionality in a backward-compatible manner
- **PATCH** version (e.g., 3.5.0 to 3.5.4): Backward-compatible bug fixes

For detailed information about changes in each version, please refer to the [CHANGELOG.md](CHANGELOG.md) file.

---

## Installation Guide

### Dependency Notice

Before installing, please ensure the following dependencies are available on your system:

- **Required Third-Party Libraries**:
  - pandas
  - xarray
  - PyPDF2
  - numpy
  - json

  You can install them via pip:
  
  ```bash
  pip install pandas xarray PyPDF2 numpy
  ```

  Or via Anaconda (recommended channel: `conda-forge`):

  ```bash
  conda install -c conda-forge pandas xarray pypdf2 numpy
  ```

### Installation Instructions

Install the package using pip:

```bash
pip install filewise
```

### Package Updates

To stay up-to-date with the latest version of this package, simply run:

```bash
pip install --upgrade filewise
```

---

## Project Structure

The package is organised into several sub-packages:

- **file_operations/**: Core file handling utilities
  - `bulk_rename_auto.py`: Automatic file renaming
  - `bulk_rename_manual.py`: Manual file renaming
  - `permission_manager.py`: File permission management
  - `path_utils.py`: Path manipulation utilities
  - `ops_handler.py`: File operation management

- **pandas_utils/**: pandas DataFrame operations
  - `pandas_obj_handler.py`: DataFrame manipulation
  - `data_manipulation.py`: Data processing utilities
  - `conversions.py`: Data format conversion

- **xarray_utils/**: xarray dataset operations
  - `xarray_obj_handler.py`: Dataset manipulation
  - `patterns.py`: Common operation patterns
  - `file_utils.py`: File handling utilities
  - `data_manipulation.py`: Data processing

- **json_utils/**: JSON handling
  - `json_obj_handler.py`: JSON object manipulation
  - `json_encoding_operations.py`: Encoding utilities

- **format_converters/**: File format conversion
  - `pdf_tools.py`: PDF manipulation utilities

- **general/**: General utilities
  - `introspection_utils.py`: Code introspection tools

- **scripts/**: Utility scripts
  - `bulk_rename.py`: File renaming script
  - `copy_compress.py`: File compression utilities
  - `compress_pdf.py`: PDF compression
  - `tweak_pdf.py`: PDF manipulation
  - Email conversion scripts

For detailed version history and changes, please refer to:

- `CHANGELOG.md`: Comprehensive list of changes for each version
- `VERSIONING.md`: Versioning policy and guidelines

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
