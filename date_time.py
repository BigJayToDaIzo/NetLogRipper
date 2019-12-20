from datetime import datetime
import re

f = open('internetLogFile.txt', 'r')
lines = []
for line in f:
    lines.append(line)

p = re.compile('^.*:.*:.*[^:]')
m = p.search(lines[0])
print(m)
print(m.search())

datetimes = []