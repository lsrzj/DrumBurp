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
Created on 8 Jan 2011

@author: Mike Thomas
'''

from Data.Counter import CounterRegistry
from Data.ASCIISettings import ASCIISettings
import Data.MeasureCount
from PyQt4.QtCore import QObject, pyqtSignal

#pylint: disable-msg=R0902

class QDisplayProperties(QObject):
    _START_NOTE_WIDTH = 12
    MIN_NOTE_WIDTH = 12
    MAX_NOTE_WIDTH = 20
    NOTE_WIDTH_RANGE = MAX_NOTE_WIDTH - MIN_NOTE_WIDTH

    _START_NOTE_HEIGHT = 12
    MIN_NOTE_HEIGHT = 11
    MAX_NOTE_HEIGHT = 20
    NOTE_HEIGHT_RANGE = MAX_NOTE_HEIGHT - MIN_NOTE_HEIGHT

    _START_LINE_SPACE = 20
    MIN_LINE_SPACE = 10
    MAX_LINE_SPACE = 80
    LINE_SPACE_RANGE = MAX_LINE_SPACE - MIN_LINE_SPACE

#    LINELABELWIDTH = 30

    def __init__(self):
        super(QDisplayProperties, self).__init__()
        self._xMargins = 20
        self._yMargins = 30
        self._xSpacing = self._START_NOTE_WIDTH
        self._ySpacing = self._START_NOTE_HEIGHT
        self._lineSpacing = self._START_LINE_SPACE
        self._noteFont = None
        self._sectionFont = None
        self._sectionFontSize = 20
        self._metadataVisible = True
        self._metadataFont = None
        self._metadataFontSize = 20
        self._kitDataVisible = False
        self._beatCountVisible = True
        self._emptyLinesVisible = True
        self._head = None
        self._width = 80
        self._counterRegistry = CounterRegistry()
        self.defaultCounter = Data.MeasureCount.makeSimpleCount(self._counterRegistry[0], 4)

    xSpacingChanged = pyqtSignal()
    ySpacingChanged = pyqtSignal()
    lineSpacingChanged = pyqtSignal()
    fontChanged = pyqtSignal()
    sectionFontChanged = pyqtSignal()
    sectionFontSizeChanged = pyqtSignal()
    metadataVisibilityChanged = pyqtSignal()
    metadataFontChanged = pyqtSignal()
    metadataFontSizeChanged = pyqtSignal()
    kitDataVisibleChanged = pyqtSignal()
    beatCountVisibleChanged = pyqtSignal()
    emptyLinesVisibleChanged = pyqtSignal()

    def connectScore(self, score):
        self.xSpacingChanged.connect(score.xSpacingChanged)
        self.ySpacingChanged.connect(score.ySpacingChanged)
        self.lineSpacingChanged.connect(score.lineSpacingChanged)
        self.fontChanged.connect(score.update)
        self.sectionFontChanged.connect(score.sectionFontChanged)
        self.sectionFontSizeChanged.connect(score.sectionFontChanged)
        self.metadataFontChanged.connect(score.metadataFontChanged)
        self.metadataFontSizeChanged.connect(score.metadataFontChanged)
        self.metadataVisibilityChanged.connect(score.metadataVisibilityChanged)
        self.kitDataVisibleChanged.connect(score.kitDataVisibleChanged)
        self.beatCountVisibleChanged.connect(score.reBuild)
        self.emptyLinesVisibleChanged.connect(score.reBuild)

    def _getxSpacing(self):
        return self._xSpacing
    def _setxSpacing(self, value):
        if value < 0:
            value += 101
            value = int(0.5 + self.MIN_NOTE_WIDTH +
                        ((value / 100.0) * self.NOTE_WIDTH_RANGE))
        if self._xSpacing != value:
            self._xSpacing = value
            self.xSpacingChanged.emit()
    xSpacing = property(fget = _getxSpacing, fset = _setxSpacing)

    def _getySpacing(self):
        return self._ySpacing
    def _setySpacing(self, value):
        if value < 0:
            value += 101
            value = int(0.5 + self.MIN_NOTE_HEIGHT +
                        ((value / 100.0) * self.NOTE_HEIGHT_RANGE))
        if self._ySpacing != value:
            self._ySpacing = value
            self.ySpacingChanged.emit()
    ySpacing = property(fget = _getySpacing, fset = _setySpacing)

    def _getlineSpacing(self):
        return self._lineSpacing
    def _setlineSpacing(self, value):
        if value < 0:
            value += 101
            value = int(0.5 + self.MIN_LINE_SPACE +
                        ((value / 100.0) * self.LINE_SPACE_RANGE))
        if self._lineSpacing != value:
            self._lineSpacing = value
            self.lineSpacingChanged.emit()
    lineSpacing = property(fget = _getlineSpacing, fset = _setlineSpacing)

    def _getxMargins(self):
        return self._xMargins
    def _setxMargins(self, value):
        if self._xMargins != value:
            self._xMargins = value
    xMargins = property(fget = _getxMargins, fset = _setxMargins)

    def _getyMargins(self):
        return self._yMargins
    def _setyMargins(self, value):
        if self._yMargins != value:
            self._yMargins = value
    yMargins = property(fget = _getyMargins, fset = _setyMargins)

    def _getnoteFont(self):
        return self._noteFont
    def _setnoteFont(self, value):
        if self._noteFont != value:
            self._noteFont = value
            self.fontChanged.emit()
    noteFont = property(fget = _getnoteFont, fset = _setnoteFont)

    def _getsectionFontSize(self):
        return self._sectionFontSize
    def _setsectionFontSize(self, value):
        if self._sectionFontSize != value:
            self._sectionFontSize = value
            self.sectionFont.setPointSize(value)
            self.sectionFontSizeChanged.emit()
    sectionFontSize = property(fget = _getsectionFontSize,
                               fset = _setsectionFontSize)

    def _getsectionFont(self):
        return self._sectionFont
    def _setsectionFont(self, value):
        if self._sectionFont != value:
            value.setBold(True)
            value.setItalic(True)
            value.setPointSize(self._sectionFontSize)
            self._sectionFont = value
            self.sectionFontChanged.emit()
    sectionFont = property(fget = _getsectionFont, fset = _setsectionFont)

    def _getmetadataFontSize(self):
        return self._metadataFontSize
    def _setmetadataFontSize(self, value):
        if self._metadataFontSize != value:
            self._metadataFontSize = value
            self.metadataFont.setPointSize(value)
            self.metadataFontSizeChanged.emit()
    metadataFontSize = property(fget = _getmetadataFontSize,
                                fset = _setmetadataFontSize)

    def _getmetadataFont(self):
        return self._metadataFont
    def _setmetadataFont(self, value):
        if self._metadataFont != value:
            value.setBold(True)
            value.setPointSize(self._metadataFontSize)
            self._metadataFont = value
            self.metadataFontChanged.emit()
    metadataFont = property(fget = _getmetadataFont, fset = _setmetadataFont)

    def _gethead(self):
        return self._head
    def _sethead(self, value):
        if self._head != value:
            self._head = value
    head = property(fget = _gethead, fset = _sethead)

    def _getmetadataVisible(self):
        return self._metadataVisible
    def _setmetadataVisible(self, value):
        if self._metadataVisible != value:
            self._metadataVisible = value
            self.metadataVisibilityChanged.emit()
    metadataVisible = property(fget = _getmetadataVisible,
                               fset = _setmetadataVisible)

    def _getkitDataVisible(self):
        return self._kitDataVisible
    def _setkitDataVisible(self, value):
        if self._kitDataVisible != value:
            self._kitDataVisible = value
            self.kitDataVisibleChanged.emit()
    kitDataVisible = property(fget = _getkitDataVisible,
                              fset = _setkitDataVisible)

    def _getbeatCountVisible(self):
        return self._beatCountVisible
    def _setbeatCountVisible(self, value):
        if self._beatCountVisible != value:
            self._beatCountVisible = value
            self.beatCountVisibleChanged.emit()
    beatCountVisible = property(fget = _getbeatCountVisible,
                                fset = _setbeatCountVisible)

    def _getemptyLinesVisible(self):
        return self._emptyLinesVisible
    def _setemptyLinesVisible(self, value):
        if self._emptyLinesVisible != value:
            self._emptyLinesVisible = value
            self.emptyLinesVisibleChanged.emit()
    emptyLinesVisible = property(fget = _getemptyLinesVisible,
                                 fset = _setemptyLinesVisible)

    def maxColumns(self, widthInPixels):
        widthInPixels -= 2 * (self.xMargins + self.xSpacing)
        return int(widthInPixels / self.xSpacing)

    @staticmethod
    def allowedNoteHeads():
        return ("x", "X", "o", "O", "g", "f", "d", "+", "#", "b")

    def save(self, settings):
        pass

    @property
    def counterRegistry(self):
        return self._counterRegistry

    def generateAsciiSettings(self, settings = None):
        if settings is None:
            settings = ASCIISettings()
        settings.metadata = self.metadataVisible
        settings.kitKey = self.kitDataVisible
        settings.printCount = self.beatCountVisible
        settings.omitEmpty = not self.emptyLinesVisible
        return settings
