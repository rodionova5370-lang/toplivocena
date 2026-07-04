"""
Ежедневное обновление тикера (курс USD/RUB, нефть Brent, дата) на всех страницах.
Не трогает цены на топливо (это делает update_prices.py, раз в неделю).

Запуск: python3 update_ticker.py
"""
import json
import re
import glob

with open('data/current-prices.json', encoding='utf-8') as f:
    data = json.load(f)

files = glob.glob('**/index.html', recursive=True)
updated = 0
for path in files:
    content = open(path, encoding='utf-8').read()
    original = content

    content = re.sub(
        r'(<span class="ticker-value" data-ticker="usd">)[^<]*(</span>)',
        rf'\g<1>{data["usd"]}\g<2>', content)
    content = re.sub(
        r'(<span class="ticker-value" data-ticker="brent">)[^<]*(</span>)',
        rf'\g<1>{data["brent"]}\g<2>', content)
    content = re.sub(
        r'(<span class="ticker-time" data-ticker="date">)[^<]*(</span>)',
        rf'\g<1>обновлено {data["ticker_date_label"]}\g<2>', content)

    if content != original:
        open(path, 'w', encoding='utf-8').write(content)
        updated += 1

print(f'Ticker (USD/Brent/date) updated in {updated} files')
