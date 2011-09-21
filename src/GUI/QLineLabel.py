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
'''
Created on 19 Jan 2011

@author: Mike Thomas
'''

from QEditKitDialog import QEditKitDialog
from PyQt4 import QtGui, QtCore

class QLineLabel(QtGui.QGraphicsItem):
    def __init__(self, drum, qScore, parent):
        super(QLineLabel, self).__init__(parent = None,
                                          scene = qScore)
        self._text = ""
        self._props = qScore.displayProperties
        self._rect = QtCore.QRectF(0, 0,
                                   self.cellWidth(),
                                   self.cellHeight())
        self._highlighted = False
        self.setText(drum.abbr)
        self.setToolTip(drum.name)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def cellHeight(self):
        return self.scene().ySpacing

    def cellWidth(self):
        return 2 * self.scene().xSpacing

    def mouseDoubleClickEvent(self, event_):
        editDialog = QEditKitDialog(self.scene().score.drumKit,
                                    self.scene().parent())
        if editDialog.exec_():
            newKit, changes = editDialog.getNewKit()
            self.scene().changeKit(newKit, changes)


    def setText(self, text):
        self._text = text
        self.update()

    def setDimensions(self):
        self.prepareGeometryChange()
        self._rect.setBottomRight(QtCore.QPointF(self.cellWidth(),
                                                 self.cellHeight()))

    def xSpacingChanged(self):
        self.setDimensions()

    def ySpacingChanged(self):
        self.setDimensions()

    def boundingRect(self):
        return self._rect

    def paint(self, painter, dummyOption, dummyWidget = None):
        painter.save()
        painter.setPen(QtCore.Qt.NoPen)
        if len(self._text) > 0:
            painter.setPen(QtCore.Qt.SolidLine)
            font = self._props.noteFont
            if font is None:
                font = painter.font()
            else:
                painter.setFont(font)
            br = QtGui.QFontMetrics(painter.font())
            br = br.tightBoundingRect(self._text)
            w = br.width()
            h = br.height()
            textLocation = QtCore.QPointF((self.cellWidth() - w + 2) / 2,
                                          (self.cellHeight() + h) / 2)
            painter.drawText(textLocation, self._text)
        if self._highlighted:
            painter.setPen(QtCore.Qt.SolidLine)
            painter.setPen(self.scene().palette().highlight().color())
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawRect(0, 0, self.cellWidth() - 1, self.cellHeight())
        painter.restore()

    def setHighlight(self, onOff):
        if onOff != self._highlighted:
            self._highlighted = onOff
            self.update()

