with open('C:/Users/32258/Documents/habit/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Remove heatmap CSS
for old in [
    '.habit-heatmap { display: flex; gap: 4px; margin-top: 10px; align-items: center; }',
    '.heatmap-dot { width: 12px; height: 12px; border-radius: 50%; border: 1.5px solid #e0d8ce; background: transparent; flex-shrink: 0; }',
    '.heatmap-dot.done { background: #81b29a; border-color: #81b29a; }',
    '.heatmap-dot.today-dot { border-color: #d4a373; }',
    '.heatmap-dot.future-dot { opacity: 0.3; }',
]:
    c = c.replace(old, '')
print('1. Removed heatmap CSS')

# 2. Add strikethrough for completed habit name
c = c.replace(
    '.habit-name { font-size: 15px; font-weight: 600; flex: 1; }',
    '.habit-name { font-size: 15px; font-weight: 600; flex: 1; }.todo-done .habit-name { text-decoration: line-through; color: #bfb5a8; }'
)
print('2. Added strikethrough CSS')

# 3. Update JS card class to include todo-done
c = c.replace(
    "html += '<div class=\"habit-card' + (checked ? ' today-done' : '') + '\" data-id=\"' + habit.id + '\">'",
    "html += '<div class=\"habit-card' + (checked ? ' today-done todo-done' : '') + '\" data-id=\"' + habit.id + '\">'"
)
print('3. Updated card class')

# 4. Remove heatmap div from card
c = c.replace(
    "        + '<div class=\"habit-heatmap\" id=\"hm-' + habit.id + '\"></div>'",
    ''
)
print('4. Removed heatmap div')

# 5. Remove renderHeatmap function
old_func = "  function renderHeatmap(habitId) {\n"
old_func += "    var data = getData(), ts = getTodayStr(), hr = data.records[habitId] || {};\n"
old_func += "    var container = document.getElementById('hm-' + habitId);\n"
old_func += "    if (!container) return;\n"
old_func += "    container.innerHTML = '';\n"
old_func += "    var today = new Date();\n"
old_func += "    for (var i = 13; i >= 0; i--) {\n"
old_func += "      var d = new Date(today); d.setDate(d.getDate() - i);\n"
old_func += "      var ds = formatDate(d), dot = document.createElement('span');\n"
old_func += "      dot.className = 'heatmap-dot';\n"
old_func += "      if (hr[ds]) dot.classList.add('done');\n"
old_func += "      if (ds === ts) dot.classList.add('today-dot');\n"
old_func += "      if (d > today) dot.classList.add('future-dot');\n"
old_func += "      container.appendChild(dot);\n"
old_func += "    }\n"
old_func += "  }\n\n"
if old_func in c:
    c = c.replace(old_func, '')
    print('5. Removed renderHeatmap function')
else:
    print('5. Could not find renderHeatmap function')

# 6. Remove heatmap render call
old_call = "    document.querySelectorAll('.habit-heatmap').forEach(function(el) { renderHeatmap(el.id.replace('hm-','')); });\n"
if old_call in c:
    c = c.replace(old_call, '')
    print('6. Removed heatmap render call')
else:
    print('6. Could not find heatmap render call')

with open('C:/Users/32258/Documents/habit/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('All changes applied')
