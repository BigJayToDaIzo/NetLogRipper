import sys


# sys.tracebacklimit = 0

class LogRipper(object):
    def __init__(self):
        self.days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.connected = True
        self.not_connected = False
        self.disconnections = 0
        self.seconds_disconnected = 0
        self.began_monitoring = {'week_day': '', 'calendar_day': '', 'month': '', 'year': '', 'hour': '', 'minute': '',
                                 'second': '', 'timezone': ''}
        self.ended_monitoring = {'week_day': '', 'calendar_day': '', 'month': '', 'year': '', 'hour': '', 'minute': '',
                                 'second': '', 'timezone': ''}
        self.file_name = ''
        self.file_stream = None
        self.lines = []
        self.words = None
        self.total_minutes_logged = 0
        self.total_hours_logged = 0
        self.total_days_logged = 0
        self.total_months_logged = 0g

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

    def set_began_monitoring(self):
        self.began_monitoring['week_day'] = self.words[0][0]
        self.began_monitoring['calendar_day'] = self.words[0][1]
        self.began_monitoring['month'] = self.words[0][2]
        self.began_monitoring['year'] = self.words[0][3]
        hour_min_sec = self.words[0][4].split(":")
        # convert to military time for easier time math
        if self.words[0][5] == "PM":
            if int(hour_min_sec[0]) < 12:
                temp_int = int(hour_min_sec[0])
                temp_int += 12
                hour_min_sec[0] = str(temp_int)
        self.began_monitoring['hour'] = hour_min_sec[0]
        self.began_monitoring['minute'] = hour_min_sec[1]
        self.began_monitoring['second'] = hour_min_sec[2]
        self.began_monitoring['timezone'] = self.words[0][6].strip(':')

    def set_ended_monitoring(self):
        lastIndex = len(self.lines) - 1
        self.ended_monitoring['week_day'] = self.words[lastIndex][0]
        self.ended_monitoring['calendar_day'] = self.words[lastIndex][1]
        self.ended_monitoring['month'] = self.words[lastIndex][2]
        self.ended_monitoring['year'] = self.words[lastIndex][3]
        hour_min_sec = self.words[lastIndex][4].split(":")
        if self.words[lastIndex][5] == "PM":
            if int(hour_min_sec[0]) < 12:
                temp_int = int(hour_min_sec[0])
                temp_int += 12
                hour_min_sec[0] = str(temp_int)
        self.ended_monitoring['hour'] = hour_min_sec[0]
        self.ended_monitoring['minute'] = hour_min_sec[1]
        self.ended_monitoring['second'] = hour_min_sec[2]
        self.ended_monitoring['timezone'] = self.words[lastIndex][6].strip(":")
