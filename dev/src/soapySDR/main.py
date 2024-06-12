# -*- coding: utf-8 -*-
import atexit
import os
import pathlib
import sys
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from loguru import logger
from UltraDict import UltraDict
from SDRConfigs import SoundConfigs, SharedMemoryDict
from waitress import serve

external_stylesheets = [dbc.themes.FLATLY]

pyver = (
    f"python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
)

logger.info(pyver)


z = SharedMemoryDict()
p = z.CreateSharedMemoryDict()
logger.info(p.name)

logger.info(SharedMemoryDict)
ultra = UltraDict(name=p.name)
logger.info(ultra)
logger.info(ultra["commands"]["counter"])
logger.info(ultra["commands"]["fred"])
ultra["commands"]["counter"] = 40
ultra["commands"]["fred"] = 20
logger.info(ultra["commands"]["counter"])
logger.info(ultra["commands"]["fred"])
logger.info(ultra["graph"])
logger.info(ultra["status"])
logger.info(ultra["status"]["live_dev"])
logger.info(ultra["sound"]["status"])
logger.info(ultra["sound"]["soundq"])


sound_q_status = SoundConfigs.ultraSoundStatus
sound_q_status["soundstatus"] = "test"

ultraSDRGraph = UltraDict(name="ultraSDRGraph")
ultraSDRGraph["figure"] = {}
ultraSDRGraph["frequency"] = "97.3"
ultraQsizes = UltraDict(name="ultraQsizes")
ultraQsizes["soundq"] = 0

ultraSDRstatus = UltraDict(name="sdr_status")
ultraSDRstatus["freq"] = "97.3"
ultraSDRstatus["samp"] = "0"
ultraSDRstatus["gain"] = "0"
ultraSDRstatus["mtu"] = "0"
ultraSDRstatus["SDRRunning"] = False

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
)

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Link(
                    "Dashboard ",
                    href=dash.page_registry["pages.layout_dashboard"]["path"],
                    className="tab",
                ),
                dcc.Link(
                    "Logs",
                    href=dash.page_registry["pages.logs.layout_logs"]["path"],
                    className="tab first",
                ),
            ],
            # className="row all-tabs",
        ),
        dash.page_container,
    ]
)


def exit_handler():
    """
    Summary.

    Returns:
        None.

    """
    logger.info("My application is ending!")
    logger.info("All tidy!")
    atexit.register(exit_handler)


def startdash() -> None:
    """Start the Dash service."""
    logger.info((pathlib.Path().absolute().as_posix()))
    if "live" in (pathlib.Path().absolute().as_posix()):
        logger.info("start live")
        logger.info(ultra)
        ultra["status"] = {"live_dev": "Live Environment"}
        serve(app.server, host="192.168.1.77", port=8058, threads=8)
    elif "dev" in (pathlib.Path().absolute().as_posix()):
        logger.info("start dev")
        ultra["status"] = {"live_dev": "Dev Environment"}
        logger.info(ultra)
        app.run_server(
            debug=True,
            dev_tools_ui=True,
            dev_tools_serve_dev_bundles=True,
            dev_tools_props_check=True,
            port="8065",
            threaded=True,
            host="192.168.1.77",
            use_reloader=False,
        )
    else:
        logger.info("no ports found")
        ultra["status"]["live_dev"] = "Unknown, no ports match"
        # quit()
        sys.exit()
    logger.info(ultra)


if __name__ == "__main__":
    logger.success("")
    logger.success("----------------------------------------")
    logger.success("-------- Main Function Starting --------")
    logger.success("----------------------------------------")
    logger.success("")

    try:
        startdash()
        # main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
