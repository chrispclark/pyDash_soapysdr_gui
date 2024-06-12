#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 15:39:15 2021.

@author: chrissy
"""
# Python program showing
# file management using
# context manager
# from loguru import logger


class LogManager:
    """
    Summary.

    Returns
    -------
    None.

    """

    def __init__(self, filename, mode):
        """
        Summary.

        Returns
        -------
        None.

        """
        self.filename = filename
        self.mode = mode
        self.file = None
        # logger.info("file init")

    def __enter__(self):
        """
        Summary.

        Returns
        -------
        None.

        """
        # logger.info("file enter")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Summary.

        Returns
        -------
        None.

        """
        # logger.info("file exit")
        self.file.close()


if __name__ == "__main__":
    with LogManager("logfile.txt", "a") as f:
        f.write("Test")
    print(f.closed)
    with LogManager("logfile.txt", "r") as f:
        read_data = f.read()
    print(read_data)
