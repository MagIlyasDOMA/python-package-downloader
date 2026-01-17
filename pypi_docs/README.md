# Python Package Downloader (PPD) - Documentation
## Description
**Python Package Downloader (PPD)** is a command—line tool for easily downloading and unpacking Python packages as `.whl` files with the ability to automatically extract and manage dependencies.

## Installation
```shell
pip install python-package-downloader
```

After installation, there are three commands available to run:
- `ppd` (recommended)
- `python-package-downloader`
- `python_package_downloader`

## Basic usage
### Basic syntax
```shell
ppd <pack1> <pack2> ... [options]
```

### Examples
```shell
# Downloading and unpacking a single
ppd requests package

# Download multiple
ppd packages numpy pandas matplotlib

# Uploading to the specified directory
ppd requests --directory ./my_packages

# Save .whl files after unpacking
ppd flask --save-wheel

# Save .dist-info
ppd django --save-dist-info
```

## Command line options
### Required arguments
- `packages` — one or more packages to download (positional argument)

### Basic options
| Option | Short version | Description |
|---------------------------------------------|-----------------|-----------------------------------------------|
| `-- version`, `-v` | `-v` | Show program version |
| `--directory`, `-d` | `-d <path>`     | Directory for downloading and unpacking packages |
| `--save-wheel`, `-w` | `-w` | Save .whl files after unpacking |
| `--save-dist-info`, `-i` | `-i` | Save .dist-info directories |
| `--requirements-file`, `--requirements`, `-r` | `-r [path]`     | Create a file requirements.txt with dependencies |

### Output control (logging)
| Option | Short version | Values | Description |
|------------------------------------------------------------------------------------|-----------------|-----------------------------------------------------------------------------------------|----------------------------|
| `-- logging-level`, `--log-level`, `--loglevel`, `--log`, `--verbosity`, `-l`, `-V` | `-l`, `-V` | `0-7` or `silent`, `critical`, `error`, `warning`, `info`, `verbose`, `debug`, `silly` | Output level of detail |

#### Logging levels:
- `0` / `silent` — completely silent mode
- `1` / `critical` — critical errors only
- `2` / `error` — errors
- `3` / `warning` — warnings
- `4` / `info` — normal information (default)
- `5` / `verbose` — detailed information
- `6` / `debug` — debugging information
- `7` / `silly` — maximum detail

## Detailed description of the functionality
### The work process
1. **Downloading packages:** The program uses `pip download` to download `.whl` files without dependencies
2. **Unpacking:** Automatically extracts the contents of `.whl` files
3. **Cleaning:** By default, deletes the `.whl` files and `.dist-info' directories after unpacking
4. **Dependency Management:** Can create a file `requirements.txt ` with package dependencies

### Features
- **Automatic Python detection:** Finds an available Python interpreter in the system
- **Error handling:** Different error display levels depending on the logging level
- **Color output:** Uses color formatting for better readability
- **Checking for updates:** Automatically checks for new versions

### Files and directories
By default, the program:
1. Downloads `.whl` files to the current directory (or specified via `-d`)
2. Unpacks them into the same directory
3. Deletes `.whl` files (unless `--save-wheel` is specified)
4. Deletes `.dist-info` directories (unless `--save-dist-info` is specified)
5. Creates `requirements.txt ` with dependencies (if `-r` is specified)

## Usage examples
### Example 1: Downloading an offline installation package
```shell
# Upload the package to the current
ppd requests directory

# Result:
# - The requests/ directory with the package contents
# - The package files are ready for use
```

### Example 2: Creating a portable library
```shell
# Create a directory with multiple packages
ppd numpy pandas matplotlib --directory ./data_science_packages

# Save information about
ppd numpy pandas matplotlib -r dependencies./requirements.txt
```

### Example 3: Silent mode for scripts
```shell
# Minimal output, only
ppd errors some-package --log-level silent
# or
ppd some-package -l 0
```

### Example 4: Debugging problems
```shell
# Maximum detailed output
ppd problematic-package --log-level silly
# or
ppd problematic-package -l 7
```

## Requirements
- Python >= 3.10
- Internet access to download packages
- Installed `pip` in the system

## Permissions
- MIT License
- Cross-platform (Windows, Linux, macOS)

## Support and feedback
- The author: Маг Ильяс DOMA (MagIlyasDOMA)
- Email: magilyas.doma.09@list.ru
- GitHub: [https://github.com/MagIlyasDOMA/python-package-downloader](https://github.com/MagIlyasDOMA/python-package-downloader )
- PyPI: [https://pypi.org/project/python-package-downloader/](https://pypi.org/project/python-package-downloader/)

## Notes
- The program uses `pip download --no-deps`, so dependencies are not downloaded automatically
- To get dependencies, use the `-r` option to create a file. requirements.txt
- It is recommended to use virtual environments for packet isolation

## Update
```shell
# Update check (automatic at startup)
ppd --version

# Manual update
pip install --upgrade python-package-downloader
# Or
ppd --upgrade
```

## Exit codes
- `0` — successful completion
- `1` — error during execution 
- `2` — help is called (when running without arguments)
