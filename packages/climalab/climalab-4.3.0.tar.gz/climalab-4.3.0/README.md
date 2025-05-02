# climalab

**climalab** is a Python toolkit designed to facilitate climate data analysis and manipulation, including tools for data extraction, processing, and visualization. It leverages external tools and standards like CDO and CDS to streamline workflows for climate-related research.

## Features

- **Meteorological Tools**:
  - Comprehensive handling of meteorological variables and data
  - Weather software input file generation
  - Variable conversion and standardisation utilities
- **NetCDF Tools**:
  - Advanced CDO operations for netCDF file manipulation
  - NCO tools for efficient data processing
  - Faulty file detection and reporting
  - Basic information extraction from netCDF files
- **Supplementary Analysis Tools**:
  - Visualisation tools for maps and basic plots
  - Bias correction methods (parametric and non-parametric quantile mapping)
  - Statistical analysis tools
  - Auxiliary functions for data processing
- **Project Structure**:
  - Sample project templates for data analysis workflows
  - Standardised directory organisation
  - Version control and changelog management

---

## Installation Guide

### Dependency Notice

Before installing, please ensure the following dependencies are available on your system:

- **Required Third-Party Libraries**:
  - numpy
  - pandas
  - scipy
  - cdsapi (for data downloads)
  - PyYAML (for configuration files)

  You can install them via pip:
  
  ```bash
  pip install numpy pandas scipy cdsapi PyYAML
  ```

  Or via Anaconda (recommended channel: `conda-forge`):

  ```bash
  conda install -c conda-forge numpy pandas scipy cdsapi pyyaml
  ```

- **Other Internal Packages**: these are other packages created by the same author:
  - filewise
  - paramlib
  - pygenutils

### Installation Instructions

Install the package using pip:

```bash
pip install climalab
```

### Package Updates

To stay up-to-date with the latest version of this package, simply run:

```bash
pip install --upgrade climalab
```

---

## Project Structure

The package is organised into several sub-packages:

- **meteorological/**: Core tools for handling meteorological data and variables
  - `variables.py`: Meteorological variable definitions and conversions
  - `weather_software.py`: Tools for weather software input file generation

- **netcdf_tools/**: Utilities for working with netCDF files
  - `cdo_tools.py`: CDO operations and utilities
  - `nco_tools.py`: NCO operations and utilities
  - `detect_faulty.py`: Tools for identifying problematic netCDF files
  - `extract_basics.py`: Basic information extraction from netCDF files

- **supplementary_tools/**: Additional analysis and visualisation tools
  - Bias correction methods
  - Plotting utilities
  - Statistical analysis tools
  - Auxiliary functions

- **data_analysis_projects_sample/**: Example project structure demonstrating best practices

For detailed version history and changes, please refer to:

- `CHANGELOG.md`: Comprehensive list of changes for each version
- `VERSIONING.md`: Versioning policy and guidelines
