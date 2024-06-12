from soap_mp import runSDR
from loguru import logger
from multiprocessing import Process
from SDRConfigs import QueueConfigs
from UltraDict import UltraDict


class RunSDRlocal:
    def __init__(self):
        queue_config = QueueConfigs()
        logger.info("init")
        self.command_queue_to_sdr = queue_config.command_queue_to_sdr
        logger.info(self.command_queue_to_sdr)
        self.command_queue_from_sdr = queue_config.command_queue_from_sdr
        self.graph_fig_queue = queue_config.graph_fig_queue
        self.z = 0

    def go(self):
        logger.info("go")
        sdr_run = runSDR()
        sdr_run.runit()

    def run(self):
        process_start = Process(name="SDR", target=self.go)
        process_start.daemon = True
        process_start.start()

        logger.info(
            f"Starting: {process_start.name} {process_start.pid} {process_start}"
        )
        process_start.join()


if __name__ == "__main__":
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

    a = RunSDRlocal()
    a.run()
