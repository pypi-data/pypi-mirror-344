import argparse
import os
import sys
from typing import Dict, Any

from pyqt6rc import __version__
from pyqt6rc.convert_tools import (
    ui_to_py,
    modify_py,
    save_py,
    get_ui_files,
    update_resources,
)
from pyqt6rc.script_helpers import set_logger

description = [
    f"pyqt6rc v{__version__}",
    "PyQt6 UI templates - Resource Converter.",
    "Default input location is Current Working Directory.",
    "",
    "Usage examples:",
    "  Convert all .ui files in CWD:",
    "  pyqt6rc",
    "",
    "  Convert all .ui files in CWD using importlib_resources:",
    "  pyqt6rc -c",
    "",
    "  Convert all .ui files in directory:",
    "  pyqt6rc -i /directory/with/templates",
    "",
    "  Convert all .ui files in CWD, save output in different directory:",
    "  pyqt6rc -o /directory/with/converted/templates",
    "",
]

arguments = sys.argv
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter, description="\r\n".join(description)
)
parser.add_argument(
    "input",
    type=str,
    help="Path to .ui template file or Directory containing .ui files."
    "If empty, scan current working directory and use all .ui template files.",
    default="*",
    nargs="?",
)
parser.add_argument(
    "-tb", "--tab_size", type=int, help="Size of tab in spaces, default=4", default=4
)
parser.add_argument(
    "-o",
    "--out",
    type=str,
    help="Output directory to save converted templates",
    default=None,
)
parser.add_argument("-s", "--silent", help="Supress logging", action="store_true")
parser.add_argument(
    "-c",
    "--compatible",
    help="Use compatible importlib_resources instead of native importlib."
    "Requires importlib_resources.",
    action="store_true",
)
args = parser.parse_args()

# Set logger
set_logger(args.silent)

# Input files check
if args.input == "*":
    input_files = get_ui_files(os.getcwd())
elif os.path.isdir(args.input):
    input_files = get_ui_files(args.input)
else:
    if not args.input.endswith(".ui"):
        raise Exception(f"Not template file {args.input}.")
    if not os.path.exists(args.input):
        raise Exception(f"Template file {args.input} does not exists.")
    input_files = [args.input]


def run() -> None:
    resources: Dict[str, Any] = {}
    for input_file in input_files:
        current_resources = update_resources(input_file, resources)
        py_input = ui_to_py(input_file)
        # Do conversion only when resources are found in current ui file
        if current_resources["qrc_info"]:
            py_input = modify_py(py_input, resources, args.tab_size, args.compatible)
        save_py(input_file, py_input, args.out)
