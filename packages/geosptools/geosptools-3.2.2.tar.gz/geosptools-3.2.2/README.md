# geosptools

**geosptools** is a specialised Python package designed for geospatial data processing and analysis. It provides tools for handling raster data, format conversions, and spatial operations, with a focus on environmental and climate data applications.

## Features

- **Raster Operations**:
  - NetCDF to raster format conversion
  - Raster merging and manipulation
  - Coordinate reference system handling
  - NoData value management
- **Format Conversion**:
  - Support for multiple raster formats (GTiff, JPEG, etc.)
  - Customisable output parameters
  - Resolution control
- **Spatial Analysis**:
  - Region-based operations
  - Multi-file processing capabilities
  - Spatial data integration

## Project History

This project was developed to address the need for simplified geospatial data processing in Python. It builds upon the powerful GDAL library while providing a more intuitive interface for common geospatial operations. The package has evolved to include more sophisticated spatial analysis tools while maintaining ease of use.

## Usage Examples

### Converting NetCDF to Raster

```python
from geosptools import raster_tools

# Convert a single NetCDF file to raster
raster_tools.nc2raster(
    nc_file_list="input.nc",
    output_file_format="GTiff",
    raster_extension=".tif",
    raster_resolution=1000,
    crs="EPSG:4326"
)

# Convert multiple NetCDF files
raster_tools.nc2raster(
    nc_file_list=["file1.nc", "file2.nc"],
    output_file_format="GTiff",
    raster_extension=".tif",
    raster_resolution=1000
)
```

### Merging Rasters

```python
from geosptools import raster_tools

# Merge multiple rasters
raster_tools.merge_independent_rasters(
    raster_files_dict={
        "region1": "file1.tif",
        "region2": "file2.tif"
    },
    output_file_format="GTiff",
    joint_region_name="combined",
    output_file_name_ext=".tif"
)
```

## Versioning

This package follows semantic versioning (SemVer) with the format `vX.Y.Z`:

- **X** (Major): Incompatible API changes
- **Y** (Minor): Backward-compatible functionality additions
- **Z** (Patch): Backward-compatible bug fixes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Installation Guide

### Dependency Notice

Before installing, please ensure the following dependencies are available on your system:

- **Required Third-Party Libraries**:
  - GDAL
  - numpy
  - paramlib
  - pygenutils

  You can install them via pip:
  
  ```bash
  pip install GDAL numpy paramlib pygenutils
  ```

  Or via Anaconda (recommended channel: `conda-forge`):

  ```bash
  conda install -c conda-forge gdal numpy paramlib pygenutils
  ```

### Installation Instructions

Install the package using pip:

```bash
pip install geosptools
```

### Package Updates

To stay up-to-date with the latest version of this package, simply run:

```bash
pip install --upgrade geosptools
```

---

## Project Structure

The package is organised into the following components:

- **raster_tools.py**: Core raster operations
  - NetCDF to raster conversion
  - Raster merging
  - Spatial data handling
  - Format conversion utilities

For detailed version history and changes, please refer to:

- `CHANGELOG.md`: Comprehensive list of changes for each version
- `VERSIONING.md`: Versioning policy and guidelines
