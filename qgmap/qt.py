
try:
	from PySide6 import (
		QtCore, QtGui, QtWidgets, QtWebEngineCore, QtWebEngineWidgets, QtWebChannel, QtNetwork
	)

except ImportError:
	from PyQt6 import (
		QtCore, QtGui, QtWidgets, QtWebEngineCore, QtWebEngineWidgets, QtWebChannel, QtNetwork
	)
	# Alias used in PySide
	QtCore.Signal = QtCore.pyqtSignal
	QtCore.Slot = QtCore.pyqtSlot
	QtCore.Property = QtCore.pyqtProperty


