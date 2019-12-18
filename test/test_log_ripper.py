from logripper import LogRipper

import unittest
import sys

sys.path.append('../')


class TestLogRipperInit(unittest.TestCase):
    def test_class_init(self):
        log_ripper = LogRipper()
        self.assertEqual(log_ripper.days_of_week, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        self.assertEqual(log_ripper.connected, True)
        self.assertEqual(log_ripper.not_connected, False)
        self.assertEqual(log_ripper.disconnections, 0)
        self.assertEqual(log_ripper.seconds_disconnected, 0)
        self.assertEqual(log_ripper.began_monitoring,
                         {'week_day': '', 'calendar_day': '', 'month': '', 'year': '', 'hour': '', 'minute': '',
                          'second': '', 'timezone': ''})
        self.assertEqual(log_ripper.ended_monitoring,
                         {'week_day': '', 'calendar_day': '', 'month': '', 'year': '', 'hour': '', 'minute': '',
                          'second': '', 'timezone': ''})
        self.assertEqual(log_ripper.file_name, '')
        self.assertEqual(log_ripper.file_stream, None)
        self.assertEqual(log_ripper.lines, [])
        self.assertEqual(log_ripper.words, None)
        self.assertEqual(log_ripper.total_minutes_logged, 0)
        self.assertEqual(log_ripper.total_hours_logged, 0)
        self.assertEqual(log_ripper.total_days_logged, 0)
        self.assertEqual(log_ripper.total_months_logged, 0)


class TestLogRipperHappy(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.log_ripper = LogRipper()
        sys.argv = ['', 'testpinglog.txt']
        cls.log_ripper.set_filename()
        cls.log_ripper.open_file_stream()

    @classmethod
    def tearDown(cls):
        cls.log_ripper.file_stream.close()

    def test_set_filename_when_logfile_name_passed(self):
        self.assertEqual(self.log_ripper.file_name, 'testpinglog.txt')

    def test_reads_in_file_when_logfile_exists(self):
        self.assertIsNotNone(self.log_ripper.file_stream)

    def test_file_stream_populates_lines_array(self):
        self.log_ripper.populate_lines_array()
        self.assertEqual(len(self.log_ripper.lines), 4)

    def test_lines_array_populates_words_array(self):
        self.log_ripper.populate_lines_array()
        self.log_ripper.populate_words_array()
        self.assertIsNotNone(self.log_ripper.words)

    def test_set_began_monitoring(self):
        self.log_ripper.populate_lines_array()
        self.log_ripper.populate_words_array()
        self.log_ripper.set_began_monitoring()
        self.assertNotEqual(self.log_ripper.began_monitoring,
                            {'week_day': '', 'calendar_day': '', 'month': '', 'year': '', 'hour': '', 'minute': '',
                             'second': '', 'timezone': ''})
        self.assertEqual(self.log_ripper.began_monitoring,
                         {'week_day': 'Tue', 'calendar_day': '17', 'month': 'Dec', 'year': '2019', 'hour': '09',
                          'minute': '50',
                          'second': '13', 'timezone': 'CST'})

    def test_set_began_monitoring_converts_pm_times_to_military(self):
        log_ripper = LogRipper()
        sys.argv = ['', 'testpinglogpm.txt']
        log_ripper.set_filename()
        log_ripper.open_file_stream()
        log_ripper.populate_lines_array()
        log_ripper.populate_words_array()
        log_ripper.set_began_monitoring()
        self.assertEqual(log_ripper.began_monitoring,
                         {'week_day': 'Tue', 'calendar_day': '17', 'month': 'Dec', 'year': '2019', 'hour': '21',
                          'minute': '50', 'second': '13', 'timezone': 'CST'})
        log_ripper.file_stream.close()

    def test_set_ended_monitoring(self):
        self.log_ripper.populate_lines_array()
        self.log_ripper.populate_words_array()
        self.log_ripper.set_ended_monitoring()
        self.assertEqual(self.log_ripper.ended_monitoring,
                         {'week_day': 'Tue', 'calendar_day': '17', 'month': 'Dec', 'year': '2019', 'hour': '09',
                          'minute': '54', 'second': '20', 'timezone': 'CST'})

    def test_set_ended_monitoring_converts_pm_times_to_military(self):
        log_ripper = LogRipper()
        sys.argv = ['', 'testpinglogpm.txt']
        log_ripper.set_filename()
        log_ripper.open_file_stream()
        log_ripper.populate_lines_array()
        log_ripper.populate_words_array()
        log_ripper.set_ended_monitoring()
        self.assertEqual(log_ripper.ended_monitoring, {'week_day': 'Tue', 'calendar_day': '17', 'month': 'Dec', 'year': '2019', 'hour': '21',
                      'minute': '54', 'second': '20', 'timezone': 'CST'})
        log_ripper.file_stream.close()

class TestLogRipperTimeParsing

class TestLogRipperSad(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.log_ripper = LogRipper()
        sys.argv = ['']

    def test_throws_exception_when_logfile_name_not_passed(self):
        # sys.argv[1] would be a logfile name if passed in properly
        with self.assertRaises(SystemExit) as cm:
            self.log_ripper.set_filename()
        self.assertEqual(cm.exception.code, 1)

    def test_throws_exception_when_logfile_doesnt_exist(self):
        sys.argv = ['', 'non_existent_logfile.txt']
        self.log_ripper.set_filename()
        with self.assertRaises(FileNotFoundError) as cm:
            self.log_ripper.open_file_stream()
        self.assertEqual(self.log_ripper.file_name, 'non_existent_logfile.txt')

    if __name__ == '__main__':
        unittest.main()
