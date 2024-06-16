from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from loguru import logger
from queue import Queue
from UltraDict import UltraDict  # type: ignore
import SoapySDR
from SoapySDR import SOAPY_SDR_CF32, SOAPY_SDR_RX  # SOAPY_SDR_CS16,


@dataclass()
class QueueConfigs:
    """_summary_"""

    soundsQ = deque()
    command_queue_to_sdr: Queue = Queue()
    command_queue_from_sdr: Queue = Queue()
    graph_fig_queue: Queue = Queue()
    samplesQ: Queue = Queue()
    ultra = UltraDict(name="commands_for_sdr", recursive=True)
    ultraSDRstatus = UltraDict(name="sdr_status")
    ultraSDRDefinitions = UltraDict(name="SDRDefinitions", recursive=True)

    def __post_init__(self) -> None:
        logger.info("q data")



class SharedMemoryDict:
    def __init__(self):
        logger.info("init")

    def __post_init__(self) -> None:
        logger.info("shared data")


    @staticmethod
    def CreateSharedMemoryDict():
        ultra = UltraDict(name="sdr", recursive=True)
        ultra["commands"] = {"counter": 0, "fred": 1}
        ultra["sound"] = {"status": 0, "mute": 0, "soundq": 0}
        ultra["graph"] = {"figure": {}, "frequency": 97.3}
        ultra["SDRDefinitions"] = {"a": 1, "b": 2}
        ultra["status"] = {
            "freq": "97.3",
            "samp": 0,
            "gain": 0,
            "mtu": 0,
            "SDRRunning": False,
            "live_dev": "unknown system",
        }
        logger.info("created")
        logger.info(ultra.name)
        return ultra


@dataclass
class RadioConfigs:
    sdr_name = SoapySDR.Device(dict(driver="rtlsdr"))
    blocksize: int = 48100  # 42100   # 44100
    freq: float = 97.3e6  # Radio station to tune too
    # freq: float = 102.2e6  # Radio station to tune too
    Fs: float = (
        2.2e6  # 2.4e6  # 2.5e6 # smaller sample rate, speach is faster.
    )
    F_offset: int = 2500
    Fc: float = freq - F_offset
    sdr_sample_rate: float = Fs
    sdr_center_freq: float = Fc
    samples_per_scan = int(4194304 / 6)
    sdr_gain: str = "auto"
    rx_chan: int = 0
    Fs_audio: int = 0
    enable_cuda: bool = True  # False  # If True, enable CUDA demodulation.
    input_rate: float = 10e6  # The SDR RX bandwidth.
    device_name: str = "rtlsdr"  # The SoapySDR device string.
    F_offset: int = 250000
    use_agc: bool = True  # Use or don't use the AGC
    timeout_us: int = int(5e6)

    @staticmethod
    def __post_init__() -> None:
        logger.info("radio data")


@dataclass
class SoundConfigs:
    blocksize = 13981
    ultraSoundStatus = UltraDict(name="sdr_sound_status")
    # ultraSoundStatus = 'test'
    sound_q_status: str = ""


if __name__ == "__main__":
    config = QueueConfigs()
    q1 = config.command_queue_to_sdr
    q1.put(7)
    logger.info(q1)
    q2 = config.command_queue_to_sdr
    logger.info(q2)
    logger.info(q2.get())
    # z = runSDR()
    # z.runit()
