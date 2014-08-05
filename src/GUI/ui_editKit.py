# -*- coding: utf-8 -*-

# Copyright 2011 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\DrumBurp\src\GUI\editKit.ui'
#
# Created: Sun Apr 17 16:05:22 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_editKitDialog(object):
    def setupUi(self, editKitDialog):
        editKitDialog.setObjectName(_fromUtf8("editKitDialog"))
        editKitDialog.resize(645, 402)
        self.verticalLayout_2 = QtGui.QVBoxLayout(editKitDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.kitTable = QtGui.QTableWidget(editKitDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.kitTable.sizePolicy().hasHeightForWidth())
        self.kitTable.setSizePolicy(sizePolicy)
        self.kitTable.setDragEnabled(True)
        self.kitTable.setDragDropOverwriteMode(False)
        self.kitTable.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.kitTable.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.kitTable.setAlternatingRowColors(True)
        self.kitTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.kitTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.kitTable.setGridStyle(QtCore.Qt.DotLine)
        self.kitTable.setWordWrap(False)
        self.kitTable.setRowCount(8)
        self.kitTable.setColumnCount(5)
        self.kitTable.setObjectName(_fromUtf8("kitTable"))
        self.kitTable.setColumnCount(5)
        self.kitTable.setRowCount(8)
        item = QtGui.QTableWidgetItem()
        self.kitTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.kitTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.kitTable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.kitTable.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.kitTable.setHorizontalHeaderItem(4, item)
        self.kitTable.verticalHeader().setVisible(False)
        self.kitTable.verticalHeader().setMinimumSectionSize(10)
        self.horizontalLayout.addWidget(self.kitTable)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.upButton = QtGui.QPushButton(editKitDialog)
        self.upButton.setObjectName(_fromUtf8("upButton"))
        self.verticalLayout.addWidget(self.upButton)
        self.downButton = QtGui.QPushButton(editKitDialog)
        self.downButton.setObjectName(_fromUtf8("downButton"))
        self.verticalLayout.addWidget(self.downButton)
        self.addButton = QtGui.QPushButton(editKitDialog)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout.addWidget(self.addButton)
        self.deleteButton = QtGui.QPushButton(editKitDialog)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.verticalLayout.addWidget(self.deleteButton)
        self.clearButton = QtGui.QPushButton(editKitDialog)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.verticalLayout.addWidget(self.clearButton)
        self.resetButton = QtGui.QPushButton(editKitDialog)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.verticalLayout.addWidget(self.resetButton)
        self.loadButton = QtGui.QPushButton(editKitDialog)
        self.loadButton.setEnabled(False)
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.verticalLayout.addWidget(self.loadButton)
        self.saveButton = QtGui.QPushButton(editKitDialog)
        self.saveButton.setEnabled(False)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.verticalLayout.addWidget(self.saveButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(editKitDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(editKitDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), editKitDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), editKitDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(editKitDialog)
        editKitDialog.setTabOrder(self.kitTable, self.addButton)
        editKitDialog.setTabOrder(self.addButton, self.deleteButton)
        editKitDialog.setTabOrder(self.deleteButton, self.clearButton)
        editKitDialog.setTabOrder(self.clearButton, self.loadButton)
        editKitDialog.setTabOrder(self.loadButton, self.saveButton)
        editKitDialog.setTabOrder(self.saveButton, self.buttonBox)

    def retranslateUi(self, editKitDialog):
        editKitDialog.setWindowTitle(QtGui.QApplication.translate("editKitDialog", "Edit Drum Kit", None, QtGui.QApplication.UnicodeUTF8))
        self.kitTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("editKitDialog", "Drum name", None, QtGui.QApplication.UnicodeUTF8))
        self.kitTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("editKitDialog", "Abbreviation", None, QtGui.QApplication.UnicodeUTF8))
        self.kitTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("editKitDialog", "Default head", None, QtGui.QApplication.UnicodeUTF8))
        self.kitTable.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("editKitDialog", "Locked", None, QtGui.QApplication.UnicodeUTF8))
        self.kitTable.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("editKitDialog", "Old Drum", None, QtGui.QApplication.UnicodeUTF8))
        self.upButton.setText(QtGui.QApplication.translate("editKitDialog", "Move Up", None, QtGui.QApplication.UnicodeUTF8))
        self.downButton.setText(QtGui.QApplication.translate("editKitDialog", "Move Down", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("editKitDialog", "Add Drum", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("editKitDialog", "Delete Drum", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("editKitDialog", "Clear Kit", None, QtGui.QApplication.UnicodeUTF8))
        self.resetButton.setText(QtGui.QApplication.translate("editKitDialog", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.loadButton.setText(QtGui.QApplication.translate("editKitDialog", "Load Kit", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("editKitDialog", "Save Kit", None, QtGui.QApplication.UnicodeUTF8))

