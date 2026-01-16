#!/usr/bin/env python3
import os, zipfile, glob, warnings, tempfile
from argparse import ArgumentParser, ArgumentTypeError
from typing import Optional, Literal

__version__ = '1.0.0'

LOGGING_LEVELS = ('silent', 'critical', 'error', 'warning', 'info', 'verbose', 'debug', 'silly')
ALLOWED_LOGGING_LEVEL_VALUES = ('silent', 'critical', 'error', 'warning', 'info', 'verbose', 'debug',
                                'silly', 0, 1, 2, 3, 4, 5, 6, 7, '0', '1', '2', '3', '4', '5', '6', '7')

LoggingLevelType = Literal[*ALLOWED_LOGGING_LEVEL_VALUES]
IntLoggingLevelType = Literal[0, 1, 2, 3, 4, 5, 6, 7]

# log_level: IntLoggingLevelType = 4
# packages: list
# directory: Optional[str]

def logging_level(level: LoggingLevelType) -> int:
    if level not in ALLOWED_LOGGING_LEVEL_VALUES:
        raise ArgumentTypeError(f'Invalid logging level: {level}')
    elif isinstance(level, int):
        return level
    elif level.isdigit():
        return int(level)
    else:
        return LOGGING_LEVELS.index(level)


def pip_log_flags(temp_filename: str, log_level: IntLoggingLevelType) -> str:
    match log_level:
        case 0:
            return f' -qqq > {temp_filename}'
        case 1:
            return ' -qqq'
        case 2:
            return ' -qq'
        case 3:
            return ' -q'
        case 4:
            return ''
        case 5:
            return ' -v'
        case 6:
            return ' -vv'
        case 7:
            return ' -vvv'
        case _:
            raise ValueError(f'Invalid logging level: {log_level}')


def log(message: str, current_level: int, max_level: int = 4) -> None:
    if max_level <= current_level:
        print(message)


def download_wheels(packages: list[str], directory: Optional[str], log_level: IntLoggingLevelType) -> None:
    with tempfile.NamedTemporaryFile('w+') as log_file:
        command = 'pip download ' + ' '.join(packages) + ' --no-deps'
        if directory:
            command += f' -d {directory}'
        command += pip_log_flags(log_file.name, log_level)
        log(f'Running a command {command}', log_level, 5)
        os.system(command)


def extract_wheels(save_wheel: bool, save_dist_info: bool, packages: list[str],
                   directory: Optional[str], log_level: IntLoggingLevelType) -> None:
    dir_ = directory or os.getcwd()
    for filename in glob.glob('*.whl', root_dir=dir_):
        with zipfile.ZipFile(filename) as wheel:
            log(f'Extracting {filename}', log_level)
            if not save_dist_info:
                for file_info in wheel.infolist():
                    if '.dist-info' in file_info.filename or file_info.filename.endswith('.dist-info/RECORD'):
                        continue
                    wheel.extract(file_info, dir_)
            else:
                wheel.extractall(dir_)
            log(f'Extracted {filename} to {dir_}', log_level)
        if not save_wheel:
            os.remove(filename)
            log(f'Removed {filename}', log_level)
    log(f'Successfully extracted {" ".join(packages)}', log_level)


def main():
    # global packages, log_level, directory
    parser = ArgumentParser()
    parser.add_argument('packages', nargs='+', type=str, help='packages to download')
    parser.add_argument('--version', '-v', action='version', version=__version__)
    parser.add_argument('--directory', '-d', type=str, help='directory for unpacking')
    parser.add_argument('--logging-level', '--log-level', '--loglevel', '--log',
                        '--verbosity', '-l', '-V', type=logging_level, dest='logging_level',
                        default=4, help='logging level')
    parser.add_argument('--save-wheel', '-s', '-w', action='store_true', help='save .whl files')
    parser.add_argument('--save-dist-info', '-i', action='store_true', help='save .dist-info directory')

    args = parser.parse_args()
    packages = args.packages
    log_level = args.logging_level
    directory = args.directory

    if log_level < 3:
        warnings.filterwarnings('ignore')

    try:
        download_wheels(packages, directory, log_level)
        extract_wheels(args.save_wheel, args.save_dist_info, packages, directory, log_level)
    except Exception as error:
        if log_level == 0:
            pass
        elif log_level == 1:
            print(f'{error.__class__.__name__}: {error}')
        else:
            raise error
        exit(1)


if __name__ == '__main__':
    main()
