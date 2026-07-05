import sys
with open('C:/Users/32258/Documents/habit/index.html', 'rb') as f:
    lines = f.readlines()

if len(lines) > 340 and b'habit-card-top' in lines[338]:
    new_lines = [
        b"        + '<div class=\"check-box\" style=\"display:none;\">'\n",
        b"        + '</div>'\n",
        b"        + '<div class=\"habit-name\">' + escapeHtml(habit.name) + '</div>'\n",
        b"        + '<div class=\"habit-streak\">' + sd + '</div>'\n",
    ]
    # Actually, we need to replace the entire block
    # Let's just do a targeted replacement
    old = lines[337] + lines[338] + lines[339]
    new = lines[337]
    new += b"        + '<div class=\"habit-card-top\">'\n"
    new += b"        + '<div class=\"check-box' + (checked ? ' checked' : '') + '\" data-id=\"' + habit.id + '\">' + (checked ? '\xe2\x9c\x93' : '') + '</div>'\n"
    new += b"        + '<div class=\"habit-name\">' + escapeHtml(habit.name) + '</div>'\n"
    new += b"        + '<div class=\"habit-streak\">' + sd + '</div>'\n"
    new += b"        + '</div>'\n"
    new += b"        + '<div class=\"habit-heatmap\" id=\"hm-' + habit.id + '\"></div>'\n"
    new += b"        + '</div>';\n"
    # Find and replace CHECKPOINT line too
    for i, l in enumerate(lines):
        lines[i] = l.replace(b'CHECKPOINT', b'habit-card-bottom')
    # Now replace the block
    data = b''.join(lines)
    old_block = b"        + '<div class=\"habit-card-top\">'\n    }\n"
    new_block = b"        + '<div class=\"habit-card-top\">'\n"
    new_block += b"        + '<div class=\"check-box' + (checked ? ' checked' : '') + '\" data-id=\"' + habit.id + '\">' + (checked ? '\xe2\x9c\x93' : '') + '</div>'\n"
    new_block += b"        + '<div class=\"habit-name\">' + escapeHtml(habit.name) + '</div>'\n"
    new_block += b"        + '<div class=\"habit-streak\">' + sd + '</div>'\n"
    new_block += b"        + '</div>'\n"
    new_block += b"        + '<div class=\"habit-heatmap\" id=\"hm-' + habit.id + '\"></div>'\n"
    new_block += b"        + '</div>';\n"
    if old_block in data:
        data = data.replace(old_block, new_block)
        with open('C:/Users/32258/Documents/habit/index.html', 'wb') as f:
            f.write(data)
        print('Replaced successfully')
    else:
        print('Could not find old block')
        # Show what's at line 338-340
        for i in range(336, 345):
            if i < len(lines):
                print(f'{i}: {lines[i].rstrip()[:130]}')
else:
    print('Unexpected file structure')
    for i in range(334, 345):
        if i < len(lines):
            print(f'{i}: {lines[i].rstrip()[:130]}')
