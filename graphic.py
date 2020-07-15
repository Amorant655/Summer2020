from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys
import random

from database import DataBase


class GraphicVariable:
    def __init__(self):
        self.time_line = []
        self.values = []
        self.updator = None


class MainWindow():
    def __init__(self):
        self.traces = dict()
        self._db = DataBase()
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title="Plotting from influx")
        self.win.resize(1000, 600)
        self.win.setWindowTitle('influxPlot')
        self._last_measure = 0
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        self.canvas = self.win.addPlot()
        self.canvas.addLegend()
        timer = QtCore.QTimer()
        timer.timeout.connect(self._update_plot)
        timer.start(50)
        self.start()

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def trace(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name]["dx"].append(data_x)
            self.traces[name]["dy"].append(data_y)
            self.traces[name]["plot"].setData(self.traces[name]["dx"], self.traces[name]["dy"])
        else:
            self.traces[name] = {"plot": self.canvas.plot([data_x], [data_y], name=name,
                                                          pen=(random.randint(1, 255), random.randint(1, 255),
                                                               random.randint(1, 255))),
                                 "dx": [],
                                 "dy": []
                                 }

    def _update_plot(self):
        res = self._db.get_data(self._last_measure)
        time_l = self._last_measure
        for measure in res:
            time_l = int(measure.pop("time"))
            for variable in measure:
                if measure[variable] is None:
                    continue
                self.trace(variable, time_l, float(measure[variable]))
        self._last_measure = time_l


if __name__ == '__main__':
    MainWindow()