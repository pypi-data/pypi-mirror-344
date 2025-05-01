import os
import random
import re
import unicodedata
import numpy as np
import torch
from tsimpute.core.logger import log, Color


def global_seed(seed: int = None):
    if seed is None:
        random.seed()
        np.random.seed()
        torch.manual_seed(torch.seed())
        torch.cuda.manual_seed_all(torch.seed())
    else:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    if torch.cuda.is_available():
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def _accelerate_device_verbose(msg: str):
    '''
    Print verbose message for device acceleration
    '''
    log.debug(f"{Color.bold}[Device]{Color.reset} {msg}")


def get_accelerate_device() -> torch.device:
    '''
    Get accelerate device based on cuda priority
    '''
    prefer_cuda = os.getenv("PREFER_CUDA", "True") == "True"
    device = "cpu"

    if not prefer_cuda:
        _accelerate_device_verbose("CUDA is not preferred, using CPU instead")
        return torch.device(device)

    if torch.cuda.is_available():
        device = "cuda"
        _accelerate_device_verbose(
            f"CUDA is available, using GPU {torch.cuda.get_device_name()}")
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        device = "mps"
        _accelerate_device_verbose("MPS is available, using Apple's MPS")
    else:
        _accelerate_device_verbose(
            "CUDA, MPS is not available, using CPU instead")
    return torch.device(device)


def get_table_summary(
    name: str,
    data: list[list[str]],
    cols: list[str],
    max_length: int = 20
) -> str:
    """
    Generate a table as a string.
    """
    # Calculate max padding
    max_padd = [len(col) for col in cols]
    for row in data:
        for i, col in enumerate(row):
            if len(str(col)) > max_length:
                max_padd[i] = max_length
            elif len(str(col)) > max_padd[i]:
                max_padd[i] = len(str(col))

    # Trim data
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if len(str(col)) > max_length:
                data[i][j] = str(col)[:max_length - 3] + '...'

    # Build the table
    table = []

    # Top border
    table.append(
        '┌' + '┬'.join('─' * (max_padd[i] + 2) for i in range(len(cols))) + '┐')

    # Column headers
    table.append(
        '│' + '│'.join(f' {cols[i]}{" " * (max_padd[i] - len(str(cols[i])))} ' for i in range(len(cols))) + '│')

    # Divider
    table.append(
        '├' + '┼'.join('─' * (max_padd[i] + 2) for i in range(len(cols))) + '┤')

    # Content rows
    for row in data:
        table.append(
            '│' + '│'.join(f' {row[i]}{" " * (max_padd[i] - len(str(row[i])))} ' for i in range(len(cols))) + '│')

    # Bottom border
    table.append(
        '└' + '┴'.join('─' * (max_padd[i] + 2) for i in range(len(cols))) + '┘')

    return f'Model {name} summary:\n' + '\n'.join(table)


def slugnify(text: str, separator: str = "-") -> str:
    """
    Convert a string to a slug-safe format for directory names and URLs.
    :param text: The input string to be converted.
    :param separator: The character used to replace spaces and special characters (default is '-').
    :return: A slugified string safe for directories and URLs.
    """
    # Normalize Unicode characters
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    # Replace non-alphanumeric characters with separator
    text = re.sub(r'[^a-zA-Z0-9]+', separator, text)

    # Remove leading/trailing separators
    text = text.strip(separator)

    # Ensure only single occurrences of the separator
    text = re.sub(rf'{separator}+', separator, text)

    return text.lower()


GLOBAL_PROPERTIES = {}
