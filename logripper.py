import sys
from datetime import datetime


# sys.tracebacklimit = 0

class LogRipper(object):
    def __init__(self):
        self.connected = True
        self.not_connected = False
        self.disconnections = 0
        self.began_monitoring = None
        self.ended_monitoring = None
        self.file_name = None
        self.file_stream = None
        self.lines = []
        self.total_seconds_logged = 0
        self.total_minutes_logged = 0
        self.total_hours_logged = 0
        self.total_days_logged = 0
        self.total_weeks_logged = 0
        self.total_months_logged = 0
        self.total_seconds_disconnected = 0
        self.average_downtime = 0
        self.average_uninterrupted_uptime = 0
        self.packet_loss = 0


    def __str__(self):
        return "connected: {0}\n" \
               "not_connected: {1}\n" \
               "disconnections: {2}\n" \
               "seconds_disconnected: {3}\n" \
               "began_monitoring: {4}\n" \
               "ended_monitoring: {5}\n" \
               "file_name: {6}\n" \
               "lines: <use print(log_ripper.get_lines_array())>\n" \
               "total_seconds_logged: {7}\n" \
               "total_minutes_logged: {8}\n" \
               "total_hours_logged: {9}\n" \
               "total_days_logged: {10}\n" \
               "total_weeks_logged: {11}\n" \
               "total_months_logged: {12}".format(
                                                self.connected,
                                                self.not_connected,
                                                self.disconnections,
                                                self.seconds_disconnected,
                                                self.get_began_monitoring(),
                                                self.get_ended_monitoring(),
                                                self.file_name,
                                                self.total_seconds_logged,
                                                self.total_minutes_logged,
                                                self.total_hours_logged,
                                                self.total_days_logged,
                                                self.total_weeks_logged,
                                                self.total_months_logged
                                            )

    """ Class Getters """
    def get_began_monitoring(self):
        return "{0}/{1}/{2} {3}:{4}:{5}".format(
            self.began_monitoring.month,
            self.began_monitoring.day,
            self.began_monitoring.year,
            self.began_monitoring.hour,
            self.began_monitoring.minute,
            self.began_monitoring.second
        )

    def get_ended_monitoring(self):
        return "{0}/{1}/{2} {3}:{4}:{5}".format(
            self.ended_monitoring.month,
            self.ended_monitoring.day,
            self.ended_monitoring.year,
            self.ended_monitoring.hour,
            self.ended_monitoring.minute,
            self.ended_monitoring.second
        )

    def get_lines_array(self):
        """
        Summary line.
        Function returns a string representation of the classes lines array
        Parameters:
            None
        Returns:
            String: Class list array to string
        """
        return '\n'.join(self.lines)

    """ Class Setters """
    def set_filename(self):
        if len(sys.argv) < 2:
            print("Usage: python logripper.py <logfile.txt>")
            sys.exit(1)
        else:
            self.file_name = sys.argv[1]

    def set_began_monitoring(self):
        timestamp = int(self.lines[1].split()[0].strip('[]').split('.')[0])
        begin_date_and_time = datetime.fromtimestamp(timestamp)
        self.began_monitoring = begin_date_and_time

    def set_ended_monitoring(self):
        timestamp = int(self.lines[len(self.lines) - 1].split()[0].strip('[]').split('.')[0])
        end_date_and_time = datetime.fromtimestamp(timestamp)
        self.ended_monitoring = end_date_and_time

    def set_connected(self, connected):
        self.connected = connected

    def set_not_connected(self, not_connected):
        self.not_connected = not_connected



    """ Class Methods """
    def open_file_stream(self):
        try:
            self.file_stream = open(self.file_name, 'r')
        except FileNotFoundError:
            print("File not found.  Are you sure the path is correct?")
            raise
            sys.exit(2)

    def populate_lines_array(self):
        for line in self.file_stream:
            self.lines.append(line.strip('\n'))

    def populate_words_array(self):
        word_array_height = len(self.lines)
        word_array_length = 0
        for line in self.lines:
            if len(line.split()) > word_array_length:
                word_array_length = len(line.split())

        self.words = [['' for i in range(word_array_length)] for j in range(word_array_height)]
        i = 0
        for line in self.lines:
            self.words[i] = line.split()
            i += 1

    def calculate_totals_logged(self):
        duration = self.ended_monitoring - self.began_monitoring
        self.total_seconds_logged = duration.total_seconds()
        self.total_minutes_logged = self.total_seconds_logged / 60
        self.total_hours_logged = self.total_minutes_logged / 60
        self.total_days_logged = self.total_hours_logged / 24
        self.total_weeks_logged = self.total_days_logged / 7
        self.total_months_logged = self.total_weeks_logged / 4

    def check_line_for_connected(self, line):
        if line.split()[1] != '64':
            self.set_connected(False)
            self.set_not_connected(True)
            return False
        else:
            self.set_connected(True)
            self.set_not_connected(False)
            return True
