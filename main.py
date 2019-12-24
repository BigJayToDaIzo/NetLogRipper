from logripper import LogRipper

log_ripper = LogRipper()
log_ripper.set_filename()
log_ripper.open_file_stream()
log_ripper.populate_lines_array()
# log_ripper.populate_words_array()
log_ripper.set_began_monitoring()
log_ripper.set_ended_monitoring()
log_ripper.calculate_totals_logged()
print(log_ripper)
print(log_ripper.get_began_monitoring())
# print(log_ripper.get_ended_monitoring())
# print(log_ripper.get_lines_array())
