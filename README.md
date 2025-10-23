# ⚡️ Home Assistant — EnergyUA Outages Parser (Kyiv, Черга 2-2)

Пакет для Home Assistant, що парсить графік відключень із
[kyiv.energy-ua.info/cherga/2-2](https://kyiv.energy-ua.info/cherga/2-2) і створює сенсори:
- «сьогодні» та «завтра» (до 2 періодів на добу - можна збільшити за потреби, якщо на добу буде більше відключень),
- стислий текст `*_brief`,
- бінарний сенсор «відключення зараз»,
- автомати сповіщень.

> Працює через інтеграцію [`multiscrape`](https://github.com/danieldotnl/ha-multiscrape).

## 🔧 Встановлення
1. Скопіюйте файл пакету до вашого HA:
   ```yaml
   /config/includes/packages/energyua_22.yaml
   ```
   і переконайтесь, що у `configuration.yaml` є:
   ```yaml
   homeassistant:
     packages: !include_dir_named includes/packages
   ```
2. Перезапустіть Home Assistant (або *Reload Template Entities* + *Reload All*).


## 📊 Швидкі картки (Lovelace)
```yaml
type: entities
entities:
  - sensor.energyua_22_today_brief
  - binary_sensor.energyua_22_outage_now
  - sensor.energyua_22_tomorrow_brief
```

## 🧠 Як це працює
- **Multiscrape** тягне HTML та парсить секції «на сьогодні/на завтра».
- **Template-сенсори** формують таймстемпи. Для «завтра» доданий анти‑залипання механізм:
  `sensor.energyua_22_tomorrow_fresh` → True тільки коли з'явилися **нові** завтрашні дані,
  які **не збігаються** з сьогоднішніми.
- Автоматизації:
  - сповіщення при **фактичному** відключенні в межах графіка (‑15 хв до старту → до кінця);
  - сповіщення, коли **з'явився графік на завтра**;
  - сповіщення **поза графіком** з випадковим повідомленням.

## 🧩 Залежності
- Home Assistant ≥ 2024.6
- HACS або вручну: `multiscrape`

## 👤 Автор
- Made with ❤️ в Україні.
