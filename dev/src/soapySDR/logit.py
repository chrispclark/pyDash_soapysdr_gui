#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 16:31:18 2022

@author: chrissy
"""
import sys
from functools import partialmethod

from loguru import logger


def only_level(level):
    def is_level(record):
        return record["level"].name == level

    return is_level


logger.info("Logging 1")
logger.remove()  # Remove all handlers added so far, including the default one.
logger.info("Logging 2")
logger.add(sys.stdout, level="TRACE", filter=only_level("TRACE"))
logger.add(sys.stdout, level="INFO", filter=only_level("INFO"))
logger.add(sys.stdout, level="DEBUG", filter=only_level("DEBUG"))
logger.add(sys.stdout, level="SUCCESS", filter=only_level("SUCCESS"))
logger.add(sys.stdout, level="WARNING", filter=only_level("WARNING"))
logger.add(sys.stdout, level="CRITICAL", filter=only_level("CRITICAL"))

logger.info("INFO")
logger.trace("TRACE")
logger.debug("DEBUG")
logger.success("SUCCESS")
logger.warning("WARNING")
logger.critical("CRITICAL")

try:
    new_level = logger.level("Event", no=6, color="<yellow>", icon="🐍")
    logger.add(
        "logfile.log",
        filter=lambda record: record["level"].name == "Event",
        format="{time:YYYY-MM-DD HH:mm:ss} |{level} | {name}:{function} {line} {message}",
        rotation="5 MB",
    )
except:
    logger.info("Level Event already exists")

try:
    new_level = logger.level("Failure", no=47, color="<yellow>", icon="🐍")
    logger.add(
        "failure.log",
        filter=lambda record: record["level"].name == "Failure",
        format="{time:YYYY-MM-DD HH:mm:ss} |{level} | {name}:{function} {line} {message}",
        rotation="5 MB",
    )
except:
    logger.info("Level Failure already exists")

try:
    new_level = logger.level("Message", no=45, color="<yellow>", icon="🐍")
    logger.add(
        "message.log",
        filter=lambda record: record["level"].name == "Message",
        format="{time:YYYY-MM-DD HH:mm:ss} |{level} | {name}:{function} {line} {message}",
        rotation="5 MB",
    )
except:
    logger.info("Level Message already exists")

try:
    new_level = logger.level("Changes", no=46, color="<yellow>", icon="🐍")
    logger.add(
        "changes.log",
        filter=lambda record: record["level"].name == "Changes",
        format="{time:YYYY-MM-DD HH:mm:ss} |{level} | {name}:{function} {line} {message}",
        level="Changes",
        rotation="5 MB",
    )
except:
    logger.info("Level Changes already exists")

logger.__class__.Failure = partialmethod(logger.__class__.log, "Failure")
logger.__class__.Event = partialmethod(logger.__class__.log, "Event")
logger.__class__.Changes = partialmethod(logger.__class__.log, "Changes")
logger.__class__.Message = partialmethod(logger.__class__.log, "Message")
logger.info("Logging 4")
# logger.add("logfile.log", level="Event")
# logger.__class__.Event = partialmethod(logger.__class__.log, "Event")
# logger.log("Event", "Here we go!")
logger.info("no write")
# print(new_level)
logger.Message("test message")
logger.Changes("test ch")
logger.Failure("failed")
logger.add("special.log", filter=lambda record: "special" in record["extra"])
