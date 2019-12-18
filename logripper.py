import sys


# sys.tracebacklimit = 0

class LogRipper(object):
    def __init__(self):
        self.days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.connected = True
        self.not_connected = False
        self.disconnections = 0
        self.seconds_disconnected = 0
        self.began_monitoring = {'weekday': '', 'calendar_day': '', 'month': '', 'year': '', 'hour': '', 'minute': '',
                                 'second': '', 'day_part': '', 'timezone': ''}
        self.ended_monitoring = {'weekday': '', 'calendar_day': '', 'month': '', 'year': '', 'hour': '', 'minute': '',
                                 'second': '', 'day_part': '', 'timezone': ''}
        self.file_name = ''
        self.file_stream = None
        self.lines = []
        self.words = None

    def set_filename(self):
        if len(sys.argv) < 2:
            print("Usage: python logripper.py <logfile.txt>")
            sys.exit(1)
        else:
            self.file_name = sys.argv[1]

    def open_file_stream(self):
        try:
            self.file_stream = open(self.file_name, 'r')
        except FileNotFoundError:
            print("File not found.  Are you sure the path is correct?")
            raise
            sys.exit(2)

    def populate_lines_array(self):
        for line in self.file_stream:
            self.lines.append(line)

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

