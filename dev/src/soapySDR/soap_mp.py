# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 13:22:43 2023

@author: chrissy

Get more usb 'usbcore.usbfs_memory_mb=256'
"""
import threading

import numpy as np
import plotly.express as px  # type: ignore
import sounddevice  # type: ignore
from UltraDict import UltraDict  # type: ignore
from loguru import logger
from scipy import signal  # type: ignore

import SoapySDR
from SDRConfigs import QueueConfigs
from SDRConfigs import RadioConfigs
from SDRConfigs import SoundConfigs
from SDRcommands import SDRcommands
from SoapySDR import SOAPY_SDR_CF32, SOAPY_SDR_RX  # SOAPY_SDR_CS16,

ultraSDR = UltraDict(freq="97.3", sample="20000", name="SDRSharedMemoryDict")
ultraSDRGraph = UltraDict(name="ultraSDRGraph")
ultraSDRSounds = UltraDict(name="ultraSound")
ultraQsizes = UltraDict(name="ultraQsizes")
ultraSDRGraph["frequency"] = "97.3"
freq = ultraSDRGraph["frequency"]

commands = UltraDict(name="commands_for_sdr", recursive=True)
SDRDefinitions = UltraDict(name="SDRDefinitions", recursive=True)

config = RadioConfigs()
config_as_dict = vars(config)
logger.info(config_as_dict)
"""
for k, v in config_as_dict.items():
    ultraSDR[k] = v
"""


class runSDR:
    """test."""

    def __init__(self) -> None:
        """test."""
        self.sdr_name = "empty"
        queue_configs = QueueConfigs()
        self.command_queue_to_sdr = queue_configs.command_queue_to_sdr
        self.soundsQ = queue_configs.soundsQ
        # self.samples = np.array([])

    def runit(self) -> None:
        """

        Return.

        -------
        None
            DESCRIPTION.

        """
        config = RadioConfigs()
        devices = GetDevices()
        audio_devices = devices.list_audio_devices
        logger.info(audio_devices)
        self.sdr_name = devices.sdr_devices()
        logger.info(self.sdr_name)
        logger.info(self.soundsQ)
        SDRSamplesThread = ReadSDRSamplesThread(
            self.sdr_name,
            self.soundsQ,
            self.command_queue_to_sdr,
            config,
        )
        SDRSamplesThread.start()
        logger.info(SDRSamplesThread)
        audio = SoundThread(self.soundsQ)
        audio.soundit()


class ReadSDRSamplesThread(threading.Thread):
    """doc"""

    def __init__(
        self, sdr_device, sounds, command_queue_to_sdr, config
    ) -> None:
        """

        Args:
            sdr_device:
            sounds:
            command_queue_to_sdr:
            config:
        """
        threading.Thread.__init__(self)

        self.samples_per_scan = RadioConfigs.samples_per_scan
        self.samples = np.zeros(self.samples_per_scan, dtype=np.complex64)

        self.config = config
        self.soundsQ = sounds
        self.command_queue_to_sdr = command_queue_to_sdr
        logger.info(self.command_queue_to_sdr)
        self.sdr_name = sdr_device

        self.sdr_name.setSampleRate(
            SOAPY_SDR_RX, self.config.rx_chan, self.config.sdr_sample_rate
        )
        self.sdr_name.setFrequency(
            SOAPY_SDR_RX, config.rx_chan, "RF", config.sdr_center_freq
        )
        # set the gains
        self.sdr_name.setGain(SOAPY_SDR_RX, 0, "IF", 5)
        self.sdr_name.setGain(SOAPY_SDR_RX, 0, "LNA", 5)
        self.sdr_name.setGain(SOAPY_SDR_RX, 0, "MIX", 5)
        self.sdr_name.setGainMode(
            SOAPY_SDR_RX, config.rx_chan, config.use_agc
        )  # Set the gain mode

        # enable bias-tee
        self.sdr_name.writeSetting("biastee", "true")
        logger.info(self.sdr_name)

        self.rx_stream = self.sdr_name.setupStream(
            SOAPY_SDR_RX, SOAPY_SDR_CF32, [config.rx_chan]
        )
        logger.info(self.rx_stream)
        self.nb = self.sdr_name.getStreamMTU(self.rx_stream)
        self.sdr_name.activateStream(self.rx_stream)
        self.SDRcommands = SDRcommands(self.sdr_name)

        # create a re-usable buffer for receiving samples

        self.num_left = self.samples_per_scan

        logger.info(self.sdr_name.listAntennas(SOAPY_SDR_RX, 0))
        # self.samplesQ = samples
        # self.samples = samples
        self.stopit = False

        logger.info(self.sdr_name.readStreamStatus(self.rx_stream))
        self.buff = np.zeros(self.nb, dtype=np.complex64)  # This works as well
        logger.info(len(self.buff))
        self.sdr_name.sample_rate = config.sdr_sample_rate
        logger.info(f"Stream MTU set to {self.nb}")

    '''
    def get_status(self) -> UltraDict:
        """
        Returns:

        """
        data_list = SDRcommands.return_get(self)
        logger.info(type(data_list))
        return data_list
    '''

    def demod(self, samples) -> None:
        """

        Args:
            samples:

        Returns:

        """
        # decimate 1/5 from 1.2MHz to 240kHz
        sigif = signal.decimate(samples, 5, ftype="iir")
        # convert to continuous phase angle
        phase = np.unwrap(np.angle(sigif))
        # differentiate phase brings into frequency
        pd = np.convolve(phase, [1, -1], mode="valid")
        # decimate 1/10 from 240kHz to 24kHz
        audio = signal.decimate(pd, 10, ftype="iir")
        audio = np.expand_dims(audio, axis=-1)
        self.soundsQ.append(audio)
        ultraQsizes["soundq"] = len(self.soundsQ)
        return

    def run(self) -> None:
        """_summary_"""
        while not self.stopit:
            """
            ssdr_stream = self.sdr_name.readStream(
                self.rx_stream,
                [self.buff],
                self.nb,
                timeoutUs=self.config.timeout_us,
            )
            """
            num_samples_read = 0
            while num_samples_read < self.samples_per_scan:
                sdr_stream = self.sdr_name.readStream(
                    self.rx_stream,
                    [self.samples[num_samples_read:]],
                    self.samples_per_scan - num_samples_read,
                    timeoutUs=config.timeout_us,
                )
                num_samples_read += sdr_stream.ret
                if sdr_stream.ret <= 0:
                    logger.error(
                        f"Failed to read samples, error code: {sdr_stream.ret}"
                    )
                    break

            self.demod(self.samples)
            """
            (self.f_c, self.S) = signal.periodogram(
                self.samples,
                1e6,
                scaling='density',
                return_onesided=False,
            )
            """
            (self.f_c, self.S) = signal.welch(
                self.samples,
                1e6,
                nperseg=1024,
                return_onesided=False,
            )
            fig = px.line(
                x=self.f_c,
                y=self.S,
            )

            fig.update_layout(
                paper_bgcolor="lightgrey",
                plot_bgcolor="lightgrey",
                title="Power Spectral Density",
                xaxis_title=f"Frequency {self.config.freq / 1000000} MHz)",
                yaxis_title="Relative power (dB)",
            )
            ultraSDRGraph["figure"] = fig
            self.SDRcommands.SDRset_get(commands)
            z = self.SDRcommands.return_get()
            # logger.info(z)
        return


'''
class ProcessThread(threading.Thread):
    """

    """
    def __init__(self, samples, sounds):
        """

        Args:
            samples:
            sounds:
        """
        threading.Thread.__init__(self)
        logger.info("PROCESS THREAD")
        # self.samplesQ = samples
        self.samples = samples
        self.soundsQ = sounds
        self.stopit = False

    """
    def demod(self, samples):
        # decimate 1/5 from 1.2MHz to 240kHz
        sigif = signal.decimate(samples, 5, ftype="iir")
        # convert to continuous phase angle
        phase = np.unwrap(np.angle(sigif))
        # differentiate phase brings into frequency
        pd = np.convolve(phase, [1, -1], mode="valid")
        # decimate 1/10 from 240kHz to 24kHz
        audio = signal.decimate(pd, 10, ftype="iir")
        audio = np.expand_dims(audio, axis=-1)
        self.soundsQ.append(audio)
        # logger.info(self.soundsQ)
        # logger.info(len(self.soundsQ))
        ultraQsizes["soundq"] = len(self.soundsQ)
        logger.info(f'soundsQ {len(self.soundsQ)}')
        # return audio
    """

    def run(self):
        """

        Returns:

        """
        while not self.stopit:
            logger.info(f"demod {self.samples.qsize()}")
'''


class SoundThread:
    def __init__(
        self,
        sounds,
        *args,
        **kwargs,
    ) -> None:
        """

        Args:
            sounds:
            *args:
            **kwargs:
        """
        logger.info("Sound Thread")
        self.soundsQ = sounds
        self.port = "5570"
        self.topic: str = "data"
        self.SoundConfig = SoundConfigs
        self.blocksize = self.SoundConfig.blocksize
        self.sound_q_status = self.SoundConfig.ultraSoundStatus

    def callback(self, outdata: np.ndarray, frames: int, time, status) -> None:
        """

        Args:
            outdata:
            frames:
            time:
            status:

        Returns:

        """
        if not self.soundsQ:  # or if len(stack)==0
            self.sound_q_status["soundsstatus"] = "Sounds Queue is Empty!!!"
        else:
            if not ultraSDRSounds["mute"]:
                sounds = self.soundsQ.popleft()
                self.sound_q_status["soundstatus"] = (
                    "Sounds Queue Processed !!!"
                )
                outdata[:] = sounds
            else:
                self.sound_q_status["soundstatus"] = "Sound Muted"
                self.soundsQ.popleft()
                outdata[:] = 0
                outdata[:] = 0

    def run(self) -> None:
        """

        Returns:

        """
        self.soundit()

    def soundit(self) -> None:
        """

        Returns:

        """
        logger.info(threading.current_thread())
        logger.info("sound run")
        stream = sounddevice.OutputStream(
            channels=10,
            # blocksize=13981,  # 20972, #41943, # 83886, #167773,  # 20972, #8389, #83886, #2622, #44100, # 2622,  # 44100,
            blocksize=self.blocksize,
            samplerate=None,
            callback=self.callback,
        )
        stream.start()
        logger.info("stream started")
        # sounddevice.check_output_settings()
        while True:
            # logger.info("waiting")
            sounddevice.sleep(1)
            # ime.sleep(300)


def CallbackFlags():
    """

    Returns:

    """
    logger.info("flags")


def Nonecallback():
    """

    Returns:

    """
    logger.info("flags")


class GetDevices:
    """ """

    def __init__(self) -> None:
        """ """
        self.sdr_name = RadioConfigs.sdr_name

    def list_audio_devices(self):
        """

        Returns:

        """
        logger.info(sounddevice.default.device)
        return sounddevice.query_devices()

    def sdr_devices(self) -> str:
        """

        Returns:

        """
        results = SoapySDR.Device.enumerate()
        args = results[0]["driver"]
        logger.info(args)
        # sdr_name = SoapySDR.Device(dict(driver="rtlsdr"))
        return self.sdr_name


"""
class SDRcontrol(ReadSDRSamplesThread):
    def get_details(self):
        logger.info(f"name: {self.sdr_name}")
        return self.sdr_name
"""

if __name__ == "__main__":
    ultraSDRGraph = UltraDict(name="ultraSDRGraph")
    ultraSDRGraph["figure"] = {}
    ultraSDRGraph["frequency"] = "97.3"
    logger.info(ultraSDRGraph["frequency"])
    ultraQsizes = UltraDict(name="ultraQsizes")
    ultraQsizes["soundq"] = 0

    ultraSDRstatus = UltraDict(name="sdr_status")
    ultraSDRstatus["freq"] = "97.3"
    ultraSDRstatus["samp"] = "0"
    ultraSDRstatus["gain"] = "0"
    ultraSDRstatus["mtu"] = "0"
    ultraSDRstatus["bandwidth"] = "0"

    config = RadioConfigs()

    z = runSDR()
    z.runit()
