with open('C:/Users/32258/Documents/habit/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'renderHeatmap' not in line:
        new_lines.append(line)

with open('C:/Users/32258/Documents/habit/index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Removed', len(lines) - len(new_lines), 'lines with renderHeatmap')
