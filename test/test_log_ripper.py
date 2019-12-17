from logripper import LogRipper
from unittest.mock import patch

import unittest
import sys

sys.path.append('../')


class TestLogRipper(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.log_ripper = LogRipper()

    def test_class_init(self):
        self.assertEqual(self.log_ripper.days_of_week, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        self.assertEqual(self.log_ripper.connected, True)
        self.assertEqual(self.log_ripper.not_connected, False)
        self.assertEqual(self.log_ripper.disconnections, 0)
        self.assertEqual(self.log_ripper.seconds_disconnected, 0)
        self.assertEqual(self.log_ripper.began_monitoring,
                         {'weekday': '', 'calendar_day': '', 'month': '', 'year': '', 'hour': '', 'minute': '',
                          'second': '', 'day_part': '', 'timezone': ''})
        self.assertEqual(self.log_ripper.ended_monitoring,
                         {'weekday': '', 'calendar_day': '', 'month': '', 'year': '', 'hour': '', 'minute': '',
                          'second': '', 'day_part': '', 'timezone': ''})
        self.assertEqual(self.log_ripper.file_name, '')
        self.assertEqual(self.log_ripper.file_stream, None)
        self.assertEqual(self.log_ripper.lines, [])

    def test_throws_exception_when_logfile_name_not_passed(self):
        # sys.argv[1] would be a logfile name if passed in properly
        sys.argv = ['python']
        with self.assertRaises(SystemExit) as cm:
            self.log_ripper.set_filename()
        self.assertEqual(cm.exception.code, 1)

    def test_set_filename_when_logfile_name_passed(self):
        sys.argv = ['python', 'pinglog.txt']
        self.log_ripper.set_filename()
        self.assertEqual(self.log_ripper.file_name, 'pinglog.txt')

    def test_throws_exception_when_logfile_doesnt_exist(self):
        sys.argv = ['', 'non_existent_logfile.txt']
        self.log_ripper.set_filename()
        with self.assertRaises(FileNotFoundError) as cm:
            self.log_ripper.open_file_stream()
        self.assertEqual(self.log_ripper.file_name, 'non_existent_logfile.txt')

    def test_reads_in_file_when_logfile_exists(self):
        sys.argv = ['', 'testpinglog.txt']
        self.log_ripper.set_filename()
        self.log_ripper.open_file_stream()
        self.assertIsNotNone(self.log_ripper.file_stream)
        self.log_ripper.file_stream.close()

    def test_file_stream_populates_lines_array(self):
        sys.argv = ['', 'testpinglog.txt']
        self.log_ripper.set_filename()
        self.log_ripper.open_file_stream()
        self.log_ripper.populate_lines_array()
        self.assertEqual(len(self.log_ripper.lines), 3)
        self.log_ripper.file_stream.close()


if __name__ == '__main__':
    unittest.main()
