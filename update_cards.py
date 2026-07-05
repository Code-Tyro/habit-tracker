import re

with open(r'C:\Users\32258\Documents\habit\index.html', 'r', encoding='utf-8') as f:
   c = f.read()

# 1. Square checkbox -> Circular checkbox
c = c.replace(
   'border: 2.5px solid #d4c9bc; border-radius: 7px;',
   'border: 2.5px solid #d4c9bc; border-radius: 50%;'
)

# 2. Add heatmap CSS
old_css = '.check-box.checked { background: #81b29a; border-color: #81b29a; color: #fff; }'
new_css = old_css + '''
.habit-heatmap { display: flex; gap: 4px; margin-top: 10px; align-items: center; }
.heatmap-dot { width: 12px; height: 12px; border-radius: 50%; border: 1.5px solid #e0d8ce; background: transparent; flex-shrink: 0; }
.heatmap-dot.done { background: #81b29a; border-color: #81b29a; }
.heatmap-dot.today-dot { border-color: #d4a373; }
.heatmap-dot.future-dot { opacity: 0.3; }
'''
c = c.replace(old_css, new_css)

# 3. Remove old inline color overrides for today-done (we'll keep it simple)
c = c.replace(
   '.habit-card.today-done .habit-name { color: #7a8f7a; font-weight: 500; }',
   ''
)
c = c.replace(
   '.habit-card.today-done .habit-streak { opacity: 0.75; }',
   ''
)

# 4. Replace the JS card rendering section
old_render = '''      html += '<div class="habit-card' + (checked ? ' today-done' : '') + '">'
       + '<div class="habit-card-top"><div class="habit-name">' + escapeHtml(habit.name) + '</div><div class="habit-streak">' + sd + '</div></div>'
       + '<div class="habit-card-bottom">'
       + '<div class="habit-checkin"><span class="habit-checkin-label">\u4eca\u65e5</span>'
       + '<div class="check-box' + (checked ? ' checked' : '') + '" data-id="' + habit.id + '">' + (checked ? '\u2713' : '') + '</div></div>'
       + '<div class="habit-actions">'
       + '<button class="habit-btn" data-cal="' + habit.id + '">\U0001f4c5 \u65e5\u5386</button>'
       + '<button class="habit-btn delete" data-del="' + habit.id + '">\U0001f5d1</button></div></div></div>';'''

new_render = '''      html += '<div class="habit-card' + (checked ? ' today-done' : '') + '" data-id="' + habit.id + '">'
       + '<div class="habit-card-top">'
       + '<div class="check-box' + (checked ? ' checked' : '') + '" data-id="' + habit.id + '">' + (checked ? '\u2713' : '') + '</div>'
       + '<div class="habit-name">' + escapeHtml(habit.name) + '</div>'
       + '<div class="habit-streak">' + sd + '</div>'
       + '</div>'
       + '</div>';'''

if old_render in c:
   c = c.replace(old_render, new_render)
   print('Replaced render section')
else:
   print('WARNING: Could not find old render section')

# 5. Add heatmap rendering function
heatmap_fn = '''
 function renderHeatmap(habitId) {
   var data = getData(), ts = getTodayStr(), hr = data.records[habitId] || {};
   var container = document.getElementById('hm-' + habitId);
   if (!container) return;
   container.innerHTML = '';
   var today = new Date();
   for (var i = 13; i >= 0; i--) {
     var d = new Date(today); d.setDate(d.getDate() - i);
     var ds = formatDate(d);
     var dot = document.createElement('span');
     dot.className = 'heatmap-dot';
     if (hr[ds]) dot.classList.add('done');
     if (ds === ts) dot.classList.add('today-dot');
     if (d > today) dot.classList.add('future-dot');
     container.appendChild(dot);
   }
 }
'''

# Insert heatmap function before the render() function
c = c.replace('  function render() {', heatmap_fn + '\n  function render() {')

# 6. Call renderHeatmap in the render function after building HTML
old_render_end = '    PB.style.width = (total > 0 ? Math.round(done / total * 100) : 0) + \'%\';'
new_render_end = old_render_end + '''
   document.querySelectorAll('.habit-card').forEach(function(el) {
     if (el.dataset.id) renderHeatmap(el.dataset.id);
   });'''
c = c.replace(old_render_end, new_render_end)

# 7. Update the habit-card-bottom and habit-checkin, habit-actions - remove them
# Check if old bottom section exists
old_bottom = '''  .habit-card-bottom { display: flex; align-items: center; justify-content: space-between; }
 .habit-checkin { display: flex; align-items: center; gap: 10px; }
 .habit-checkin-label { font-size: 14px; color: #8c8274; }'''
c = c.replace(old_bottom, '  .habit-card-bottom { display: flex; align-items: center; justify-content: space-between; }')

# 8. Update habit-card-top to have new layout
c = c.replace(
   '.habit-card-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }',
   '.habit-card-top { display: flex; align-items: center; gap: 12px; margin-bottom: 4px; }'
)

with open(r'C:\Users\32258\Documents\habit\index.html', 'w', encoding='utf-8') as f:
   f.write(c)
print('All updates applied successfully')
