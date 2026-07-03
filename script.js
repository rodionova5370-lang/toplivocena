// 12-месячная динамика (АИ-92 / АИ-95), примерные помесячные значения на основе тренда роста ~1.8-2.1%/мес к июню 2026
const months = ['Июл 25','Авг 25','Сен 25','Окт 25','Ноя 25','Дек 25','Янв 26','Фев 26','Мар 26','Апр 26','Май 26','Июн 26'];
const ai92 = [61.2, 61.8, 62.3, 62.9, 63.4, 63.9, 64.5, 65.1, 65.8, 66.6, 67.5, 68.76];
const ai95 = [65.8, 66.5, 67.1, 67.8, 68.4, 69.0, 69.7, 70.4, 71.2, 72.1, 73.1, 74.38];

new Chart(document.getElementById('dynamicsChart'), {
  type: 'line',
  data: {
    labels: months,
    datasets: [
      { label: 'АИ-92', data: ai92, borderColor: '#475569', backgroundColor: 'transparent', tension: 0.3 },
      { label: 'АИ-95', data: ai95, borderColor: '#16a34a', backgroundColor: 'transparent', tension: 0.3 }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { position: 'bottom' } },
    scales: { y: { ticks: { callback: v => v + ' ₽' } } }
  }
});

// Историческая динамика 1991-2026 (ориентировочно, после деноминации 1998 года)
const historyYears = [1995, 2000, 2005, 2010, 2015, 2018, 2020, 2022, 2024, 2026];
const historyPrices = [1.2, 7.8, 15.5, 23.4, 33.9, 42.1, 45.8, 52.3, 58.9, 68.76];

new Chart(document.getElementById('historyChart'), {
  type: 'line',
  data: {
    labels: historyYears,
    datasets: [
      { label: 'АИ-92/93, ₽/л', data: historyPrices, borderColor: '#0f172a', backgroundColor: 'rgba(15,23,42,0.05)', fill: true, tension: 0.25 }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { ticks: { callback: v => v + ' ₽' } } }
  }
});

