import re, sys
with open('C:/Users/32258/Documents/habit/index.html', 'rb') as f:
    data = f.read()

old = b'habit-card-bottom'
new = b'CHECKPOINT'
data = data.replace(old, new)

with open('C:/Users/32258/Documents/habit/index.html', 'wb') as f:
    f.write(data)
print('ok')
