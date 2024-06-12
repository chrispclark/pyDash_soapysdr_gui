from loguru import logger
from SoapySDR import SOAPY_SDR_CF32, SOAPY_SDR_RX  # SOAPY_SDR_CS16,
from UltraDict import UltraDict
from SDRConfigs import RadioConfigs
from SDRConfigs import QueueConfigs

commands = UltraDict(name="commands_for_sdr", recursive=True)

SDRDefinitions = UltraDict(name="SDRDefinitions", recursive=True)
ultraSDRstatus = UltraDict(name="sdr_status")


class SDRcommands:
    def __init__(self, rx_stream):
        SDRconfig = RadioConfigs()
        SDRqueue = QueueConfigs
        self.sdr_name = SDRconfig.sdr_name
        self.ultraSDRStatus = QueueConfigs.ultraSDRstatus
        # self.sdrlogic = SDRlogic()
        self.config = RadioConfigs()
        self.rx_stream = rx_stream
        self.oldz = ""

    def SDRset_get(self, commands):
        # logger.info(commands)
        z = commands["command_to_sdr"]
        if z != self.oldz:
            logger.info(f"sdr command received {z}")
            key, val = list(z.items())[0]
            logger.info(f"key {key} val {val}")
            func_call = getattr(self.SDRlogic, key)
            func_call(self, val)
            self.oldz = z
        else:
            pass
            # logger.info('not changed')

    def return_get(self):
        freq = self.SDRlogic.get_frequency(self, 0)
        samp = self.SDRlogic.get_samplerate(self, 0)
        gain = self.SDRlogic.get_gain(self, 0)
        mtu = self.SDRlogic.get_MTU(self, 0)
        bandwidth = self.SDRlogic.get_bandwidth(self, 0)
        # logger.info(bandwidth)
        self.ultraSDRStatus["freq"] = freq
        self.ultraSDRStatus["bandwidth"] = bandwidth
        self.ultraSDRStatus["samp"] = samp
        self.ultraSDRStatus["gain"] = gain
        self.ultraSDRStatus["mtu"] = mtu

        """
        data_list = [{'Field': 'freq', 'Value': freq},
                     {'Field': 'sample rate', 'Value': samp}]
        """
        # logger.info(self.ultraSDRStatus)
        return self.ultraSDRStatus

    class SDRlogic:
        def __init__(self, rx_stream):
            SDRconfig = RadioConfigs()
            self.sdr_name = SDRconfig.sdr_name
            self.config = SDRconfig()
            self.rx_stream = rx_stream
            logger.info(self.rx_stream)
            logger.info(type(self.rx_stream))
            pass

        def control_logic(self, o):
            logger.info(o)
            z = self.sdr_name.getFrequency(self.config.rx_chan, 0)
            logger.info(f"Freq: {z}")
            z = self.sdr_name.setFrequency(self.config.rx_chan, 0)
            logger.info(f"Freq: {z}")
            z = self.sdr_name.getBandwidth(self.config.rx_chan, 0)
            logger.info(f"bandwidth: {z}")
            z = self.sdr_name.getGain(self.config.rx_chan, 0)
            logger.info(f"Gain: {z}")
            z = self.sdr_name.getHardwareInfo()
            logger.info(f"Hardware Info: {z}")
            z = self.sdr_name.getHardwareTime()
            logger.info(f"Hardware Time: {z}")
            z = self.sdr_name.getSampleRate(self.config.rx_chan, 0)
            logger.info(f"sample Rate {z}")
            z = self.sdr_name.setSampleRate(self.config.rx_chan, 0)
            logger.info(f"sample Rate {z}")
            z = self.sdr_name.getStreamMTU(self.rx_stream)
            logger.info(f"Stream MTU: {z}")
            z = self.sdr_name.getTimeSource()
            logger.info(f"Time Source: {z}")
            return

        def get_frequency(self, val):
            z = self.sdr_name.getFrequency(self.config.rx_chan, 0)
            # logger.info(z)
            return z

        def set_frequency(self, val):
            logger.info(val)
            z = self.sdr_name.setFrequency(
                SOAPY_SDR_RX, self.config.rx_chan, "RF", val
            )
            logger.info(z)
            return z

        def get_samplerate(self, val):
            z = self.sdr_name.getSampleRate(self.config.rx_chan, 0)
            # logger.info(f"Get Sample Rate: {z}")
            return z

        def set_samplerate(self, val):
            z = self.sdr_name.getSampleRate(self.config.rx_chan, 0)
            logger.info(z)
            return z

        def get_gain(self, val):
            z = self.sdr_name.getGain(self.config.rx_chan, 0)
            # logger.info(z)
            return z

        def get_bandwidth(self, val):
            z = self.sdr_name.getBandwidth(self.config.rx_chan, 0)
            # logger.info(z)
            return z

        def get_MTU(self, val):
            # z = self.sdr_name.getStreamMTU(self.rx_stream)
            z = "Not implemented"
            # logger.info(z)
            return z


if __name__ == "__main__":
    pass
