# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 13:50:11 2021

@author: chrissy
"""
import pathlib
import socket
from datetime import datetime

# from logit import logger
import psutil
import tomli
from loguru import logger
from plyer import notification

# logger.getLogger("sqlalchemy.engine").setLevel(loggier.ERROR)

SQLALCHEMY_DATABASE_URI: str = "sqlite:///hoststatus.db"

logit = False
# logger.add(sys.stderr)


class GeneralFunctions:
    @staticmethod
    def datetimestring(timeanddate) -> str:
        if timeanddate:
            return f"{datetime.now():%d/%m/%Y %H:%M:%S}"
        else:
            return f"{datetime.now(): %H:%M:%S}"

    @staticmethod
    def getconnectionstring():
        # logger.info(pathlib.Path().absolute().as_posix())
        with open("config.toml", "rb") as fileObj:
            toml_config = tomli.load(fileObj)

        # toml_config: dict = toml.load("config.toml")
        if "dev" in (pathlib.Path().absolute().as_posix()):
            SQLALCHEMY_DATABASE_URI = toml_config["database dev"][
                "SQLALCHEMY_DATABASE_URI"
            ]
        elif "live" in (pathlib.Path().absolute().as_posix()):
            SQLALCHEMY_DATABASE_URI = toml_config["database live"][
                "SQLALCHEMY_DATABASE_URI"
            ]
        else:
            SQLALCHEMY_DATABASE_URI = "Not A Live Or Dev System"
        return SQLALCHEMY_DATABASE_URI

    @staticmethod
    def send_notification(title, message):
        notification.notify(title, message, timeout=1)

    '''
    @staticmethod
    def log_only(filename, mode, alert):
        """
        Summary.

        Details.
        """
        with LogManager(filename, mode) as log_file:
            log_file.write(alert)
            log_file.write("\n")

    @staticmethod
    def log_and_notify(filename, mode, alert):
        """
        Summary.

        Returns:
            None.

        """
        dt_string: str = GeneralFunctions.datetimestring(True)
        with LogManager(filename, mode) as log_file:
            """log_file.write(dt_string + ' Moved to down: ' + alert)"""
            log_file.write(alert)
            log_file.write("\n")
        if "dev" in (pathlib.Path().absolute().as_posix()):
            GeneralFunctions.send_notification("ALERT - dev", alert)
        elif "live" in (pathlib.Path().absolute().as_posix()):
            GeneralFunctions.send_notification("ALERT - live", alert)
    '''

    @staticmethod
    def get_ip_address(hostname):
        try:
            ipaddress = socket.gethostbyname(hostname)
        except socket.gaierror:
            ipaddress = "0.0.0.0"
        return ipaddress

    @staticmethod
    def validate_ip_address(ipaddress):
        try:
            return socket.gethostbyaddr(ipaddress)
        except socket.error:
            return None, None, None

    def killprocess(self: object, process_name: str) -> int:
        """
        Kill a named process.

        Called when the mainwindow is closed, just to close rtl_udp process.
        Otherwise it will stay open and when the app is run next time it will
        try to start rtl_udp again, even though it was still running.

        Returns
        -------
        0 for fail 1 for success.

        """
        process_id = GeneralFunctions.checkifprocessrunning(self, process_name)
        # f = f"process_id: {process_id} Killed"fs
        if process_id is None or (process_id == 0):
            logger.warning("No process found to kill - good")
            return 1
        else:
            # self.mylog.append_log(f"Killed: {process_name}")
            logger.warning("Killed: {proc}", proc=process_name)
            psutil.Process(process_id).kill()
        return 0

    @staticmethod
    def checkifprocessrunning(self: object, process_name: str) -> int:
        """
        Check if process is running.

        Used to check status of rtl_udp

        Returns
        -------
        The PID of the running process, or 0 if not found

        """
        for proc in psutil.process_iter():
            try:
                # Get process name & pid & cmd line from process object.
                processID = proc.pid
                if process_name in proc.name():
                    return processID
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                pass
        return 0


if __name__ == "__main__":
    z = GeneralFunctions.validate_ip_address("fred")
