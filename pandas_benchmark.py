# import the library
from appJar import gui
import time
# handle button events


class PandasBenchmark:

    no_all = 0
    no_all_last = 0
    time = 0
    perc_time = 0
    perc_time_last = 0
    cpu = 0
    perc_cpu = 0
    perc_cpu_last = 0
    mem = 0
    perc_mem = 0
    perc_mem_last = 0
    avg_pt = 0
    perc_avg_pt = 0
    perc_avg_pt_last = 0

    def __init__(self):
        # create a GUI variable called app
        self.app = gui("Pandas Benchmark", "800x300")
        self.app.setBg("gray")
        self.app.setFont(24)

        # add & configure widgets - widgets get a name, to help referencing them later
        self.app.addLabel("title", "Welcome to PandasBenchmark")

        # add labels
        self._update_all_labels(create=True)
        self._update_label(
            "l0",
            "(Running benchmark may take a few minutes please wait...)",
            create=True)
        self.app.getLabelWidget("l0").config(font="Verdana 12 overstrike")
        # link the buttons to the function called _press
        self.app.addButtons(["Run", "Exit"], self._press)

        # start the GUI
        self.app.go()

    def _update_all_labels(self, create=False):
        self._update_label(
            "l1",
            "Your last score: {} (better than {}% overall and {}% last hour)".format(
                self.avg_pt, self.perc_avg_pt, self.perc_avg_pt_last),
            create)
        self._update_label(
            "l2",
            "Your last time: {:.2f}s (better than {}% overall and {}% last hour)".format(
                self.time/1000, self.perc_time, self.perc_time_last),
            create)
        self._update_label(
            "l3",
            "Your last cpu load: {}% (better than {}% overall and {}% last hour)".format(
                self.cpu, self.perc_cpu, self.perc_cpu_last),
            create)
        self._update_label(
            "l4",
            "Your last memory usage: {:.2f}MB (better than {}% overall and {}% last hour)".format(
                self.mem/1024/1024, self.perc_mem, self.perc_mem_last),
            create)

    def _update_label(self, name, text, create=False):
        if create:
            self.app.addLabel(
                name,
                text
            )
            if name != 'l1':
                self.app.getLabelWidget(name).config(font="Verdana 16 overstrike")
        else:
            self.app.setLabel(
                name,
                text
            )

    def _do_compute(self, running=True):
        if running:
            self.app.disableButton("Run")
        else:
            self.app.enableButton("Run")

    def _press(self, button):
        if button == "Exit":
            self.app.stop()
        else:
            self._do_compute(True)
            print("Run benchmark")
            self.no_all = 10
            self.no_all_last = 3
            self.time = 10000
            self.perc_time = 90
            self.perc_time_last = 80
            self.cpu = 23
            self.perc_cpu = 65
            self.perc_cpu_last = 46
            self.mem = 557441024
            self.perc_mem = 45
            self.perc_mem_last = 35
            self.avg_pt = 12353
            self.perc_avg_pt = 12
            self.perc_avg_pt_last = 43
            a = 0
            for i in range(1_000_000):
                for j in range(1_0):
                    a += 1
            self._update_all_labels(create=False)
            self._do_compute(False)


PandasBenchmark()
