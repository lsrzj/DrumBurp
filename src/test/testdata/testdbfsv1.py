# Copyright 2015 Michael Thomas
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
Created on Jun 21, 2015

@author: Mike Thomas
'''

import unittest
from cStringIO import StringIO
from Data import Beat, Counter, fileUtils, DBErrors, DrumKit, FontOptions, DefaultKits
from Data.Drum import Drum, HeadData
from Data.Counter import CounterRegistry
from Data.Measure import Measure
from Data import MeasureCount, ScoreMetaData
from Data.NotePosition import NotePosition

from Data.fileStructures import dbfsv1

class TestBeat(unittest.TestCase):
    def testWriteFullBeat(self):
        beat = Beat.Beat(Counter.Counter("e+a"))
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv1.BeatStructureV1().write(beat, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["BEAT_START",
                          "  NUM_TICKS 4",
                          "  COUNT |^e+a|",
                          "BEAT_END"])


    def testWritePartialBeat(self):
        beat = Beat.Beat(Counter.Counter("e+a"), 2)
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv1.BeatStructureV1().write(beat, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["BEAT_START",
                          "  NUM_TICKS 2",
                          "  COUNT |^e+a|",
                          "BEAT_END"])

    def testReadFull(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS 4
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        beat = dbfsv1.BeatStructureV1().read(iterator)
        self.assertEqual("".join(beat.count(1)), "1e+a")

    def testReadPartial(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS 2
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        beat = dbfsv1.BeatStructureV1().read(iterator)
        self.assertEqual("".join(beat.count(1)), "1e")

    def testReadBadCount(self):
        handle = StringIO("""BEAT_START
        COUNT |^e+d|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.BadCount, dbfsv1.BeatStructureV1().read,
                          iterator)

    def testReadBadTicks(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS x
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidInteger, dbfsv1.BeatStructureV1().read,
                          iterator)

    def testReadBadNegativeTicks(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS -1
        COUNT |^e+a|
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.InvalidPositiveInteger,
                          dbfsv1.BeatStructureV1().read,
                          iterator)

    def testReadBadLine(self):
        handle = StringIO("""BEAT_START
        NUM_TICKS 4
        COUNT |^e+a|
        BAD_LINE xxx
        BEAT_END""")
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.UnrecognisedLine,
                          dbfsv1.BeatStructureV1().read, iterator)

class TestMeasureCount(unittest.TestCase):
    def testSimpleWrite(self):
        myCounter = Counter.Counter("e+a")
        count = MeasureCount.makeSimpleCount(myCounter, 4)
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv1.MeasureCountStructureV1().write(count, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["START_MEASURE_COUNT",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "END_MEASURE_COUNT"])

    def testComplexWrite(self):
        counter1 = Counter.Counter("e+a")
        counter2 = Counter.Counter("+a")
        counter3 = Counter.Counter("+")
        counter4 = Counter.Counter("e+a")
        count = MeasureCount.MeasureCount()
        count.addBeats(Beat.Beat(counter1), 1)
        count.addBeats(Beat.Beat(counter2), 1)
        count.addBeats(Beat.Beat(counter3), 1)
        count.addBeats(Beat.Beat(counter4, 2), 1)
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv1.MeasureCountStructureV1().write(count, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["START_MEASURE_COUNT",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 3",
                          "    COUNT |^+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 2",
                          "    COUNT |^+|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 2",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "END_MEASURE_COUNT"])

    def testSimpleDefaultWrite(self):
        myCounter = Counter.Counter("e+a")
        count = MeasureCount.makeSimpleCount(myCounter, 4)
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv1.DefaultMeasureCountStructureV1().write(count, indenter)
        output = handle.getvalue().splitlines()
        self.assertEqual(output,
                         ["START_DEFAULT_MEASURE_COUNT",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "  BEAT_START",
                          "    NUM_TICKS 4",
                          "    COUNT |^e+a|",
                          "  BEAT_END",
                          "END_DEFAULT_MEASURE_COUNT"])

    def testReadSimple(self):
        data = """START_MEASURE_COUNT
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                  END_MEASURE_COUNT"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        count = dbfsv1.MeasureCountStructureV1().read(iterator)
        self.assert_(count.isSimpleCount())
        self.assertEqual(len(count), 16)
        self.assertEqual(count.countString(), "1e+a2e+a3e+a4e+a")

    def testReadSimpleDefault(self):
        data = """START_DEFAULT_MEASURE_COUNT
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                      BEAT_START
                          NUM_TICKS 4
                          COUNT |^e+a|
                      BEAT_END
                  END_DEFAULT_MEASURE_COUNT"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        count = dbfsv1.DefaultMeasureCountStructureV1().read(iterator)
        self.assert_(count.isSimpleCount())
        self.assertEqual(len(count), 16)
        self.assertEqual(count.countString(), "1e+a2e+a3e+a4e+a")


    def testReadComplex(self):
        data = """START_MEASURE_COUNT
                  BEAT_START
                    COUNT |^e+a|
                  BEAT_END
                  BEAT_START
                    COUNT |^+a|
                  BEAT_END
                  BEAT_START
                    COUNT |^+|
                  BEAT_END
                  BEAT_START
                    NUM_TICKS 2
                    COUNT |^e+a|
                  BEAT_END
                END_MEASURE_COUNT"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        count = dbfsv1.MeasureCountStructureV1().read(iterator)
        self.assertFalse(count.isSimpleCount())
        self.assertEqual(len(count), 11)
        self.assertEqual(count.countString(), "1e+a2+a3+4e")

    def testBadLine(self):
        data = """START_MEASURE_COUNT
              UNRECOGNISED LINE
              BEAT_START
                  COUNT |^e+a|
              BEAT_END
          END_MEASURE_COUNT"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.UnrecognisedLine,
                          dbfsv1.MeasureCountStructureV1().read,
                          iterator)

    def testRepeatBeats(self):
        data = """START_MEASURE_COUNT
              REPEAT_BEATS 3
              BEAT_START
                  COUNT |^e+a|
              BEAT_END
          END_MEASURE_COUNT"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        self.assertRaises(DBErrors.UnrecognisedLine,
                          dbfsv1.MeasureCountStructureV1().read, iterator)

class TestReadMeasure(unittest.TestCase):
    def testReadMeasure(self):
        data = """START_MEASURE
                  START_MEASURE_COUNT
                    BEAT_START
                      NUM_TICKS 2
                      COUNT |^+|
                    BEAT_END
                    BEAT_START
                      NUM_TICKS 2
                      COUNT |^+|
                    BEAT_END
                    BEAT_START
                      NUM_TICKS 2
                      COUNT |^+|
                    BEAT_END
                    BEAT_START
                      NUM_TICKS 2
                      COUNT |^+|
                    BEAT_END
                  END_MEASURE_COUNT
                  STARTBARLINE 1
                  NOTE 0,1,o
                  NOTE 0,2,o
                  NOTE 1,2,o
                  NOTE 2,2,o
                  NOTE 2,3,o
                  NOTE 3,2,o
                  NOTE 3,3,o
                  NOTE 4,1,o
                  NOTE 4,2,o
                  NOTE 5,2,o
                  NOTE 6,2,o
                  NOTE 6,3,o
                  NOTE 7,2,x
                  ENDBARLINE 1
                  REPEAT_COUNT 1
                  ALTERNATE
                  SIMILE 0
                  SIMINDEX 0
                END_MEASURE"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv1.MeasureStructureV1().read(iterator)
        self.assertEqual(len(measure), 8)
        self.assertEqual(measure.numNotes(), 13)
        self.assertEqual(measure.noteAt(0, 1), "o")
        self.assertEqual(measure.noteAt(0, 2), "o")
        self.assertEqual(measure.noteAt(1, 2), "o")
        self.assertEqual(measure.noteAt(2, 2), "o")
        self.assertEqual(measure.noteAt(2, 3), "o")
        self.assertEqual(measure.noteAt(3, 2), "o")
        self.assertEqual(measure.noteAt(3, 3), "o")
        self.assertEqual(measure.noteAt(4, 1), "o")
        self.assertEqual(measure.noteAt(4, 2), "o")
        self.assertEqual(measure.noteAt(5, 2), "o")
        self.assertEqual(measure.noteAt(6, 2), "o")
        self.assertEqual(measure.noteAt(6, 3), "o")
        self.assertEqual(measure.noteAt(7, 2), "x")
        self.assertFalse(measure.isRepeatStart())
        self.assertFalse(measure.isRepeatEnd())
        self.assertFalse(measure.isSectionEnd())
        self.assertFalse(measure.isLineBreak())
        self.assertEqual(measure.alternateText, None)
        self.assertEqual(measure.repeatCount, 1)

    def testReadRepeatBar(self):
        data = """START_MEASURE
                    START_MEASURE_COUNT
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                    END_MEASURE_COUNT
                    STARTBARLINE 3
                    ENDBARLINE 5
                    REPEAT_COUNT 6
                    ALTERNATE
                    SIMILE 0
                    SIMINDEX 0
                  END_MEASURE"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv1.MeasureStructureV1().read(iterator)
        self.assertEqual(measure.repeatCount, 6)
        self.assert_(measure.isRepeatStart())
        self.assert_(measure.isRepeatEnd())
        self.assertFalse(measure.isSectionEnd())
        self.assertFalse(measure.isLineBreak())

    def testReadAlternate(self):
        data = """
        START_MEASURE
          START_MEASURE_COUNT
            BEAT_START
              NUM_TICKS 4
              COUNT |^+|
            BEAT_END
            BEAT_START
              NUM_TICKS 4
              COUNT |^+|
            BEAT_END
            BEAT_START
              NUM_TICKS 4
              COUNT |^+|
            BEAT_END
            BEAT_START
              NUM_TICKS 4
              COUNT |^+|
            BEAT_END
          END_MEASURE_COUNT
          STARTBARLINE 1
          ENDBARLINE 1
          REPEAT_COUNT 2
          ALTERNATE 2.
          SIMILE 0
          SIMINDEX 0
        END_MEASURE
        """
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv1.MeasureStructureV1().read(iterator)
        self.assertEqual(measure.alternateText, "2.")

    def testReadLineBreak(self):
        data = """START_MEASURE
                    START_MEASURE_COUNT
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                    END_MEASURE_COUNT
                    STARTBARLINE 1
                    ENDBARLINE 17
                    REPEAT_COUNT 6
                    ALTERNATE
                    SIMILE 0
                    SIMINDEX 0
                  END_MEASURE"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv1.MeasureStructureV1().read(iterator)
        self.assert_(measure.isLineBreak())

    def testReadSectionEnd(self):
        data = """START_MEASURE
                    START_MEASURE_COUNT
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                    END_MEASURE_COUNT
                    STARTBARLINE 1
                    ENDBARLINE 9
                    REPEAT_COUNT 6
                    ALTERNATE
                    SIMILE 0
                    SIMINDEX 0
                  END_MEASURE"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv1.MeasureStructureV1().read(iterator)
        self.assert_(measure.isSectionEnd())

    def testReadSimile(self):
        data = """START_MEASURE
                    START_MEASURE_COUNT
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                        BEAT_START
                          NUM_TICKS 2
                          COUNT |^+|
                        BEAT_END
                    END_MEASURE_COUNT
                    STARTBARLINE 1
                    ENDBARLINE 9
                    REPEAT_COUNT 6
                    ALTERNATE
                    SIMILE 2
                    SIMINDEX 1
                  END_MEASURE"""
        handle = StringIO(data)
        iterator = fileUtils.dbFileIterator(handle)
        measure = dbfsv1.MeasureStructureV1().read(iterator)
        self.assertEqual(measure.simileDistance, 2)
        self.assertEqual(measure.simileIndex, 1)

class TestWriteMeasure(unittest.TestCase):
    reg = CounterRegistry()

    def setUp(self):
        self.measure = Measure(16)
        counter = self.reg.getCounterByName("16ths")
        mc = MeasureCount.MeasureCount()
        mc.addSimpleBeats(counter, 4)
        self.measure.setBeatCount(mc)

    def get_output(self):
        handle = StringIO()
        indenter = fileUtils.Indenter(handle)
        dbfsv1.MeasureStructureV1().write(self.measure, indenter)
        return handle.getvalue().splitlines()

    def testWriteEmpty(self):
        output = self.get_output()
        self.assertEqual(output,
                         ['START_MEASURE',
                          '  START_MEASURE_COUNT',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '  END_MEASURE_COUNT',
                          '  STARTBARLINE 1',
                          '  ENDBARLINE 1',
                          '  REPEAT_COUNT 1',
                          '  SIMILE 0',
                          '  SIMINDEX 0',
                          'END_MEASURE'])

    def testWriteSimple(self):
        self.measure.addNote(NotePosition(noteTime = 0, drumIndex = 0), "a")
        self.measure.addNote(NotePosition(noteTime = 1, drumIndex = 1), "b")
        self.measure.addNote(NotePosition(noteTime = 2, drumIndex = 0), "c")
        self.measure.addNote(NotePosition(noteTime = 3, drumIndex = 1), "d")
        self.measure.addNote(NotePosition(noteTime = 4, drumIndex = 0), "e")
        self.measure.addNote(NotePosition(noteTime = 5, drumIndex = 1), "f")
        self.measure.addNote(NotePosition(noteTime = 6, drumIndex = 0), "g")
        self.measure.addNote(NotePosition(noteTime = 7, drumIndex = 1), "h")
        self.measure.addNote(NotePosition(noteTime = 8, drumIndex = 0), "i")
        self.measure.addNote(NotePosition(noteTime = 9, drumIndex = 1), "j")
        self.measure.addNote(NotePosition(noteTime = 10, drumIndex = 0), "k")
        self.measure.addNote(NotePosition(noteTime = 11, drumIndex = 1), "l")
        self.measure.addNote(NotePosition(noteTime = 12, drumIndex = 0), "m")
        self.measure.addNote(NotePosition(noteTime = 13, drumIndex = 1), "n")
        self.measure.addNote(NotePosition(noteTime = 14, drumIndex = 0), "o")
        self.measure.addNote(NotePosition(noteTime = 15, drumIndex = 1), "p")
        output = self.get_output()
        self.assertEqual(output,
                         ['START_MEASURE',
                          '  START_MEASURE_COUNT',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '  END_MEASURE_COUNT',
                          '  STARTBARLINE 1',
                          '  NOTE 0,0,a',
                          '  NOTE 1,1,b',
                          '  NOTE 2,0,c',
                          '  NOTE 3,1,d',
                          '  NOTE 4,0,e',
                          '  NOTE 5,1,f',
                          '  NOTE 6,0,g',
                          '  NOTE 7,1,h',
                          '  NOTE 8,0,i',
                          '  NOTE 9,1,j',
                          '  NOTE 10,0,k',
                          '  NOTE 11,1,l',
                          '  NOTE 12,0,m',
                          '  NOTE 13,1,n',
                          '  NOTE 14,0,o',
                          '  NOTE 15,1,p',
                          '  ENDBARLINE 1',
                          '  REPEAT_COUNT 1',
                          '  SIMILE 0',
                          '  SIMINDEX 0',
                          'END_MEASURE'])

    def testWriteDecorations(self):
        self.measure.setLineBreak(True)
        self.measure.setSectionEnd(True)
        self.measure.setRepeatEnd(True)
        self.measure.setRepeatStart(True)
        self.measure.alternateText = "xxx"
        self.measure.repeatCount = 10
        self.measure.simileDistance = 2
        self.measure.simileIndex = 1
        output = self.get_output()
        self.assertEqual(output,
                         ['START_MEASURE',
                          '  START_MEASURE_COUNT',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '    BEAT_START',
                          '      NUM_TICKS 4',
                          '      COUNT |^e+a|',
                          '    BEAT_END',
                          '  END_MEASURE_COUNT',
                          '  STARTBARLINE 3',
                          '  ENDBARLINE 29',
                          '  REPEAT_COUNT 10',
                          '  ALTERNATE xxx',
                          '  SIMILE 2',
                          '  SIMINDEX 1',
                          'END_MEASURE'])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
