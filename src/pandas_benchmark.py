from run_benchmark import main as b_main
from appJar import gui


class PandasBenchmark:

    stats = {
        "no_all": 0,
        "no_all_last": 0,
        "time": 0,
        "perc_time": 0,
        "perc_time_last": 0,
        "cpu": 0,
        "perc_cpu": 0,
        "perc_cpu_last": 0,
        "mem": 0,
        "perc_mem": 0,
        "perc_mem_last": 0,
        "avg_pt": 0,
        "perc_avg_pt": 0,
        "perc_avg_pt_last": 0,
    }

    def __init__(self):
        self.app = gui("Pandas Benchmark", "800x300")
        self.app.setBg("gray")
        self.app.setFont(24)

        self.app.addLabel("title", "Welcome to PandasBenchmark")

        self._update_all_labels(create=True)
        self._update_label(
            "l0",
            "(Running benchmark may take a few minutes please wait...)",
            create=True)
        self.app.getLabelWidget("l0").config(font="Verdana 12 normal")
        self._update_l_error_label(0, True)
        self.app.addButtons(["Run", "Exit"], self._press)

        self.app.go()

    def _update_all_labels(self, create=False):
        self._update_label(
            "l1",
            "Your score: {} (better than {}% overall and {}% over last hour)".format(
                self.stats["avg_pt"],
                self.stats["perc_avg_pt"],
                self.stats["perc_avg_pt_last"]
            ),
            create)
        self._update_label(
            "l2",
            "Your time: {:.2f}s (better than {}% overall and {}% over last hour)".format(
                self.stats["time"]/1000,
                self.stats["perc_time"],
                self.stats["perc_time_last"]
            ),
            create)
        self._update_label(
            "l3",
            "Your cpu load: {}% (better than {}% overall and {}% over last hour)".format(
                self.stats["cpu"],
                self.stats["perc_cpu"],
                self.stats["perc_cpu_last"]
            ),
            create)
        self._update_label(
            "l4",
            "Your memory usage: {:.2f}MB (better than {}% overall and {}% over last hour)".format(
                self.stats["mem"]/1024/1024,
                self.stats["perc_mem"],
                self.stats["perc_mem_last"]
            ),
            create)

    def _update_l_error_label(self, er=0, cr=False):
        if er == 0:
            self._update_label(
                "l_error",
                "(If you do not see buttons below, please resize this window)",
                create=cr)
            self.app.getLabelWidget("l_error").config(font="Verdana 12 normal")
            self.app.setLabelFg("l_error", "black")
        else:
            self._update_label(
                "l_error",
                "(Can't send result to database (show only your results!))",
                create=cr)
            self.app.getLabelWidget("l_error").config(font="Verdana 14 bold")
            self.app.setLabelFg("l_error", "red")

    def _update_label(self, name, text, create=False):
        if create:
            self.app.addLabel(
                name,
                text
            )
            if name != 'l1':
                self.app.getLabelWidget(name).config(font="Verdana 14 normal")
            else:
                self.app.setLabelFg(name, "#731DD8")
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
            res_stat = b_main()
            self.stats = res_stat
            self._update_all_labels(create=False)

            self._update_l_error_label(self.stats["error"], False)
            self._do_compute(False)


def main():
    PandasBenchmark()


if __name__ == '__main__':
    main()
