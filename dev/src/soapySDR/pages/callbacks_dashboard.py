from dash import (
    Input,
    Output,
    html,
    callback,
    ctx,
)
from startSDR import RunSDRlocal
from SDRConfigs import QueueConfigs
from SDRConfigs import SoundConfigs

# from SDRConfigs import SharedMemoryDict
from UltraDict import UltraDict

# import plotly.express as px
# from logit import logger
from loguru import logger
from datetime import datetime

run_sdr = RunSDRlocal()
queue_config = QueueConfigs()
command_queue_to_sdr = queue_config.command_queue_to_sdr
logger.info(command_queue_to_sdr)
command_queue_from_sdr = queue_config.command_queue_from_sdr

# z = SharedMemoryDict()
ultra = UltraDict(name="sdr")
logger.info(ultra)

logger.info(f"to sdr {command_queue_to_sdr}")
logger.info(f"from sdr {command_queue_from_sdr}")

ultraQsizes = UltraDict(name="ultraQsizes")
ultraSDRstatus = UltraDict(name="sdr_status")
ultraSDRSounds = UltraDict(mute=False, name="ultraSound")
sound_config = SoundConfigs
soundq = ultraQsizes["soundq"]
commands = UltraDict(name="commands_for_sdr")


def get_callbacks_dashboard():

    @callback(
        Output(component_id="spanner", component_property="children"),
        Input(component_id="load_interval", component_property="n_intervals"),
    )
    def update_spanner(n_intervals: int):
        logger.info(ctx.triggered)
        logger.info(datetime.now())
        is_sdr_running = ultraSDRstatus["SDRRunning"]
        logger.info(is_sdr_running)
        logger.info(type(run_sdr))
        if not is_sdr_running:
            ultraSDRstatus["SDRRunning"] = True
            run_sdr.run()
        else:
            msg = "SDR Already Running"
        logger.info(msg)
        # return datetime.now()

    #########################################
    # Update The Settings Table             #
    #########################################
    @callback(
        Output("SDRsettings", "data"),
        [Input("SDRsettings-interval", "n_intervals")],
    )
    def update_output(n_intervals):
        z = ultraSDRstatus
        # logger.info(z)
        # logger.info(ultra['status'])

        r = SoundConfigs.ultraSoundStatus
        r["soundstatus"] = "test"

        status = "Stopped"
        if ultraSDRstatus["SDRRunning"]:
            status = "Running"
        else:
            status = "Stopped"

        data_list = [
            {"Field": "Status", "Value": status},
            {"Field": "freq", "Value": z["freq"]},
            {"Field": "samp", "Value": z["samp"]},
            {"Field": "bandwidth", "Value": z["bandwidth"]},
            {"Field": "gain", "Value": z["gain"]},
            {"Field": "mtu", "Value": z["mtu"]},
            # {"Field": "soundQ", "Value": ultraQsizes["soundq"]},
            {"Field": "soundQ", "Value": ultra["sound"]["soundq"]},
            {"Field": "sound Status", "Value": r["soundstatus"]},
            {"Field": "Environment", "Value": ultra["status"]["live_dev"]},
        ]
        return data_list

    #########################################
    # Draw the Power Spectral Density Graph #
    #########################################
    @callback(
        Output("draw_graph", "figure"),
        [Input("graph_interval", "n_intervals")],
    )
    def update_graph_live(n_intervals):
        graph_figure = UltraDict(name="ultraSDRGraph")
        figure = graph_figure["figure"]
        # logger.info(figure)
        # logger.info(type(figure))
        return figure

    """
    #########################################
    # Draw the Power Spectral Density Graph #
    #########################################
    @callback(
        Output('draw_graph', 'figure'), [Input('graph_interval', 'n_intervals')]
    )
    def update_graph_live(n_intervals):
        #graph_figure = UltraDict(name='ultraSDRGraph')
        logger.info(ultraSDRGraph)
        freq = ultraSDRGraph['frequency']
        logger.info(freq)
        buffer = ultraSDRGraph['sdr_buffer']
        # logger.info(buffer)
        (f_c, S) = signal.periodogram("soundq-interval"
            buffer,
            1e6,
            scaling='density',
            return_onesided=False,
        )
        # logger.info(f_c)
        # logger.info(S)
        figure = px.line(
            x=f_c,
            y=S,
        )

        #figure = graph_figure['figure']
        figure.update_layout(
            title='Power Spectral Density',
            xaxis_title=f'Frequency11 {freq / 1000000} MHz)',
            yaxis_title='Relative power (dB)',
        )
        logger.info(figure)
        return figure
    """

    #########################################
    # Capture output from frequency slider  #
    # or the up / down buttons              #
    # Update the frequency slider value     #
    #########################################
    @callback(
        [
            Output("freq-slider1", "value"),
        ],
        Input("freq-slider1", "value"),
    )
    def displayClick1(value):
        # x= startRTLSDR(sdr)
        logger.info("click freq")
        logger.info(value)
        # x.getFreq() # "None of the buttons have been clicked yet"
        freq_value = value * 10**6
        logger.info(freq_value)
        led_value = f"{value: .2f}"
        logger.info(led_value)
        p = 102.2e6
        logger.info(p)
        command_dict = {"set_frequency": freq_value}
        # command_dict = {'set_frequency': 102.2e6}
        logger.info(f"putting command {command_dict}")
        commands["command_to_sdr"] = command_dict
        # command_queue_to_sdr.put(command_dict)
        # logger.info(f" commadn q size {command_queue_to_sdr.qsize()} {command_queue_to_sdr}")
        # logger.info(f"command q id {id(command_queue_to_sdr)}")
        return [value]

    """
    @callback(
        [
            Output("container-button-freq-dwn", "children"),
            Output("freq-slider", "value"),
            Output("led_freq", "value"),
        ],
        Input("freq-slider", "value"),
        Input("btn-dwn", "n_clicks"),
        Input("btn-up", "n_clicks"),
    )
    def displayClick1(value, btn1, btn2):
        # x= startRTLSDR(sdr)
        logger.info("click freq")
        logger.info(value)
        # x.getFreq() # "None of the buttons have been clicked yet"
        if "btn-dwn" == ctx.triggered_id:
            value = value - 0.1
            value = round(value, 1)
            msg = "Down freq"
            logger.info(msg)
        if "btn-up" == ctx.triggered_id:
            value = value + 0.1
            value = round(value, 1)
            msg = "Up freq"
            logger.info(msg)
        freq_value = value * 10**6
        logger.info(freq_value)
        led_value = f"{value:.2f}"
        logger.info(led_value)
        p = 102.2e6
        logger.info(p)
        command_dict = {"set_frequency": freq_value}
        # command_dict = {'set_frequency': 102.2e6}
        logger.info(f"putting command {command_dict}")
        command_queue_to_sdr.put(command_dict)
        logger.info(f" commadn q size {command_queue_to_sdr.qsize()}")
        logger.info(command_queue_to_sdr)

        return [
            "",
            value,
            str(led_value),
        ]

    #########################################
    # get the sample rate from the SDR      #
    #########################################
    @callback(
        Output("SDRSampleRateDiv", "children"), Input("SDRSampleRate", "value")
    )
    def update_value(value):
        logger.info("here")
        command_dict = {"get_samplerate": 2.5e6}
        command_queue_to_sdr.put(command_dict)
        logger.info(command_queue_from_sdr.qsize())
        led_value = f"{value:.2f}"
        logger.info(led_value)
        return str(led_value)


    #########################################
    # Get output from frequency slide and   #
    # Update the led display                #
    #########################################
    @callback(Output('led_freq', 'value'), Input('freq-slider', 'value'))
    def update_led_output(value):
        led_value = f'{value:.2f}'
        logger.info(led_value)
        return str(led_value)
    """

    """
    #########################################
    # Triggered by 'soundq-interval get the #
    # size of the current audio queue which #
    # is held in a ultraDict shared memory  #
    #########################################
    @callback(Output("soundq", "value"), Input("soundq-interval", "n_intervals"))
    def update_led_output(value):
        led_value = f"{value:.2f}"
        queueSize = ultraQsizes["soundq"]
        # logger.info(queueSize)
        return str(queueSize)
    """

    #########################################
    # Capture pre-programmed buttons        #
    # too star SDR or switch to a channel   #
    #########################################
    @callback(
        Output("container-button-layout", "children"),
        Input("btn-smooth", "n_clicks"),
        Input("btn-lbc", "n_clicks"),
        Input("btn-flex", "n_clicks"),
        Input("btn-startSDR", "n_clicks"),
        Input("standalone-switch", "value"),
        # Input('btn-startSDR', 'n_clicks'),
        # Input('btn_freq_down', 'down_value')
    )
    def displayClick(btn1, btn2, btn3, btn4, value):
        # x= startRTLSDR(sdr)

        msg = "Hello"
        logger.info("click")
        # x.getFreq() # "None of the buttons have been clicked yet"
        if "btn-startSDR" == ctx.triggered_id:
            # msg = 'SDR start Button 3 was most recently clicked'
            pass
        elif "btn-smooth" == ctx.triggered_id:
            command_dict = {"set_frequency": 102.2e6}
            logger.info(f"sending {command_dict}")
            commands["command_to_sdr"] = command_dict
            # command_queue_to_sdr.put(command_dict)
            msg = "Button 1 was most recently clicked"
            logger.info(msg)
        elif "btn-flex" == ctx.triggered_id:
            command_dict = {"set_frequency": 153.025e6}
            logger.info(f"sending {command_dict}")
            # command_queue_to_sdr.put(command_dict)
            commands["command_to_sdr"] = command_dict
            msg = "Button Flex was most recently clicked"
            logger.info(msg)
        elif "btn-lbc" == ctx.triggered_id:
            command_dict = {"set_frequency": 97.3e6}
            logger.info(f"sending {command_dict}")
            commands["command_to_sdr"] = command_dict
            msg = "Button lbc was most recently clicked"
            logger.info(msg)
        elif "btn-freq_down" == ctx.triggered_id:
            msg = "Button Down was most recently clicked"
            logger.info(msg)
        elif "standalone-switch" == ctx.triggered_id:
            msg = "Switch Mute was most recently clicked"
            logger.info(value)
            if value:
                ultraSDRSounds["mute"] = True
            else:
                ultraSDRSounds["mute"] = False
            logger.info(msg)

        return html.Div(msg)
