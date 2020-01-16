import psutil
from threading import Thread
from time import sleep, time


class MeasureThread(Thread):
    cpu_avg = 0
    _cpu_sum = 0
    _cpu_cnt = 0
    mem_max = 0
    time_s = 0
    time_elapsed = 0

    def run(self):

        self.running = True
        self.time_s = time()
        currentProcess = psutil.Process()

        while self.running:
            sleep(0.5)
            self._cpu_sum = currentProcess.cpu_percent()
            self._cpu_cnt += 1
            self.cpu_avg = int(self._cpu_sum/self._cpu_cnt)
            self.mem_max = max(self.mem_max, currentProcess.memory_info()[0])

    def stop(self):
        self.running = False
        self.time_elapsed = int((time() - self.time_s)*1000)
