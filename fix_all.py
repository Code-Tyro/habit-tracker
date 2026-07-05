import sys
with open('C:/Users/32258/Documents/habit/index.html', 'rb') as f:
    d = f.read()

d = d.replace(b'CHECKPOINT\n', b'')

streak_line = b'      var streak = calcStreak(habit.id, data.records);\n'
sd_line = b'     var sd = streak > 0 ? \'<span class="fire">\xf0\x9f\x94\xa5</span> \xe8\xbf\x9e\xe7\xbb\xad <strong>\' + streak + \'</strong> \xe5\xa4\xa9\' : \'\';\n'
if streak_line in d:
    d = d.replace(streak_line, streak_line + sd_line)

old_start = b"      html += '<div class=\"habit-card' + (checked ? ' today-done' : '') + '\">'\n"
old_end = b"</div></div></div>';\n"
si = d.find(old_start)
if si >= 0:
    ei = d.find(old_end, si) + len(old_end)
    new_sect = old_start
    new_sect += b"        + '<div class=\"habit-card-top\">'\n"
    new_sect += b"        + '<div class=\"check-box' + (checked ? ' checked' : '') + '\" data-id=\"' + habit.id + '\">' + (checked ? '\xe2\x9c\x93' : '') + '</div>'\n"
    new_sect += b"        + '<div class=\"habit-name\">' + escapeHtml(habit.name) + '</div>'\n"
    new_sect += b"        + '<div class=\"habit-streak\">' + sd + '</div>'\n"
    new_sect += b"        + '</div>'\n"
    new_sect += b"        + '<div class=\"habit-heatmap\" id=\"hm-' + habit.id + '\"></div>'\n"
    new_sect += b"        + '</div>';\n"
    d = d[:si] + new_sect + d[ei:]

d = d.replace(b'    document.querySelectorAll(\'.habit-card\').forEach(function(el) {', b'    document.querySelectorAll(\'[data-id]\').forEach(function(el) {')

with open('C:/Users/32258/Documents/habit/index.html', 'wb') as f:
    f.write(d)
print('Done')
import sys
with open('C:/Users/32258/Documents/habit/index.html', 'rb') as f:
    d = f.read()
d = d.replace(b'CHECKPOINT\n', b'')
old_start = b"      html += '<div class=\"habit-card' + (checked ? ' today-done' : '') + '\">'\n"
old_end = b"</div></div></div>';\n"
si = d.find(old_start)
if si >= 0:
    ei = d.find(old_end, si) + len(old_end)
    new_sect = old_start
    new_sect += b"        + '<div class=\"habit-card-top\">'\n"
    new_sect += b"        + '<div class=\"check-box' + (checked ? ' checked' : '') + '\" data-id=\"' + habit.id + '\">' + (checked ? '\xe2\x9c\x93' : '') + '</div>'\n"
    new_sect += b"        + '<div class=\"habit-name\">' + escapeHtml(habit.name) + '</div>'\n"
    new_sect += b"        + '<div class=\"habit-streak\">' + sd + '</div>'\n"
    new_sect += b"        + '</div>'\n"
    new_sect += b"        + '<div class=\"habit-heatmap\" id=\"hm-' + habit.id + '\"></div>'\n"
    new_sect += b"        + '</div>';\n"
    d = d[:si] + new_sect + d[ei:]
    print('OK')
else:
    print('Not found, searching for CHECKPOINT...')
    # Fallback: just fix the CHECKPOINT line and remaining old HTML
    line_start = b"        + '<div class=\"habit-card-top\">"
    line_end = b"        + '<button class=\"habit-btn delete\""
    ls = d.find(line_start)
    le = d.find(line_end, ls) if ls >= 0 else -1
    if ls >= 0 and le >= 0:
        le = d.find(b'\n', le) + 1
        print('Found at', ls, le)
        new_lines = b""
        d = d[:ls] + b"        + '<div class=\"habit-card-top\">'\n" + d[le:]
        # Now handle what's between CHECKPOINT and the end
        # Find CHECKPOINT line
        cp = d.find(b'CHECKPOINT')
        if cp >= 0:
            ce = d.find(b'\n', cp) + 1
            # Find checkin line
            ci = d.find(b'habit-checkin', ce)
            if ci >= 0:
                ce2 = d.find(b'\n', ci) + 1
                # Find actions line
                ai = d.find(b'habit-actions', ce2)
                if ai >= 0:
                    ae = d.find(b'\n', ai) + 1
                    # Find button line
                    bi = d.find(b'href=', ae)
                    if bi < 0: bi = d.find(b'habit-btn', ae)
                    be = d.find(b'\n', bi) + 1 if bi >= 0 else -1
                    if be >= 0:
                        rest = b"        + '<div class=\"check-box' + (checked ? ' checked' : '') + '\" data-id=\"' + habit.id + '\">' + (checked ? '\xe2\x9c\x93' : '') + '</div>'\n"
                        rest += b"        + '<div class=\"habit-name\">' + escapeHtml(habit.name) + '</div>'\n"
                        rest += b"        + '<div class=\"habit-streak\">' + sd + '</div>'\n"
                        rest += b"        + '</div>'\n"
                        rest += b"        + '<div class=\"habit-heatmap\" id=\"hm-' + habit.id + '\"></div>'\n"
                        rest += b"        + '</div>';\n"
                        d = d[:cp] + rest + d[be:]

with open('C:/Users/32258/Documents/habit/index.html', 'wb') as f:
    f.write(d)
print('Fixed')
