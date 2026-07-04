"""
Обновляет "живые" блоки цен в статичном HTML на основе data/current-prices.json.
Не трогает /history/, /about/, /tools/calculator/ текст, графики Chart.js.

Запуск: python3 update_prices.py
"""
import json
import re
import glob

with open('data/current-prices.json', encoding='utf-8') as f:
    data = json.load(f)

# Ticker (USD/Brent only) is updated separately by update_ticker.py (daily).
# This script only updates fuel prices (weekly): homepage KPI/compare table + fuel hero blocks.

# --- 2. Homepage KPI cards + compare table ---
home_path = 'index.html'
content = open(home_path, encoding='utf-8').read()

for fuel, d in data['fuels'].items():
    if d['source'] == 'rosstat':
        sub = f'{d["month"]} за месяц · Росстат, {data["rosstat_week_label"]}'
    else:
        sub = f'по данным агрегаторов, {data["fuel_date_label"]}'

    # KPI card price
    content = re.sub(
        rf'(data-fuel="{fuel}">\s*<div class="kpi-top">.*?</div>\s*<div class="kpi-price" data-field="price">)[^<]*( <span class="kpi-unit">₽/л</span></div>)',
        rf'\g<1>{d["price"]}\g<2>', content, flags=re.S)
    # KPI card sub (auto-composed from date + source)
    content = re.sub(
        rf'(data-fuel="{fuel}">.*?<div class="kpi-sub" data-field="sub">)[^<]*(</div>)',
        rf'\g<1>{sub}\g<2>', content, flags=re.S)
    # compare table row
    content = re.sub(
        rf'(<tr data-fuel="{fuel}">.*?data-field="price">)[^<]*(</td>)'
        rf'(<td class="mono \w+" data-field="week">)[^<]*(</td>)'
        rf'(<td class="mono \w+" data-field="month">)[^<]*(</td>)',
        rf'\g<1>{d["price"]}\g<2>\g<3>{d["week"]}\g<4>\g<5>{d["month"]}\g<6>',
        content, flags=re.S)

open(home_path, 'w', encoding='utf-8').write(content)
print('Homepage KPI + compare table updated')

# --- 3. Fuel pages hero blocks ---
slug_map = {'ai92': 'ai-92', 'ai95': 'ai-95', 'ai98': 'ai-98', 'ai100': 'ai-100', 'dt': 'dt'}
for fuel, slug in slug_map.items():
    path = f'fuel/{slug}/index.html'
    content = open(path, encoding='utf-8').read()
    d = data['fuels'][fuel]

    content = re.sub(
        r'(data-field="price">)[^<]*( ₽/л</div>)',
        rf'\g<1>{d["price"]}\g<2>', content)
    content = re.sub(
        r'(class="value (?:up|down)" data-field="week">)[^<]*(</div>)',
        rf'\g<1>{d["week"]}\g<2>', content)
    content = re.sub(
        r'(class="value (?:up|down)" data-field="month">)[^<]*(</div>)',
        rf'\g<1>{d["month"]}\g<2>', content)
    content = re.sub(
        r'(class="value (?:up|down)" data-field="year">)[^<]*(</div>)',
        rf'\g<1>{d["year"]}\g<2>', content)
    content = re.sub(
        r'(data-field="updated">Обновлено: )[^<]*(</div>)',
        rf'\g<1>{data["fuel_date_label"]}\g<2>', content)

    open(path, 'w', encoding='utf-8').write(content)

print('Fuel pages hero blocks updated')
print('Done.')
