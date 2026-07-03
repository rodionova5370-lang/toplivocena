import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def decline_prepositional(name):
    """Возвращает название региона в предложном падеже ('в ...') для <title>."""
    overrides = {
        'г. Москва': 'Москве',
        'г. Санкт-Петербург': 'Санкт-Петербурге',
        'г. Севастополь': 'Севастополе',
    }
    if name in overrides:
        return overrides[name]

    if name.endswith('Республика') and not name.startswith('Республика'):
        adj = name[:-len('Республика')].strip()
        if adj.endswith('ая'):
            adj = adj[:-2] + 'ой'
        elif adj.endswith('яя'):
            adj = adj[:-2] + 'ей'
        return f'{adj} Республике'

    if name.startswith('Республика '):
        rest = name[len('Республика '):]
        return f'Республике {rest}'

    if name.endswith('авт. округ'):
        adj = name[:-len('авт. округ')].strip()
        if adj.endswith('ий') or adj.endswith('ой'):
            adj = adj[:-2] + 'ом'
        return f'{adj} авт. округе'

    if name.endswith('авт. область'):
        adj = name[:-len('авт. область')].strip()
        if adj.endswith('ая'):
            adj = adj[:-2] + 'ой'
        return f'{adj} авт. области'

    if name.endswith('край'):
        adj = name[:-len('край')].strip()
        if adj.endswith('ский') or adj.endswith('цкий'):
            adj = adj[:-2] + 'ом'
        return f'{adj} крае'

    if name.endswith('область'):
        adj = name[:-len('область')].strip()
        if adj.endswith('ая'):
            adj = adj[:-2] + 'ой'
        elif adj.endswith('яя'):
            adj = adj[:-2] + 'ей'
        return f'{adj} области'

    return name

with open(os.path.join(BASE, 'data/regions_raw.csv'), encoding='utf-8') as f:
    regions = list(csv.DictReader(f))

# National averages (Rosstat bulletin, 23-29 June 2026, https://rosstat.gov.ru/storage/mediabank/102_01-07-2026.html)
NAT_AI92 = 68.76
NAT_AI95 = 74.38
NAT_DT = 84.84

def delta_str(value, national):
    d = value - national
    sign = '+' if d >= 0 else ''
    return f'{sign}{d:.2f} ₽'

def delta_cls(value, national):
    return 'up' if value >= national else 'down'

# Sort for prev/next nav (alphabetical by region name)
regions_sorted = sorted(regions, key=lambda r: r['region_name'])
slugs = [r['slug'] for r in regions_sorted]

for i, r in enumerate(regions_sorted):
    slug = r['slug']
    name = r['region_name']
    name_prep = decline_prepositional(name)
    ai92 = float(r['ai92'])
    ai95 = float(r['ai95'])
    ai98 = r['ai98']
    dt = float(r['dt'])

    ai92_delta = delta_str(ai92, NAT_AI92)
    ai92_cls = delta_cls(ai92, NAT_AI92)
    ai95_delta = delta_str(ai95, NAT_AI95)
    ai95_cls = delta_cls(ai95, NAT_AI95)
    dt_delta = delta_str(dt, NAT_DT)
    dt_cls = delta_cls(dt, NAT_DT)

    tier = 'дороже' if ai92 >= NAT_AI92 else 'дешевле'
    tier_amount = abs(ai92 - NAT_AI92)

    ai98_row = f'<tr><td>АИ-98 и выше</td><td class="mono">{float(ai98):.2f}</td><td class="mono">—</td></tr>' if ai98 else ''

    text = (
        f'В {name_prep} автомобильный бензин АИ-92 стоит {ai92:.2f} ₽ за литр — это '
        f'{"выше" if ai92 >= NAT_AI92 else "ниже"} среднего по России ({NAT_AI92:.2f} ₽) '
        f'на {tier_amount:.2f} ₽. АИ-95 в регионе продаётся по {ai95:.2f} ₽ за литр '
        f'(среднее по стране — {NAT_AI95:.2f} ₽), дизельное топливо — по {dt:.2f} ₽ за литр.'
    )

    prev_link = f'<a href="../{slugs[i-1]}/">← {regions_sorted[i-1]["region_name"]}</a>' if i > 0 else '<span style="opacity:0.5;">← нет</span>'
    next_link = f'<a href="../{slugs[i+1]}/">{regions_sorted[i+1]["region_name"]} →</a>' if i < len(regions_sorted)-1 else '<span style="opacity:0.5;">нет →</span>'

    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="yandex-verification" content="650ce87388e5f96a" />
<meta name="msvalidate.01" content="3FB04DDA2BB6883799F6E625D04971EF" />
<link rel="icon" href="../../favicon.ico" sizes="any">
<link rel="icon" href="../../favicon-32x32.png" sizes="32x32" type="image/png">
<link rel="icon" href="../../favicon-16x16.png" sizes="16x16" type="image/png">
<link rel="apple-touch-icon" sizes="180x180" href="../../apple-touch-icon.png">
<link rel="manifest" href="../../site.webmanifest">
<title>Цены на бензин в {name_prep} сегодня: стоимость за литр</title>
<meta name="description" content="Актуальная цена бензина АИ-92, АИ-95 и дизельного топлива в {name_prep}. Данные Росстата. Сравнение со средней ценой по России.">
<link rel="canonical" href="https://toplivocena.ru/regions/{slug}/">
<meta property="og:type" content="website">
<meta property="og:title" content="Цена бензина в {name_prep}">
<meta property="og:description" content="Актуальная цена бензина АИ-92, АИ-95 и дизельного топлива в {name_prep}. Данные Росстата. Сравнение со средней ценой по России.">
<meta property="og:url" content="https://toplivocena.ru/regions/{slug}/">
<meta property="og:site_name" content="Toplivocena.ru">
<meta property="og:locale" content="ru_RU">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Цена бензина в {name_prep}">
<meta name="twitter:description" content="Актуальная цена бензина АИ-92, АИ-95 и дизельного топлива в {name_prep}. Данные Росстата. Сравнение со средней ценой по России.">

<link rel="stylesheet" href="../../style.css">
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
    <a href="../../" class="logo">Toplivocena<span class="logo-dot">.ru</span></a>
    <nav class="main-nav">
      <a href="../../#fuel">Виды топлива</a>
      <a href="../../#regions">Регионы</a>
      <a href="../../#compare">Сравнение</a>
      <a href="../../#history">История</a>
    </nav>
  </div>
</header>

<div class="ticker">
  <div class="wrap ticker-inner">
    <span class="ticker-item"><span class="ticker-label">USD/RUB</span><span class="ticker-value" data-ticker="usd">77.93 ₽</span></span>
    <span class="ticker-item"><span class="ticker-label">Brent</span><span class="ticker-value" data-ticker="brent">$70.93</span></span>
    <span class="ticker-item"><span class="ticker-label">АИ-92</span><span class="ticker-value" data-ticker="ai92">68.76 ₽/л</span></span>
    <span class="ticker-item"><span class="ticker-label">АИ-95</span><span class="ticker-value" data-ticker="ai95">74.38 ₽/л</span></span>
    <span class="ticker-time" data-ticker="date">обновлено 2 июля 2026</span>
  </div>
</div>

<main class="wrap">

  <div class="breadcrumbs">
    <a href="../../">Главная</a><span class="sep">/</span>
    <a href="../../#regions">Регионы</a><span class="sep">/</span>
    <span>{name}</span>
  </div>

  <section class="fuel-hero">
    <h1>Цена бензина в {name_prep}</h1>
  </section>

  <section class="card compare-card" data-region="{slug}">
    <div class="card-header">
      <h2>Текущие цены в регионе</h2>
    </div>
    <div class="table-scroll">
      <table class="compare-table">
        <thead><tr><th>Вид топлива</th><th>Цена, ₽/л</th><th>Отклонение от среднего по РФ</th></tr></thead>
        <tbody>
          <tr><td><a href="../../fuel/ai-92/">АИ-92</a></td><td class="mono" data-field="ai92">{ai92:.2f}</td><td class="mono {ai92_cls}" data-field="ai92_delta">{ai92_delta}</td></tr>
          <tr><td><a href="../../fuel/ai-95/">АИ-95</a></td><td class="mono" data-field="ai95">{ai95:.2f}</td><td class="mono {ai95_cls}" data-field="ai95_delta">{ai95_delta}</td></tr>
          {ai98_row}
          <tr><td><a href="../../fuel/dt/">ДТ</a></td><td class="mono" data-field="dt">{dt:.2f}</td><td class="mono {dt_cls}" data-field="dt_delta">{dt_delta}</td></tr>
        </tbody>
      </table>
    </div>
    <p class="note">Данные Росстата за неделю 23–29 июня 2026 года. Среднее по России: АИ-92 — {NAT_AI92:.2f} ₽, АИ-95 — {NAT_AI95:.2f} ₽, ДТ — {NAT_DT:.2f} ₽.</p>
  </section>

  <section class="card analytics-text">
    <h2>Особенности региона</h2>
    <p>{text}</p>
  </section>

  <section class="card">
    <div class="card-header">
      <h2>Соседние регионы (по алфавиту)</h2>
    </div>
    <div class="fuel-nav-links">
      {prev_link}
      <span class="current" style="padding:6px 12px; border-radius:999px; background:var(--slate-900); color:#fff; font-size:0.85rem;">{name}</span>
      {next_link}
    </div>
    <div class="card-header" style="margin-top:24px;">
      <h2>Смотрите также</h2>
    </div>
    <div class="internal-links">
      <a href="../../fuel/ai-92/">Цена АИ-92 по России</a>
      <a href="../../fuel/ai-95/">Цена АИ-95 по России</a>
      <a href="../../fuel/dt/">Цена ДТ по России</a>
      <a href="../../#regions">Все регионы</a>
    </div>
  </section>

  <p class="note" style="text-align:center; padding: 0 24px 24px;">Часть данных на странице — расчётные оценки, а не официальная статистика. Подробнее об источниках и методологии — <a href="../../about/">о сайте</a>.</p>

</main>

<footer class="site-footer">
  <div class="wrap footer-inner">
    <div class="footer-col">
      <div class="logo">Toplivocena<span class="logo-dot">.ru</span></div>
      <p>Аналитика цен на топливо в России</p>
    </div>
    <div class="footer-col">
      <h4>Разделы</h4>
      <a href="../../#fuel">Виды топлива</a>
      <a href="../../#regions">Регионы</a>
      <a href="../../#compare">Сравнение</a>
      <a href="../../#history">История</a>
      <a href="../../about/">О сайте</a>
    </div>
    <div class="footer-col">
      <h4>Инструменты</h4>
      <a href="../../tools/calculator/">Калькулятор расхода топлива</a>
    </div>
    <div class="footer-col">
      <h4>Источники</h4>
      <a href="https://rosstat.gov.ru" target="_blank" rel="noopener">Росстат</a>
      <a href="https://www.spimex.com" target="_blank" rel="noopener">СПбМТСБ</a>
      <a href="https://www.cbr.ru" target="_blank" rel="noopener">ЦБ РФ</a>
    </div>
  </div>
  <div class="wrap copyright">© 2026 Toplivocena.ru</div>
</footer>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Цена бензина в {name_prep}",
  "url": "https://toplivocena.ru/regions/{slug}/"
}}
</script>

</body>
</html>
'''
    out_dir = os.path.join(BASE, 'regions', slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

print(f'Generated {len(regions_sorted)} region pages')
