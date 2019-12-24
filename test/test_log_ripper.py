from logripper import LogRipper
from datetime import datetime

import unittest
import sys

sys.path.append('../')


class TestLogRipperInit(unittest.TestCase):
    def test_class_init(self):
        log_ripper = LogRipper()
        self.assertEqual(log_ripper.connected, True)
        self.assertEqual(log_ripper.not_connected, False)
        self.assertEqual(log_ripper.disconnections, 0)
        self.assertEqual(log_ripper.began_monitoring, None)
        self.assertEqual(log_ripper.ended_monitoring, None)
        self.assertEqual(log_ripper.file_name, None)
        self.assertEqual(log_ripper.file_stream, None)
        self.assertEqual(log_ripper.lines, [])
        self.assertEqual(log_ripper.total_minutes_logged, 0)
        self.assertEqual(log_ripper.total_hours_logged, 0)
        self.assertEqual(log_ripper.total_days_logged, 0)
        self.assertEqual(log_ripper.total_months_logged, 0)
        self.assertEqual(log_ripper.total_seconds_disconnected, 0)
        self.assertEqual(log_ripper.average_downtime, 0)
        self.assertEqual(log_ripper.average_uninterrupted_uptime, 0)
        self.assertEqual(log_ripper.packet_loss, 0)


class TestLogRipperClassFieldPopulate(unittest.TestCase):
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
        self.assertEqual(len(self.log_ripper.lines), 10)

    def test_lines_array_populates_words_array(self):
        self.log_ripper.populate_lines_array()
        self.log_ripper.populate_words_array()
        self.assertIsNotNone(self.log_ripper.words)

    def test_set_began_monitoring(self):
        self.log_ripper.populate_lines_array()
        self.log_ripper.set_began_monitoring()
        self.assertNotEqual(self.log_ripper.began_monitoring, '')
        # 2019-12-23 08:59:51
        self.assertEqual(self.log_ripper.began_monitoring.year, 2019)
        self.assertEqual(self.log_ripper.began_monitoring.month, 10)
        self.assertEqual(self.log_ripper.began_monitoring.day, 1)
        self.assertEqual(self.log_ripper.began_monitoring.hour, 1)
        self.assertEqual(self.log_ripper.began_monitoring.minute, 0)
        self.assertEqual(self.log_ripper.began_monitoring.second, 0)

    def test_set_ended_monitoring(self):
        self.log_ripper.populate_lines_array()
        self.log_ripper.set_ended_monitoring()
        self.assertNotEqual(self.log_ripper.ended_monitoring, '')
        # 2019-12-23 10:02:01
        self.assertEqual(self.log_ripper.ended_monitoring.year, 2019)
        self.assertEqual(self.log_ripper.ended_monitoring.month, 12)
        self.assertEqual(self.log_ripper.ended_monitoring.day, 23)
        self.assertEqual(self.log_ripper.ended_monitoring.hour, 18)
        self.assertEqual(self.log_ripper.ended_monitoring.minute, 0)
        self.assertEqual(self.log_ripper.ended_monitoring.second, 14)

class TestLogRipperTimeParsing(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.log_ripper = LogRipper()
        sys.argv = ['', 'testpinglog.txt']
        cls.log_ripper.set_filename()
        cls.log_ripper.open_file_stream()
        cls.log_ripper.populate_lines_array()
        cls.log_ripper.set_began_monitoring()
        cls.log_ripper.set_ended_monitoring()
        cls.log_ripper.calculate_totals_logged()

    @classmethod
    def tearDown(cls):
        cls.log_ripper.file_stream.close()

    def test_calculate_totals_monitored(self):
        self.assertNotEqual(self.log_ripper.total_seconds_logged, 0)
        self.assertNotEqual(self.log_ripper.total_minutes_logged, 0)
        self.assertNotEqual(self.log_ripper.total_hours_logged, 0)
        self.assertNotEqual(self.log_ripper.total_days_logged, 0)
        self.assertNotEqual(self.log_ripper.total_weeks_logged, 0)
        self.assertNotEqual(self.log_ripper.total_months_logged, 0)

    def test_flip_connected_boolean(self):
        self.log_ripper.set_connected(False)
        self.assertFalse(self.log_ripper.connected)
        self.log_ripper.set_connected(True)
        self.assertTrue(self.log_ripper.connected)

    def test_flip_not_connected_boolean(self):
        self.log_ripper.set_not_connected(True)
        self.assertTrue(self.log_ripper.not_connected)
        self.log_ripper.set_not_connected(False)
        self.assertFalse(self.log_ripper.not_connected)

    def test_check_line_for_connected(self):
        succeeded_connecting = '[1577162654.096654] 64 bytes from 216.239.38.117 (216.239.38.117): icmp_seq=48997 ttl=51 time=18.0 ms'
        success = self.log_ripper.check_line_for_connected(succeeded_connecting)
        self.assertTrue(self.log_ripper.connected)
        self.assertTrue(success)
        failed_to_connect = '[1577145503.845204] From ubuntu-box (192.168.1.105) icmp_seq=31884 Destination Host Unreachable'
        failure = self.log_ripper.check_line_for_connected(failed_to_connect)
        self.assertFalse(self.log_ripper.connected)
        self.assertFalse(failure)




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
