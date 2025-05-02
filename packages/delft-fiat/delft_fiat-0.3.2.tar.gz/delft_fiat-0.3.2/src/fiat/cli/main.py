"""Cli of FIAT."""

import argparse
import importlib
import sys
from multiprocessing import freeze_support

from fiat.cfg import Configurations
from fiat.check import check_config_entries
from fiat.cli.action import KeyValueAction
from fiat.cli.formatter import MainHelpFormatter
from fiat.cli.util import file_path_check, run_log, run_profiler
from fiat.log import check_loglevel, setup_default_log
from fiat.models import GeomModel, GridModel
from fiat.util import (
    MANDATORY_GEOM_ENTRIES,
    MANDATORY_GRID_ENTRIES,
    MANDATORY_MODEL_ENTRIES,
)
from fiat.version import __version__

_models = {
    "geom": {"model": GeomModel, "input": MANDATORY_GEOM_ENTRIES},
    "grid": {"model": GridModel, "input": MANDATORY_GRID_ENTRIES},
}

fiat_start_str = """
###############################################################

        #########    ##          ##      ##############
        ##           ##         ####         ######
        ##           ##         ####           ##
        ##           ##        ##  ##          ##
        ######       ##        ##  ##          ##
        ##           ##       ########         ##
        ##           ##      ##      ##        ##
        ##           ##     ##        ##       ##
        ##           ##    ##          ##      ##

###############################################################

                Fast Impact Assessment Tool
                \u00a9 Deltares

"""


# Info function
def info(args):
    """Show an info string."""
    sys.stdout.write(fiat_start_str)
    sys.stdout.write(
        """This tool is meant for quick impact assessment.

It is open source and meant to be used and implemented as such.
Therefore it is available under the MIT license.\n"""
    )


# Run FIAT function
def run(args):
    """Run the model from cli."""
    # Setup the logger, first without a file
    logger = setup_default_log(
        "fiat",
        level=2,
    )
    sys.stdout.write(fiat_start_str)

    # Setup the config reader
    cfg = file_path_check(args.config)
    cfg = run_log(Configurations.from_file, logger, cfg)

    # Set the threads is specified
    if args.threads is not None:
        assert int(args.threads)
        cfg.set("global.threads", int(args.threads))

    if args.set_entry is not None:
        cfg.update(args.set_entry)
    cfg.setup_output_dir()

    # Complete the setup of the logger
    loglevel = check_loglevel(cfg.get("global.loglevel", "INFO"))
    logger.add_file_handler(
        dst=cfg.get("output.path"),
        filename="fiat",
    )
    logger.level = loglevel

    # Add the model version
    logger.info(f"Delft-Fiat version: {__version__}")

    # Kickstart the model
    model_type = cfg.get("global.model", "geom")
    check_config_entries(
        cfg.keys(),
        MANDATORY_MODEL_ENTRIES + _models[model_type]["input"],
    )
    obj = _models[model_type]["model"](cfg)
    if args.profile is not None:
        run_profiler(obj.run, profile=args.profile, cfg=cfg, logger=logger)
    else:
        run_log(obj.run, logger=logger)


## Constructing the arguments parser for FIAT.
def args_parser():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(
        #    usage="%(prog)s <options> <commands>",
        add_help=False,
        formatter_class=MainHelpFormatter,
    )
    # Help parser
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit",
    )
    # Version parser
    version_build_str = ""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        mod = importlib.import_module("fiat_build_time")
        version_build_str += f", build {mod.BUILD_TIME}"
    parser.add_argument(
        "--version",
        action="version",
        version=f"FIAT {__version__}{version_build_str}\n",
        help="Show the version number",
    )

    # The supparser setup
    subparser = parser.add_subparsers(
        title="Commands",
        dest="command",
        metavar="<commands>",
    )

    # Set everything for the info command
    info_parser = subparser.add_parser(
        name="info",
        help="Information concerning Delft-FIAT",
        formatter_class=MainHelpFormatter,
    )
    info_parser.set_defaults(func=info)

    # Set everything for the run command
    run_parser = subparser.add_parser(
        name="run",
        help="Run Delft-FIAT via a settings file",
        formatter_class=MainHelpFormatter,
        # usage="%(prog)s subcommand1 [options] sub1_arg"
    )
    run_parser.add_argument(
        "config",
        help="Path to the settings file",
    )
    run_parser.add_argument(
        "-t",
        "--threads",
        metavar="<THREADS>",
        help="Set number of threads",
        type=int,
        action="store",
        default=None,
    )
    run_parser.add_argument(
        "-d",
        "--set-entry",
        metavar="<KEY=VALUE>",
        help="Overwrite entry in settings file",
        action=KeyValueAction,
    )
    run_parser.add_argument(
        "-q",
        "--quiet",
        help="Decrease output verbosity",
        action="count",
        default=0,
    )
    run_parser.add_argument(
        "-v",
        "--verbose",
        help="Increase output verbosity",
        action="count",
        default=0,
    )
    run_parser.add_argument(
        "-p",
        "--profile",
        help="Run profiler",
        action="store_const",
        const="profile",
    )
    run_parser.set_defaults(func=run)
    return parser


## Main entry point: parsing gets done here
def main(argv=sys.argv[1:]):
    """Execute main cli function."""
    parser = args_parser()
    args = parser.parse_args(args=None if argv else ["--help"])
    args.func(args)


if __name__ == "__main__":
    freeze_support()
    main()
