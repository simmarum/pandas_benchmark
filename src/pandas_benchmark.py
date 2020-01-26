import sys
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

    def _get_l_l1(self):
        return "Your score: {} (better than {}% overall and {}% over last day)".format(
            self.stats["avg_pt"],
            self.stats["perc_avg_pt"],
            self.stats["perc_avg_pt_last"]
        )

    def _get_l_l2(self):
        return "Your time: {:.2f}s (better than {}% overall and {}% over last day)".format(
            self.stats["time"]/1000,
            self.stats["perc_time"],
            self.stats["perc_time_last"]
        )

    def _get_l_l3(self):
        return "Your cpu load: {}% (better than {}% overall and {}% over last day)".format(
            self.stats["cpu"],
            self.stats["perc_cpu"],
            self.stats["perc_cpu_last"]
        )

    def _get_l_l4(self):
        return "Your memory usage: {:.2f}MB (better than {}% overall and {}% over last day)".format(
            self.stats["mem"]/1024/1024,
            self.stats["perc_mem"],
            self.stats["perc_mem_last"]
        )

    def __init__(self, run_gui):
        if run_gui == True:
            self.app = gui("Pandas Benchmark", "1500x300")
            self.app.setBg("#9590A8")
            self.app.setFont(24)

            self.app.addLabel("title", "Welcome to PandasBenchmark", 0, 0)

            self._update_all_labels(create=True)

            self.fig = self.app.addPlotFig("p1", 0, 3, 1, 15)

            self._update_label(
                5,
                "l0",
                "(Running benchmark may take a few minutes please wait...)",
                create=True)
            self.app.getLabelWidget("l0").config(font="Verdana 12 normal")
            self._update_l_error_label(0, True)
            self.app.addButtons(["Run", "Exit"], self._press)

            self.app.go()
        else:
            print("Run benchmark")
            res_stat = b_main()
            self.stats = res_stat
            print("Finish benchmark")
            print("\n")
            print(self._get_l_l1())
            print(self._get_l_l2())
            print(self._get_l_l3())
            print(self._get_l_l4())

    def _update_all_labels(self, create=False):
        self._update_label(
            1,
            "l1",
            self._get_l_l1(),
            create)
        self._update_label(
            2,
            "l2",
            self._get_l_l2(),
            create)
        self._update_label(
            3,
            "l3",
            self._get_l_l3(),
            create)
        self._update_label(
            4,
            "l4",
            self._get_l_l4(),
            create)

    def _update_l_error_label(self, er=0, cr=False):
        if er == 0:
            self._update_label(
                6,
                "l_error",
                "(If you do not see buttons below, please resize this window)",
                create=cr)
            self.app.getLabelWidget("l_error").config(font="Verdana 12 normal")
            self.app.setLabelFg("l_error", "black")
        else:
            self._update_label(
                6,
                "l_error",
                "(Can't send result to database (show only your results!))",
                create=cr)
            self.app.getLabelWidget("l_error").config(font="Verdana 14 bold")
            self.app.setLabelFg("l_error", "red")

    def _update_label(self, r, name, text, create=False):
        if create:
            self.app.addLabel(
                name,
                text,
                r,
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

            self.fig.clear()
            self.ax = self.fig.add_subplot(111)
            if self.stats["all_data"] is not None:
                self.barlist = self.ax.bar(
                    self.stats["all_data_x"],
                    self.stats["all_data_y"],
                    color='b'
                )
                tmp_idx_avg_pt = self.stats["all_data_y"].index(self.stats['avg_pt'])
                for idx in range(len(self.stats["all_data_y"])):
                    if idx == tmp_idx_avg_pt:
                        self.barlist[idx].set_color('r')
                    else:
                        self.barlist[idx].set_color('b')
                self.app.refreshPlot("p1")

            self._do_compute(False)


def main():
    run_gui = True
    if (len(sys.argv) > 1) and (sys.argv[1] == 'nogui'):
        run_gui = False
    PandasBenchmark(run_gui)


if __name__ == '__main__':
    main()
