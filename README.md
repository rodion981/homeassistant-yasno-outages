# ⚡️ Home Assistant — Alerts Energy Outages (Kyiv, черга 2.2)
[![release](https://img.shields.io/github/v/release/rodion981/homeassistant-yasno-outages?display_name=tag&sort=semver)](https://github.com/rodion981/homeassistant-yasno-outages/releases)
![hacs](https://img.shields.io/badge/HACS-Custom-orange)
[![patreon](https://img.shields.io/badge/support-patreon-ff424d)](https://www.patreon.com/c/Rodion_Kurylenko)
[![twitter](https://img.shields.io/badge/twitter-@rodionkurilenko-1DA1F2)](https://twitter.com/rodion_kr)

Пакет для Home Assistant, що отримує графік відключень із
[alerts.energy/kyiv](https://alerts.energy/kyiv) і створює сенсори:
- «сьогодні» та «завтра» (до 2 періодів на добу - можна збільшити за потреби, якщо на добу буде більше відключень),
- стислий текст `*_brief`,
- бінарний сенсор «відключення зараз»,
- автомати сповіщень.

МОЖНА ЗМІНИТИ ЧЕРГУ НА ВАШУ!!!

> Працює через вбудовану REST-інтеграцію Home Assistant; HACS-залежності більше не потрібні.

## 🔧 Встановлення через HACS
1. Відкрийте **HACS → Integrations → Custom repositories**.
2. Додайте `https://github.com/rodion981/homeassistant-yasno-outages` з типом **Integration**.
3. Встановіть **Alerts Energy Outages** і перезапустіть Home Assistant.
4. Відкрийте **Settings → Devices & services → Add integration → Alerts Energy Outages** і оберіть чергу.

Інтеграція створює сенсори графіка на сьогодні/завтра та бінарний сенсор «Відключення зараз». В атрибутах доступні сирі 24 коди та всі знайдені періоди.

## 🧩 Legacy YAML-пакет

Для старої схеми встановлення можна скопіювати файл пакету вручну:

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

3. (Опційно) Додайте **автоматизації** — їх можна вставляти прямо через UI:
   - Відкрийте **Settings → Automations → Add → ... → Edit in YAML**
   - Скопіюйте вміст із `automations/*.yaml` і збережіть.

## 📊 Швидкі картки (Lovelace)
```yaml
type: entities
entities:
  - sensor.energyua_22_today_brief
  - binary_sensor.energyua_22_outage_now
  - sensor.energyua_22_tomorrow_brief
```

## 🧠 Як це працює
- **REST sensor** отримує JSON з `alerts.energy` і вибирає оператора `kyiv_oblenergo` та чергу `2.2`.
- Коди `0–3` перетворюються на періоди з точністю до 30 хвилин.
- **Template-сенсори** формують таймстемпи. `sensor.energyua_22_tomorrow_fresh`
  стає `True`, коли API віддає хоча б один період відключення на завтра.
- Автоматизації:
  - сповіщення, коли **з'явився графік на завтра**;
 

## 🧩 Залежності
- Home Assistant ≥ 2024.6
- Додаткових інтеграцій чи HACS-пакетів не потрібно

## 👤 Автор
- Made with ❤️ в Україні.
