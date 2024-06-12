from dash import Input, Output, callback
from shared_memory_dict import SharedMemoryDict

from logtofile import LogManager

smd = SharedMemoryDict(name="smd", size=1000)


def my_cleanup(name):
    print("my_cleanup(%s)" % name)


colors = {"background": "rgb(50, 50, 50)", "text": "#FFFFFF"}


def get_callbacks_logs():
    """
    Summary.

    Args:
        app (TYPE): DESCRIPTION.

    Returns:
        TYPE: DESCRIPTION.

    """


# -----------------------   Update the log view   ----------------------- #
@callback(
    Output("Changes_log", "value"),
    Input("log-interval", "n_intervals"),
)
def update_output(value) -> str:
    """
    Display the log file for any host changes.

    Returns
    -------
    A reversed list of entries, so the latest updates are at the top.

    """
    with LogManager("message.log", "r") as log_file:
        lines = log_file.readlines()
    lines = reversed(lines)
    logs = "".join(map(str, lines))
    return logs
