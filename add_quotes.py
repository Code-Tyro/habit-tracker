with open('C:/Users/32258/Documents/habit/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add quote HTML after progress bar
old_html = b'    <div class="header-progress-bar"><div class="header-progress-bar-inner" id="progressBar"></div></div>\\r'
new_html = old_html + b'    <div class="header-quote" id="todayQuote"></div>\\r'
c = c.replace(old_html.decode('utf-8'), new_html.decode('utf-8'))

# 2. Update CSS: larger fonts + quote style
c = c.replace(
    '.header-date { font-size: 15px; color: #8c8274; }',
    '.header-date { font-size: 17px; color: #8c8274; }'
)
c = c.replace(
    '.header-progress-text { font-size: 18px; font-weight: 600; color: #3d3529; }',
    '.header-progress-text { font-size: 22px; font-weight: 700; color: #3d3529; }'
)
# Add quote CSS after header-progress-bar styles
old_css = '.header-progress-bar { height: 6px; background: #ece6de; border-radius: 3px; overflow: hidden; margin-top: 8px; }'
new_css = old_css + '\n  .header-quote { font-size: 16px; color: #b8aea0; margin-top: 12px; line-height: 1.5; font-weight: 500; }'
c = c.replace(old_css, new_css)

# 3. Add quotes array and render logic in JS
# Insert quotes array before render()
old_js = '\n  function render() {\n    var data = getData(), ts = getTodayStr(), t = new Date();\n'
new_js = '''
  var quotes = [
    '\u6bcf\u5929\u8fdb\u6b65\u4e00\u70b9\u70b9',
    '\u575a\u6301\u5c31\u662f\u80dc\u5229',
    '\u81ea\u5f8b\u7ed9\u6211\u81ea\u7531',
    '\u884c\u52a8\u662f\u6210\u529f\u7684\u5f00\u59cb',
    '\u4e00\u5207\u7686\u6709\u53ef\u80fd',
    '\u6210\u4e3a\u66f4\u597d\u7684\u81ea\u5df1',
    '\u597d\u4e60\u60ef\u9020\u5c31\u597d\u4eba\u751f'
  ];
  function setDailyQuote() {
    var t = new Date();
    var start = new Date(t.getFullYear(), 0, 0);
    var diff = t - start;
    var day = Math.floor(diff / 86400000);
    document.getElementById('todayQuote').textContent = quotes[day % quotes.length];
  }
''' + '  function render() {\n    var data = getData(), ts = getTodayStr(), t = new Date();\n'
c = c.replace(old_js, new_js)

# Add setDailyQuote call in render
old_render_start = '    TD.textContent = t.getFullYear() + '
new_render_start = '    setDailyQuote();\n    ' + old_render_start
c = c.replace(old_render_start, new_render_start)

with open('C:/Users/32258/Documents/habit/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('All changes applied')
