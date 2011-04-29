from app.views.qt4.graph.show_ui import Ui_GraphShow

import math
import pickle
from PyQt4 import QtCore, QtGui

from app.models.graph import Graph
from app.controllers.graphs_controller import GraphsController
from app.helpers.graph_helper import *

class GraphShow(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.controller = GraphsController()

        self.graph = Graph()
        
        self.ui = Ui_GraphShow()
        self.ui.setupUi(self)
    
    def set_action(self, action):
        self.ui.graphicsView.set_action(action)