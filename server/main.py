"""This is the main file for server, it sets up indexer and web API"""
import argparse
from io import TextIOWrapper
import pathlib
import threading
import logging

from server.indexxocore import Indexxo
from server.indexxoweb import IndexxoServer
from server.settings import IndexxoSettings
from server.filetypes import filetypes


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--run",
                        help="Run Indexxo server.",
                        action="store_true")
    parser.add_argument("--config", type=str,
                        help="Update config.json and exit.")
    parser.add_argument("--get-config",
                        help="Generate config.json and exit.",
                        action="store_true")
    parser.add_argument("--debug",
                        help="Switch logger to DEBUG level.",
                        action="store_true")

    args = parser.parse_args()
    settings = IndexxoSettings()

    # Set logging level
    logging.basicConfig(
        format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s",
        level=logging.DEBUG if args.debug else logging.INFO
    )

    if args.config:
        # Update internal config.json and exit

        logging.info("Updating config file with provided file")
        new_config_data: TextIOWrapper = open(args.config)
        settings.update_config_file(new_config_data)
        logging.info(
            f"Config file is has just been updated, see: {settings.config_path}")
        exit(0)
    elif args.get_config:
        logging.info("Generating config.json here")
        settings.get_config_file()
        logging.info("config.json was generated")

    # Loading server configuration
    settings.load_config_file()

    # Setting up Indexxo indexer
    indexxo = Indexxo(
        # Loading file that contains mapping of extension and file types
        filetypes=filetypes,
        # Setting space paths that will be indexed after server start
        space_paths=[pathlib.Path(p) for p in settings.space_paths],
        # Paths to ignore
        ignore_paths=[pathlib.Path(p) for p in settings.ignore_paths],
        # Providing user specified update interval
        refresh_interval=settings.update_interval
    )

    # Indexing runs on it's own thread
    threading.Thread(target=indexxo.start_indexing, daemon=True).start()
    # Starting WEB API
    IndexxoServer(indexxo).run_server()
