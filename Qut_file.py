#!/usr/bin/env python
#=[site officiel]================
#<<<<<Qut_file by W3YZOH0RTH>>>>>
#=====[http://progject.free.fr/]=
import PyQt4.Qt as qt
import sys
from mod.gui import Gui

app = qt.QApplication(sys.argv)
x = Gui()
x.show()
sys.exit(app.exec_())
