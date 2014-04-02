#
# Unit tests for terminal helpers
#

# Standard imports
import sys
import termcolor
import unittest

sys.path.insert(0, '..')

# Project specific imports
import outproc
import outproc.term

class ComplierCmdLineMatchTester(unittest.TestCase):

    def setUp(self):
        self.config = outproc.Config('doesnt-matter')
        self.red_fg = self.config.get_color('some', 'red', with_reset=False)
        self.yellow_fg = self.config.get_color('some', 'yellow+bold')
        self.white_fg = self.config.get_color('some', 'white')


    def test_fg2bg(self):
        self.assertEqual(outproc.term.fg2bg(self.red_fg), '\x1b[41m')


    def test_pos_to_offset_0(self):
        line = 'Hello Africa'
        colored = self.yellow_fg + line + self.config.color.reset
        #print('{}'.format(repr(colored)))

        pos = outproc.term.pos_to_offset(colored, 0)
        self.assertEqual(pos, 13)
        self.assertEqual(colored[pos], 'H')

        pos = outproc.term.pos_to_offset(colored, 6)
        self.assertEqual(pos, 19)
        self.assertEqual(colored[pos], 'A')

        pos = outproc.term.pos_to_offset(colored, len(line) - 1)
        self.assertEqual(pos, 24)
        self.assertEqual(colored[pos], 'a')


    def test_pos_to_offset_1(self):
        line = 'Hello Africa'
        colored = self.white_fg + ' ' + self.yellow_fg + line + self.config.color.reset
        #print('{}'.format(repr(colored)))
        pos = outproc.term.pos_to_offset(colored, 1)
        self.assertEqual(pos, 23)
        self.assertEqual(colored[pos], 'H')


    def test_bg_highlight_1(self):
        self.reg_bg = outproc.term.fg2bg(self.red_fg)
        line = 'Hello Africa'
        line = self.yellow_fg + line + self.config.color.reset

        pos = outproc.term.pos_to_offset(line, 0)
        self.assertEqual(line[pos], 'H')
        line = line[:pos] + self.reg_bg + line[pos:pos+1] + self.config.color.normal_bg \
          + line[pos+1:]
        self.assertEqual(line, '\x1b[0m\x1b[33m\x1b[1m\x1b[41mH\x1b[48mello Africa\x1b[0m')
        #print('{}'.format(repr(line)))
        #print('{}'.format(line))

        pos = outproc.term.pos_to_offset(line, 6)
        self.assertEqual(line[pos], 'A')
        line = line[:pos] + self.reg_bg + line[pos:pos+1] + self.config.color.normal_bg \
          + line[pos+1:]
        self.assertEqual(line, '\x1b[0m\x1b[33m\x1b[1m\x1b[41mH\x1b[48mello \x1b[41mA\x1b[48mfrica\x1b[0m')
        #print('{}'.format(repr(line)))
        #print('{}'.format(line))

        pos = outproc.term.pos_to_offset(line, 11)
        self.assertEqual(line[pos], 'a')
        line = line[:pos] + self.reg_bg + line[pos:pos+1] + self.config.color.normal_bg \
          + line[pos+1:]
        self.assertEqual(line, '\x1b[0m\x1b[33m\x1b[1m\x1b[41mH\x1b[48mello \x1b[41mA\x1b[48mfric\x1b[41ma\x1b[48m\x1b[0m')
        #print('{}'.format(repr(line)))
        #print('{}'.format(line))


    def _format_range_as_to_columns(self, count, columns):
        result = ''
        line = ''
        for i in outproc.term.column_formatter(count, columns):
            if i == -1:
                #print(line)
                result += line + '\n'
                line = ''
            else:
                line += '{} '.format(i)
        return result


    def test_column_formatter_0(self):
        for i in outproc.term.column_formatter(0, 1):
            self.assertFalse()


    def test_column_formatter_1_2(self):
        expected = '0 \n'
        result = self._format_range_as_to_columns(1, 2)
        self.assertMultiLineEqual(expected, result)


    def test_column_formatter_10_4(self):
        expected = '0 3 6 9 \n1 4 7 \n2 5 8 \n'
        result = self._format_range_as_to_columns(10, 4)
        self.assertMultiLineEqual(expected, result)


    def test_column_formatter_10_3(self):
        expected = '0 4 8 \n1 5 9 \n2 6 \n3 7 \n'
        result = self._format_range_as_to_columns(10, 3)
        self.assertMultiLineEqual(expected, result)

