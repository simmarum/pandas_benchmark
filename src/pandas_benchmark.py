# import the library
from appJar import gui
import main as b_main
# handle button events


class PandasBenchmark:

    # no_all = 0
    # no_all_last = 0
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
        self._update_label(
            "lbtn",
            "(If you do not see buttons please resize this window)",
            create=True)
        self.app.getLabelWidget("lbtn").config(font="Verdana 12 overstrike")

        # start the GUI
        self.app.go()

    def _update_all_labels(self, create=False):
        self._update_label(
            "l1",
            "Your last score: {} (better than {}% overall and {}% over last hour)".format(
                self.avg_pt, self.perc_avg_pt, self.perc_avg_pt_last),
            create)
        self._update_label(
            "l2",
            "Your last time: {:.2f}s (better than {}% overall and {}% over last hour)".format(
                self.time/1000, self.perc_time, self.perc_time_last),
            create)
        self._update_label(
            "l3",
            "Your last cpu load: {}% (better than {}% overall and {}% over last hour)".format(
                self.cpu, self.perc_cpu, self.perc_cpu_last),
            create)
        self._update_label(
            "l4",
            "Your last memory usage: {:.2f}MB (better than {}% overall and {}% over last hour)".format(
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
            res_stat = b_main.main()
            # self.no_all = res_stat[0]
            # self.no_all_last = res_stat[1]
            self.time = res_stat[2]
            self.perc_time = res_stat[3]
            self.perc_time_last = res_stat[4]
            self.cpu = res_stat[5]
            self.perc_cpu = res_stat[6]
            self.perc_cpu_last = res_stat[7]
            self.mem = res_stat[8]
            self.perc_mem = res_stat[9]
            self.perc_mem_last = res_stat[10]
            self.avg_pt = res_stat[11]
            self.perc_avg_pt = res_stat[12]
            self.perc_avg_pt_last = res_stat[13]
            self._update_all_labels(create=False)
            self._do_compute(False)


def main():
    PandasBenchmark()


if __name__ == '__main__':
    main()
