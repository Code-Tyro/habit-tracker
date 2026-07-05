import os

html_content = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>习惯打卡</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
background: #f6f1ea;
color: #3d3529;
min-height: 100vh;
display: flex;
justify-content: center;
padding: 24px 16px 80px;
}
.app { max-width: 540px; width: 100%; }
.header {
background: #fff;
border-radius: 16px;
padding: 24px 20px;
box-shadow: 0 2px 12px rgba(0,0,0,0.04);
margin-bottom: 16px;
}
.header-top {
display: flex;
align-items: center;
gap: 10px;
margin-bottom: 12px;
}
.header-date { font-size: 15px; color: #8c8274; }
.header-progress-text {
font-size: 18px;
font-weight: 600;
color: #3d3529;
}
.header-progress-bar {
height: 6px;
background: #ece6de;
border-radius: 3px;
overflow: hidden;
margin-top: 8px;
}
.header-progress-bar-inner {
height: 100%;
background: #81b29a;
border-radius: 3px;
transition: width 0.4s ease;
width: 0%;
}
.add-section {
background: #fff;
border-radius: 16px;
padding: 16px 20px;
box-shadow: 0 2px 12px rgba(0,0,0,0.04);
margin-bottom: 16px;
}
.add-form { display: flex; gap: 10px; align-items: center; }
.add-input {
flex: 1;
border: 2px solid #ece6de;
border-radius: 10px;
padding: 10px 14px;
font-size: 15px;
outline: none;
transition: border-color 0.2s;
background: #faf8f5;
color: #3d3529;
}
.add-input:focus { border-color: #d4a373; background: #fff; }
.add-input::placeholder { color: #b8aea0; }
.add-btn {
background: #d4a373;
color: #fff;
border: none;
border-radius: 10px;
width: 42px; height: 42px;
font-size: 22px;
cursor: pointer;
display: flex;
align-items: center;
justify-content: center;
transition: background 0.2s;
flex-shrink: 0;
}
.add-btn:hover { background: #c4915f; }
.add-btn:active { transform: scale(0.95); }
.empty-state {
text-align: center;
padding: 60px 20px;
color: #b8aea0;
font-size: 15px;
line-height: 1.8;
}
.empty-state-icon { font-size: 48px; margin-bottom: 12px; opacity: 0.5; }
.habit-card {
background: #fff;
border-radius: 16px;
padding: 16px 20px;
box-shadow: 0 2px 12px rgba(0,0,0,0.04);
margin-bottom: 12px;
transition: transform 0.15s, box-shadow 0.15s;
}
.habit-card:hover {
transform: translateY(-1px);
box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.habit-card-top {
display: flex;
align-items: center;
justify-content: space-between;
margin-bottom: 12px;
}
.habit-name { font-size: 16px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.habit-streak { font-size: 13px; color: #8c8274; display: flex; align-items: center; gap: 4px; }
.habit-streak .fire { color: #e76f51; }
.habit-streak strong { color: #3d3529; font-weight: 700; }
.habit-card-bottom { display: flex; align-items: center; justify-content: space-between; }
.habit-checkin { display: flex; align-items: center; gap: 10px; }
.habit-checkin-label { font-size: 14px; color: #8c8274; }
.check-box {
width: 28px; height: 28px;
border: 2.5px solid #d4c9bc;
border-radius: 7px;
cursor: pointer;
display: flex;
align-items: center;
justify-content: center;
transition: all 0.2s;
background: #faf8f5;
flex-shrink: 0;
font-size: 16px;
color: transparent;
user-select: none;
}
.check-box:hover { border-color: #d4a373; background: #f5ede4; }
.check-box.checked { background: #81b29a; border-color: #81b29a; color: #fff; }
.check-box.checked:hover { background: #6ea084; border-color: #6ea084; }
.habit-actions { display: flex; gap: 6px; }
.habit-btn {
background: transparent; border: none; cursor: pointer;
font-size: 13px; color: #b8aea0;
padding: 6px 8px; border-radius: 8px;
transition: all 0.2s;
display: flex; align-items: center; gap: 4px;
}
.habit-btn:hover { background: #f0ebe4; color: #3d3529; }
.habit-btn.delete:hover { background: #fce8e4; color: #c0392b; }
.modal-overlay {
display: none;
position: fixed;
inset: 0;
background: rgba(0,0,0,0.35);
z-index: 100;
align-items: center;
justify-content: center;
padding: 20px;
backdrop-filter: blur(2px);
}
.modal-overlay.open { display: flex; }
.modal {
background: #fff;
border-radius: 20px;
width: 100%;
max-width: 380px;
max-height: 90vh;
overflow-y: auto;
padding: 24px 20px 20px;
box-shadow: 0 8px 40px rgba(0,0,0,0.12);
animation: modalIn 0.25s ease;
}
@keyframes modalIn {
from { opacity: 0; transform: scale(0.94) translateY(10px); }
to { opacity: 1; transform: scale(1) translateY(0); }
}
.modal-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px; }
.modal-title { font-size: 16px; font-weight: 600; }
.modal-close {
background: none; border: none; font-size: 22px; cursor: pointer;
color: #b8aea0; width: 32px; height: 32px;
display: flex; align-items: center; justify-content: center;
border-radius: 8px; transition: all 0.15s;
}
.modal-close:hover { background: #f0ebe4; color: #3d3529; }
.modal-month-nav { display: flex; align-items: center; justify-content: center; gap: 16px; margin: 12px 0 16px; }
.modal-month-nav span { font-size: 17px; font-weight: 600; min-width: 110px; text-align: center; }
.modal-month-nav button {
background: #f0ebe4; border: none; width: 34px; height: 34px;
border-radius: 50%; cursor: pointer; font-size: 16px;
display: flex; align-items: center; justify-content: center;
transition: all 0.15s; color: #3d3529;
}
.modal-month-nav button:hover { background: #d4c9bc; }
.calendar-grid {
display: grid;
grid-template-columns: repeat(7, 1fr);
gap: 4px;
text-align: center;
margin-bottom: 16px;
}
.calendar-weekday { font-size: 12px; color: #b8aea0; padding: 6px 0; font-weight: 500; }
.calendar-day { aspect-ratio: 1; display: flex; align-items: center; justify-content: center; font-size: 14px; border-radius: 8px; transition: all 0.15s; color: #3d3529; position: relative; }
.calendar-day.future { color: #d4c9bc; }
.calendar-day.empty { visibility: hidden; }
.calendar-day.completed { background: #e4efe4; color: #5a8f5a; font-weight: 600; }
.calendar-day.today { border: 2px solid #d4a373; font-weight: 700; }
.calendar-day.today.completed { border-color: #81b29a; background: #d4e8d4; color: #3d7a3d; }
.modal-stats { background: #faf8f5; border-radius: 12px; padding: 14px 16px; display: flex; justify-content: space-around; text-align: center; }
.modal-stat-value { font-size: 18px; font-weight: 700; color: #3d3529; }
.modal-stat-label { font-size: 12px; color: #8c8274; margin-top: 2px; }
@media (max-width: 400px) {
body { padding: 16px 12px 80px; }
.header { padding: 18px 16px; }
.habit-card { padding: 14px 16px; }
.check-box { width: 26px; height: 26px; }
.modal { padding: 20px 16px; }
}
</style>
</head>
<body>
<div class="app">
<div class="header">
<div class="header-top">
<span style="font-size:22px;">&#x2600;&#xfe0f;</span>
<span class="header-date" id="todayDate"></span>
</div>
<div class="header-progress-text">
&#x5df2;&#x5b8c;&#x6210; <span id="doneCount">0</span> / <span id="totalCount">0</span>
</div>
<div class="header-progress-bar">
<div class="header-progress-bar-inner" id="progressBar"></div>
</div>
</div>
<div class="add-section">
<div class="add-form">
<input class="add-input" id="habitInput" placeholder="&#x65b0;&#x4e60;&#x60ef;&#x540d;&#x79f0;&#x2026;" maxlength="30" autocomplete="off">
<button class="add-btn" id="addBtn" title="&#x6dfb;&#x52a0;&#x4e60;&#x60ef;">+</button>
</div>
</div>
<div id="habitList"></div>
</div>

<div class="modal-overlay" id="calendarOverlay">
<div class="modal">
<div class="modal-header">
<span class="modal-title" id="modalTitle">&#x1f4c5; &#x65e5;&#x5386;</span>
<button class="modal-close" id="modalClose">&#x2715;</button>
</div>
<div class="modal-month-nav">
<button id="prevMonth">&#x25c0;</button>
<span id="monthLabel">2026&#x5e74; 7&#x6708;</span>
<button id="nextMonth">&#x25b6;</button>
</div>
<div class="calendar-grid" id="calendarGrid">
<div class="calendar-weekday">&#x4e00;</div>
<div class="calendar-weekday">&#x4e8c;</div>
<div class="calendar-weekday">&#x4e09;</div>
<div class="calendar-weekday">&#x56db;</div>
<div class="calendar-weekday">&#x4e94;</div>
<div class="calendar-weekday">&#x516d;</div>
<div class="calendar-weekday">&#x65e5;</div>
</div>
<div class="modal-stats">
<div class="modal-stat-item">
<div class="modal-stat-value" id="statStreak">0</div>
<div class="modal-stat-label">&#x8fde;&#x7eed;&#x6253;&#x5361;</div>
</div>
<div class="modal-stat-item">
<div class="modal-stat-value" id="statMonth">0/0</div>
<div class="modal-stat-label">&#x672c;&#x6708;&#x5b8c;&#x6210;</div>
</div>
<div class="modal-stat-item">
<div class="modal-stat-value" id="statTotal">0</div>
<div class="modal-stat-label">&#x603b;&#x5b8c;&#x6210;&#x5929;&#x6570;</div>
</div>
</div>
</div>
</div>

<script>
(function() {
'use strict';

const STORAGE_KEY = 'habit_tracker_data';

function getData() {
try {
const raw = localStorage.getItem(STORAGE_KEY);
if (raw) {
const data = JSON.parse(raw);
if (data && typeof data === 'object' && Array.isArray(data.habits) && data.records && typeof data.records === 'object') {
return data;
}
}
} catch(_) {}
return { habits: [], records: {} };
}

function saveData(data) {
localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

function genId() {
return Date.now().toString(36) + Math.random().toString(36).substring(2, 8);
}

function pad(n) { return String(n).padStart(2, '0'); }

function formatDate(date) {
return date.getFullYear() + '-' + pad(date.getMonth() + 1) + '-' + pad(date.getDate());
}

function getTodayStr() {
const d = new Date();
return formatDate(d);
}

const weekDays = ['&#x65e5;', '&#x4e00;', '&#x4e8c;', '&#x4e09;', '&#x56db;', '&#x4e94;', '&#x516d;'];
function getWeekDayChinese(date) { return weekDays[date.getDay()]; }

// DOM refs
const todayDateEl = document.getElementById('todayDate');
const doneCountEl = document.getElementById('doneCount');
const totalCountEl = document.getElementById('totalCount');
const progressBarEl = document.getElementById('progressBar');
const habitListEl = document.getElementById('habitList');
const habitInput = document.getElementById('habitInput');
const addBtn = document.getElementById('addBtn');
const overlay = document.getElementById('calendarOverlay');
const modalClose = document.getElementById('modalClose');
const modalTitle = document.getElementById('modalTitle');
const monthLabel = document.getElementById('monthLabel');
const prevMonthBtn = document.getElementById('prevMonth');
const nextMonthBtn = document.getElementById('nextMonth');
const calendarGrid = document.getElementById('calendarGrid');
const statStreak = document.getElementById('statStreak');
const statMonth = document.getElementById('statMonth');
const statTotal = document.getElementById('statTotal');

// Calendar modal state
let calHabitId = null;
let calYear = 0;
let calMonth = 0;

// --- Utilities ---

function calcStreak(habitId, records) {
const today = new Date();
const todayStr = formatDate(today);
const habitRecords = records[habitId] || {};

let startDate = new Date(today);
if (!habitRecords[todayStr]) {
startDate.setDate(startDate.getDate() - 1);
if (!habitRecords[formatDate(startDate)]) return 0;
}

let streak = 0;
let cur = new Date(startDate);
while (true) {
if (habitRecords[formatDate(cur)]) {
streak++;
cur.setDate(cur.getDate() - 1);
} else break;
}
return streak;
}

function calcMonthStats(habitId, records, year, month) {
const habitRecords = records[habitId] || {};
let completed = 0;
const daysInMonth = new Date(year, month + 1, 0).getDate();
for (let d = 1; d <= daysInMonth; d++) {
const dateStr = year + '-' + pad(month + 1) + '-' + pad(d);
if (habitRecords[dateStr]) completed++;
}
return { completed, total: daysInMonth };
}

function calcTotalDays(habitId, records) {
const habitRecords = records[habitId] || {};
return Object.keys(habitRecords).filter(k => habitRecords[k]).length;
}

function escapeHtml(str) {
const div = document.createElement('div');
div.textContent = str;
return div.innerHTML;
}

// --- Core actions ---

function toggleCheckIn(habitId) {
const data = getData();
const todayStr = getTodayStr();
if (!data.records[habitId]) data.records[habitId] = {};
data.records[habitId][todayStr] = !data.records[habitId][todayStr];
saveData(data);
render();
}

function addHabit() {
const name = habitInput.value.trim();
if (!name) return;
const data = getData();
data.habits.push({ id: genId(), name: name, createdAt: getTodayStr() });
saveData(data);
habitInput.value = '';
habitInput.focus();
render();
}

function deleteHabit(habitId) {
const data = getData();
const habit = data.habits.find(h => h.id === habitId);
if (!habit) return;
if (!confirm('&#x786e;&#x5b9a;&#x8981;&#x5220;&#x9664;&#x4e60;&#x60ef;&#x300c;' + habit.name + '&#x300d;&#x5417;&#xff1f;\n&#x6240;&#x6709;&#x6253;&#x5361;&#x8bb0;&#x5f55;&#x4e5f;&#x4f1a;&#x88ab;&#x5220;&#x9664;&#x3002;')) return;
data.habits = data.habits.filter(h => h.id !== habitId);
delete data.records[habitId];
saveData(data);
render();
}

// --- Calendar modal ---

function openCalendar(habitId) {
const data = getData();
const habit = data.habits.find(h => h.id === habitId);
if (!habit) return;
calHabitId = habitId;
const now = new Date();
calYear = now.getFullYear();
calMonth = now.getMonth();
modalTitle.textContent = '&#x1f4c5; ' + habit.name;
overlay.classList.add('open');
renderCalendar();
}

function closeCalendar() {
overlay.classList.remove('open');
calHabitId = null;
}

function renderCalendar() {
if (!calHabitId) return;
const data = getData();
const habitRecords = data.records[calHabitId] || {};
const todayStr = getTodayStr();

monthLabel.textContent = calYear + '&#x5e74; ' + (calMonth + 1) + '&#x6708;';

// Remove old day cells (keep weekday headers)
calendarGrid.querySelectorAll('.calendar-day').forEach(el => el.remove());

const firstDay = new Date(calYear, calMonth, 1).getDay();
const startOffset = firstDay === 0 ? 6 : firstDay - 1;
const daysInMonth = new Date(calYear, calMonth + 1, 0).getDate();

// Empty cells before 1st
for (let i = 0; i < startOffset; i++) {
const empty = document.createElement('div');
empty.className = 'calendar-day empty';
calendarGrid.appendChild(empty);
}

const today = new Date();
for (let d = 1; d <= daysInMonth; d++) {
const dateStr = calYear + '-' + pad(calMonth + 1) + '-' + pad(d);
const cell = document.createElement('div');
cell.className = 'calendar-day';
cell.textContent = d;

const isToday = dateStr === todayStr;
const isFuture = new Date(calYear, calMonth, d) > today;
const isCompleted = !!habitRecords[dateStr];

if (isFuture) cell.classList.add('future');
if (isCompleted) cell.classList.add('completed');
if (isToday) cell.classList.add('today');

calendarGrid.appendChild(cell);
}

// Update stats
statStreak.textContent = calcStreak(calHabitId, data.records);
const ms = calcMonthStats(calHabitId, data.records, calYear, calMonth);
statMonth.textContent = ms.completed + '/' + ms.total;
statTotal.textContent = calcTotalDays(calHabitId, data.records);
}

// --- Render all habits ---

function render() {
const data = getData();
const todayStr = getTodayStr();
const today = new Date();
todayDateEl.textContent = today.getFullYear() + '&#x5e74;' + (today.getMonth() + 1) + '&#x6708;' + today.getDate() + '&#x65e5; &#x5468;' + getWeekDayChinese(today);

const habits = data.habits;
const total = habits.length;
let done = 0;

if (total === 0) {
habitListEl.innerHTML = '<div class="empty-state"><div class="empty-state-icon">&#x1f4cb;</div>&#x8fd8;&#x6ca1;&#x6709;&#x4e60;&#x60ef;&#x5462;<br>&#x5728;&#x4e0a;&#x65b9;&#x6dfb;&#x52a0;&#x4f60;&#x7684;&#x7b2c;&#x4e00;&#x4e2a;&#x4e60;&#x60ef;&#x5427;</div>';
doneCountEl.textContent = '0';
totalCountEl.textContent = '0';
progressBarEl.style.width = '0%';
return;
}

let html = '';
for (const habit of habits) {
const checked = data.records[habit.id] && data.records[habit.id][todayStr];
if (checked) done++;
const streak = calcStreak(habit.id, data.records);
const streakDisplay = streak > 0
? '<span class="fire">&#x1f525;</span> &#x8fde;&#x7eed; <strong>' + streak + '</strong> &#x5929;'
: '';
html += '<div class="habit-card">'
+ '<div class="habit-card-top">'
+ '<div class="habit-name">' + escapeHtml(habit.name) + '</div>'
+ '<div class="habit-streak">' + streakDisplay + '</div>'
+ '</div>'
+ '<div class="habit-card-bottom">'
+ '<div class="habit-checkin">'
+ '<span class="habit-checkin-label">&#x4eca;&#x65e5;</span>'
+ '<div class="check-box' + (checked ? ' checked' : '') + '" data-id="' + habit.id + '">' + (checked ? '&#x2713;' : '') + '</div>'
+ '</div>'
+ '<div class="habit-actions">'
+ '<button class="habit-btn" data-cal="' + habit.id + '">&#x1f4c5; &#x65e5;&#x5386;</button>'
+ '<button class="habit-btn delete" data-del="' + habit.id + '">&#x1f5d1;</button>'
+ '</div>'
+ '</div>'
+ '</div>';
}
habitListEl.innerHTML = html;

doneCountEl.textContent = done;
totalCountEl.textContent = total;
progressBarEl.style.width = (total > 0 ? Math.round(done / total * 100) : 0) + '%';

// Bind check-boxes
document.querySelectorAll('.check-box').forEach(el => {
el.addEventListener('click', function(e) {
e.stopPropagation();
if (this.dataset.id) toggleCheckIn(this.dataset.id);
});
});
// Bind calendar buttons
document.querySelectorAll('[data-cal]').forEach(el => {
el.addEventListener('click', function(e) {
e.stopPropagation();
if (this.dataset.cal) openCalendar(this.dataset.cal);
});
});
// Bind delete buttons
document.querySelectorAll('[data-del]').forEach(el => {
el.addEventListener('click', function(e) {
e.stopPropagation();
if (this.dataset.del) deleteHabit(this.dataset.del);
});
});
}

// --- Event binding ---
addBtn.addEventListener('click', addHabit);
habitInput.addEventListener('keydown', function(e) { if (e.key === 'Enter') addHabit(); });
modalClose.addEventListener('click', closeCalendar);
overlay.addEventListener('click', function(e) { if (e.target === overlay) closeCalendar(); });
prevMonthBtn.addEventListener('click', function() { calMonth--; if (calMonth < 0) { calMonth = 11; calYear--; } renderCalendar(); });
nextMonthBtn.addEventListener('click', function() { calMonth++; if (calMonth > 11) { calMonth = 0; calYear++; } renderCalendar(); });
document.addEventListener('keydown', function(e) { if (e.key === 'Escape' && overlay.classList.contains('open')) closeCalendar(); });

// Go
render();
})();
</script>
</body>
</html>"""

with open(r'C:\Users\32258\Documents\habit\index.html', 'w', encoding='utf-8') as f:
f.write(html_content)
print('index.html written successfully')
