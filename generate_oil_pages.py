import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, 'data', 'current-prices.json'), encoding='utf-8') as f:
    TICKER = json.load(f)

def ticker_html(prefix):
    return f'''<div class="ticker">
  <div class="wrap ticker-inner">
    <span class="ticker-item"><span class="ticker-label">USD/RUB</span><span class="ticker-value" data-ticker="usd">{TICKER["usd"]}</span></span>
    <span class="ticker-item"><span class="ticker-label">Brent</span><span class="ticker-value" data-ticker="brent">{TICKER["brent"]}</span></span>
    <span class="ticker-time" data-ticker="date">обновлено {TICKER["ticker_date_label"]}</span>
  </div>
</div>'''

# Real annual average Brent crude oil prices, $/barrel.
# Source: publicly known EIA / Bloomberg annual averages (widely republished, e.g. statista.com, macrotrends.net).
# 2025 and 2026 are not full calendar years yet on this site's timeline — marked as estimates below.
BRENT_REAL = {
    1998: 12.72, 1999: 17.97, 2000: 28.50, 2001: 24.44, 2002: 24.99,
    2003: 28.83, 2004: 38.27, 2005: 54.52, 2006: 65.14, 2007: 72.39,
    2008: 97.26, 2009: 61.67, 2010: 79.61, 2011: 111.26, 2012: 111.63,
    2013: 108.56, 2014: 98.97, 2015: 52.32, 2016: 43.55, 2017: 54.19,
    2018: 71.19, 2019: 64.16, 2020: 41.84, 2021: 70.91, 2022: 100.93,
    2023: 82.18, 2024: 80.70,
}
# Not full-year averages — taken from the site's own current ticker data, disclosed as estimates.
BRENT_ESTIMATED = {
    2025: 75.50,
    2026: 89.00,
}

BRENT_ALL = {**BRENT_REAL, **BRENT_ESTIMATED}

CONTEXT = {
    1998: "Азиатский финансовый кризис и избыток предложения обрушили цены на нефть до минимумов десятилетия.",
    2004: "Начало устойчивого роста цен на фоне растущего спроса из Китая и ограниченных свободных мощностей добычи.",
    2008: "Цена достигла исторического пика (выше $140 летом) перед резким обвалом на фоне мирового финансового кризиса.",
    2009: "Восстановление после кризиса 2008 года шло медленно — средняя цена за год осталась низкой.",
    2014: "Во второй половине года цена рухнула более чем вдвое — на рынке возник избыток предложения (сланцевая добыча в США, решение ОПЕК не сокращать добычу).",
    2015: "Продолжение падения цен — рынок оставался в состоянии перепроизводства.",
    2016: "Год минимума текущего цикла — цена опускалась ниже $30 за баррель в начале года.",
    2020: "Пандемия COVID-19 и обвал спроса на фоне локдаунов — цена кратковременно уходила в отрицательную зону по фьючерсам WTI.",
    2022: "Резкий рост цен на фоне начала военных действий на Украине и санкционного давления на российский экспорт нефти.",
    2023: "Постепенное снижение цен по мере адаптации рынка и добровольных сокращений добычи ОПЕК+.",
}


def pct(cur, prev):
    return (cur - prev) / prev * 100

years = sorted(BRENT_ALL.keys())

for y in years:
    cur = BRENT_ALL[y]
    prev_year = y - 1
    next_year = y + 1
    has_prev = prev_year in BRENT_ALL
    prev = BRENT_ALL.get(prev_year)

    is_estimate = y in BRENT_ESTIMATED
    context_line = CONTEXT.get(y, "")

    change_line = ""
    if has_prev:
        change = pct(cur, prev)
        change_str = f"{'+' if change >= 0 else ''}{change:.1f}%"
        cls = "up" if change >= 0 else "down"
        change_line = f'<p>Изменение к {prev_year} году: <span class="{cls}">{change_str}</span> ({prev:.2f} → {cur:.2f} $/барр.)</p>'

    compare_section = ""
    if has_prev:
        change = pct(cur, prev)
        change_str = f"{'+' if change >= 0 else ''}{change:.1f}%"
        cls = "up" if change >= 0 else "down"
        compare_section = f'''
  <section class="card compare-card">
    <div class="card-header">
      <h2>Сравнение с {prev_year} годом</h2>
    </div>
    <div class="table-scroll">
      <table class="compare-table">
        <thead><tr><th>Год</th><th>Цена, $/барр.</th></tr></thead>
        <tbody>
          <tr><td>{prev_year}</td><td class="mono">{prev:.2f}</td></tr>
          <tr><td>{y}</td><td class="mono {cls}">{cur:.2f}</td></tr>
        </tbody>
      </table>
    </div>
  </section>'''

    prev_link = f'<a href="../{prev_year}/index.html">← {prev_year}</a>' if prev_year >= min(years) else f'<span style="opacity:0.5;">← {prev_year}</span>'
    next_link = f'<a href="../{next_year}/index.html">{next_year} →</a>' if next_year in BRENT_ALL else f'<span style="opacity:0.5;">{next_year} →</span>'

    estimate_note = ""
    if is_estimate:
        estimate_note = f'<p class="note">Данные за {y} год — неполный год/оценка на основе текущих котировок сайта, а не годовой итог.</p>'

    intro_extra = f" {context_line}" if context_line else ""

    labels_js = str(years)
    data_js = str([round(BRENT_ALL[yy], 2) for yy in years])

    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Цена нефти в {y} году за баррель Brent</title>
<meta name="description" content="Средняя цена нефти марки Brent в {y} году — {cur:.2f} $ за баррель. Историческая динамика с 1998 года, сравнение с {prev_year if has_prev else y} годом.">
<link rel="canonical" href="https://toplivocena.ru/oil/{y}/">
<link rel="stylesheet" href="../../style.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<!-- Yandex Autoplacement 20006976 -->
<script src="https://yandex.ru/ads/system/context.js" async></script>
<script data-page-id="20006976" src="https://yandex.ru/ads/system/ap-loader.js" async></script>
</head>
<body>
<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
        m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=110363135', 'ym');

    ym(110363135, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/110363135" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->

<header class="site-header">
  <div class="wrap header-inner">
    <a href="../../index.html" class="logo">Toplivocena<span class="logo-dot">.ru</span></a>
    <nav class="main-nav">
      <a href="../../index.html#fuel">Виды топлива</a>
      <a href="../../index.html#regions">Регионы</a>
      <a href="../../index.html#compare">Сравнение</a>
      <a href="../../history/2026/index.html">История топлива</a>
      <a href="../index.html">История нефти</a>
    </nav>
  </div>
</header>

{ticker_html('../../')}

<main class="wrap">

  <div class="breadcrumbs">
    <a href="../../index.html">Главная</a><span class="sep">/</span>
    <a href="../index.html">Нефть по годам</a><span class="sep">/</span>
    <span>{y}</span>
  </div>

  <section class="fuel-hero">
    <h1>Сколько стоила нефть в {y} году</h1>
    <div class="card fuel-stat-row grid-3">
      <div class="fuel-stat">
        <div class="label">Средняя цена за год</div>
        <div class="value">{cur:.2f} $/барр.</div>
      </div>
    </div>
  </section>

  <section class="card analytics-text">
    <h2>Итоги {y} года</h2>
    <p>Средняя цена нефти марки Brent в {y} году составляла {cur:.2f} доллара за баррель.{intro_extra}</p>
    {change_line}
    {estimate_note}
  </section>

  <section class="card chart-card">
    <div class="card-header">
      <h2>Историческая динамика цены нефти Brent, 1998–2026</h2>
    </div>
    <canvas id="oilChart" height="90"></canvas>
  </section>
{compare_section}

  <section class="card">
    <div class="card-header">
      <h2>Соседние годы</h2>
    </div>
    <div class="fuel-nav-links">
      {prev_link}
      <a href="index.html" class="current">{y}</a>
      {next_link}
    </div>
  </section>

  <p class="note" style="text-align:center; padding: 0 24px 24px;">Данные по нефти Brent за {"неполный текущий год — оценка на момент обновления сайта" if is_estimate else "прошлые годы — среднегодовые значения по публичной статистике (EIA/Bloomberg)"}, не 100% точный биржевой показатель на каждый день. Подробнее — <a href="../../about/index.html">о сайте</a>.</p>

</main>

<footer class="site-footer">
  <div class="wrap footer-inner">
    <div class="footer-col">
      <div class="logo">Toplivocena<span class="logo-dot">.ru</span></div>
      <p>Аналитика цен на топливо в России</p>
    </div>
    <div class="footer-col">
      <h4>Разделы</h4>
      <a href="../../index.html#fuel">Виды топлива</a>
      <a href="../../index.html#regions">Регионы</a>
      <a href="../../history/2026/index.html">История топлива</a>
      <a href="../../about/index.html">О сайте</a>
    </div>
    <div class="footer-col">
      <h4>Источники</h4>
      <a href="https://www.eia.gov" target="_blank" rel="noopener">EIA</a>
      <a href="https://www.spimex.com" target="_blank" rel="noopener">СПбМТСБ</a>
      <a href="https://www.cbr.ru" target="_blank" rel="noopener">ЦБ РФ</a>
    </div>
  </div>
  <div class="wrap copyright">© 2026 Toplivocena.ru</div>
</footer>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Цена нефти Brent в {y} году",
  "url": "https://toplivocena.ru/oil/{y}/",
  "articleSection": "Аналитика цен на нефть"
}}
</script>

<script>
new Chart(document.getElementById('oilChart'), {{
  type: 'line',
  data: {{
    labels: {labels_js},
    datasets: [{{
      label: 'Brent, $/барр.',
      data: {data_js},
      borderColor: '#0f172a',
      backgroundColor: 'rgba(15,23,42,0.05)',
      fill: true,
      tension: 0.25,
      pointBackgroundColor: (ctx) => ctx.parsed && ctx.parsed.x === {y} ? '#dc2626' : '#0f172a'
    }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ ticks: {{ callback: v => '$' + v }} }} }} }}
}});
</script>

</body>
</html>
'''
    out_dir = os.path.join(BASE, 'oil', str(y))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Generated oil/{y}/index.html ({"estimate" if is_estimate else "real"})')

print(f"\nTotal: {len(years)} pages")

# ---- Hub page: /oil/index.html ----
year_links = "\n".join(f'      <a href="{yy}/index.html">{yy}</a>' for yy in reversed(years))
hub_labels_js = str(years)
hub_data_js = str([round(BRENT_ALL[yy], 2) for yy in years])

hub_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Цена нефти Brent по годам: 1998–2026</title>
<meta name="description" content="История цены нефти марки Brent по годам — с 1998 по 2026 год. Среднегодовые цены в долларах за баррель, график динамики.">
<link rel="canonical" href="https://toplivocena.ru/oil/">
<link rel="stylesheet" href="../style.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<!-- Yandex Autoplacement 20006976 -->
<script src="https://yandex.ru/ads/system/context.js" async></script>
<script data-page-id="20006976" src="https://yandex.ru/ads/system/ap-loader.js" async></script>
</head>
<body>
<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
        m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=110363135', 'ym');

    ym(110363135, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/110363135" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->

<header class="site-header">
  <div class="wrap header-inner">
    <a href="../index.html" class="logo">Toplivocena<span class="logo-dot">.ru</span></a>
    <nav class="main-nav">
      <a href="../index.html#fuel">Виды топлива</a>
      <a href="../index.html#regions">Регионы</a>
      <a href="../index.html#compare">Сравнение</a>
      <a href="index.html">История нефти</a>
    </nav>
  </div>
</header>

{ticker_html('../')}

<main class="wrap">

  <div class="breadcrumbs">
    <a href="../index.html">Главная</a><span class="sep">/</span>
    <span>Нефть по годам</span>
  </div>

  <section class="fuel-hero">
    <h1>Цена нефти Brent по годам</h1>
    <p>Среднегодовая цена нефти марки Brent в долларах за баррель — с 1998 по 2026 год.</p>
  </section>

  <section class="card chart-card">
    <div class="card-header">
      <h2>Историческая динамика, 1998–2026</h2>
    </div>
    <canvas id="oilHubChart" height="90"></canvas>
  </section>

  <section class="card">
    <div class="card-header">
      <h2>Выберите год</h2>
    </div>
    <div class="internal-links">
{year_links}
    </div>
  </section>

  <p class="note" style="text-align:center; padding: 0 24px 24px;">Данные за прошлые годы — среднегодовые значения по публичной статистике (EIA/Bloomberg), за текущий год — оценка на момент обновления сайта. Подробнее — <a href="../about/index.html">о сайте</a>.</p>

</main>

<footer class="site-footer">
  <div class="wrap footer-inner">
    <div class="footer-col">
      <div class="logo">Toplivocena<span class="logo-dot">.ru</span></div>
      <p>Аналитика цен на топливо в России</p>
    </div>
    <div class="footer-col">
      <h4>Разделы</h4>
      <a href="../index.html#fuel">Виды топлива</a>
      <a href="../index.html#regions">Регионы</a>
      <a href="../history/2026/index.html">История топлива</a>
      <a href="../about/index.html">О сайте</a>
    </div>
    <div class="footer-col">
      <h4>Источники</h4>
      <a href="https://www.eia.gov" target="_blank" rel="noopener">EIA</a>
      <a href="https://www.spimex.com" target="_blank" rel="noopener">СПбМТСБ</a>
      <a href="https://www.cbr.ru" target="_blank" rel="noopener">ЦБ РФ</a>
    </div>
  </div>
  <div class="wrap copyright">© 2026 Toplivocena.ru</div>
</footer>

<script>
new Chart(document.getElementById('oilHubChart'), {{
  type: 'line',
  data: {{
    labels: {hub_labels_js},
    datasets: [{{
      label: 'Brent, $/барр.',
      data: {hub_data_js},
      borderColor: '#0f172a',
      backgroundColor: 'rgba(15,23,42,0.05)',
      fill: true,
      tension: 0.25
    }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ ticks: {{ callback: v => '$' + v }} }} }} }}
}});
</script>

</body>
</html>
'''

with open(os.path.join(BASE, 'oil', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(hub_html)
print('Generated oil/index.html (hub)')
