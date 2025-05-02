# paramlib

**paramlib** is a specialised Python package designed for centralised parameter and configuration management. It provides a structured approach to handling global parameters, configuration settings, and commonly used constants across projects.

## Features

- **Global Parameters**:
  - Time-related format strings
  - Mathematical constants
  - Programming concepts
  - Socio-economical parameters
- **Configuration Management**:
  - Database credentials handling
  - Error code mappings
  - User information storage
  - System-wide constants

---

## Installation Guide

### Dependency Notice

This package has minimal dependencies and is designed to be lightweight. No additional third-party libraries are required for basic functionality.

### Installation Instructions

Install the package using pip:

```bash
pip install paramlib
```

### Package Updates

To stay up-to-date with the latest version of this package, simply run:

```bash
pip install --upgrade paramlib
```

---

## Project Structure

The package is organised into the following components:

- **global_parameters.py**: Core parameter definitions
  - Time format strings
  - Mathematical constants
  - Programming concepts
  - Socio-economical parameters

- **config_params.py**: Configuration settings
  - Database credentials
  - Error code mappings
  - User information paths

For detailed version history and changes, please refer to:

- `CHANGELOG.md`: Comprehensive list of changes for each version
- `VERSIONING.md`: Versioning policy and guidelines

## Usage Examples

### Time Format Strings

```python
from paramlib import global_parameters

# Access basic time format strings
basic_format = global_parameters.BASIC_TIME_FORMAT_STRS["H"]  # "%Y-%m-%d %H:%M:%S"
date_format = global_parameters.BASIC_TIME_FORMAT_STRS["D"]   # "%Y-%m-%d"

# Access custom time format strings
excel_format = global_parameters.CUSTOM_TIME_FORMAT_STRS["CT_EXCEL_SPANISH_H"]  # "%d/%m/%y %H:%M:%S"
```

### Configuration Parameters

```python
from paramlib import config_params

# Access database credentials
db_creds = config_params.DATABASE_CREDENTIALS
username = db_creds["username"]
password = db_creds["password"]

# Access error code mappings
error_message = config_params.DB_ERROR_CODE_DICT["1045"]  # "Wrong username"
```

## Best Practices

1. **Parameter Organisation**:
   - Group related parameters together
   - Use clear, descriptive names
   - Follow Python naming conventions

2. **Configuration Management**:
   - Keep sensitive information secure
   - Use environment variables for sensitive data
   - Document all configuration options

3. **Version Control**:
   - Track changes in CHANGELOG.md
   - Follow semantic versioning
   - Document breaking changes
