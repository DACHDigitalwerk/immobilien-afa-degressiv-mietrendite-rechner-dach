# 🏢 DACH Immobilien-AfA-, 5-%-Degressiv-Abschreibungs- (§ 7 Abs. 5a EStG), Mietrendite- & Cashflow-Rechner 2026 (`immobilien_afa_dach`)

[![CI & Pytest](https://github.com/DACHDigitalwerk/immobilien-afa-degressiv-mietrendite-rechner-dach/actions/workflows/ci.yml/badge.svg)](https://github.com/DACHDigitalwerk/immobilien-afa-degressiv-mietrendite-rechner-dach/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Live Web-App](https://img.shields.io/badge/Live_Web_App-100%25_Client_Side-10b981)](https://dachdigitalwerk.github.io/immobilien-afa-rendite-rechner/)

Steuer- und finanzmathematische Python-Bibliothek und CLI (`dach-immo-afa`) zur Berechnung der **Kaufpreisaufteilung (Grund & Boden vs. Gebäude inkl. Kaufnebenkosten)**, der **5,0 % degressiven Gebäude-AfA nach § 7 Abs. 5a EStG** inklusive optimalem Wechseljahr auf 3,0 % linear, der **5,0 % Sonder-AfA nach § 7b EStG (EH40/QNG)**, der österreichischen **beschleunigten Gebäude-AfA (4,5 % / 3,0 % / 1,5 % nach § 8 Abs. 1a / § 16 EStG AT)** sowie von **Brutto-/Nettomietrendite, Eigenkapitalrendite und Nachsteuer-Cashflow**.

---

## 🌐 Interaktive Web-Applikation & Immobilien-Steuerratgeber (100 % Client-Side)

Nutzen Sie den kostenlosen Online-Rechner mit **druckfertigem DIN-A4 Immobilien-AfA-, Kaufpreisaufteilungs- & Mietrendite-Dossier** direkt im Browser:

- 🚀 **[DACH Immobilien-AfA-, 5-%-Degressiv-Abschreibungs- (§ 7 Abs. 5a EStG), Mietrendite- & Cashflow-Rechner 2026](https://dachdigitalwerk.github.io/immobilien-afa-rendite-rechner/)**
- 📘 **[Degressive AfA Immobilien 5 Prozent (§ 7 Abs. 5a EStG) & § 7b Sonder-AfA 2026 berechnen](https://dachdigitalwerk.github.io/degressive-afa-immobilien-5-prozent-7-abs-5a-estg-rechner-2026.html)**
- 📊 **[Mietrendite berechnen 2026: Formel für Bruttomietrendite, Nettomietrendite & Eigenkapitalrendite](https://dachdigitalwerk.github.io/mietrendite-berechnen-brutto-netto-eigenkapitalrendite-cashflow-formel.html)**
- 🏗️ **[Kaufpreisaufteilung Grund und Boden vs. Gebäudeanteil 2026: AfA-Bemessungsgrundlage maximieren](https://dachdigitalwerk.github.io/kaufpreisaufteilung-grund-und-boden-gebaeudeanteil-afa-berechnen.html)**
- 🏠 **[DACH Digitalwerk – Alle 37 Self-Serve Web-Tools im Überblick](https://dachdigitalwerk.github.io/)**

---

## ✨ Kernfunktionen

1. **Gebäude-AfA-Vergleichs-Engine (DE / AT / CH):**
   - **🇩🇪 Deutschland:** 5,0 % degressive AfA (§ 7 Abs. 5a EStG) mit automatischer Bestimmung des optimalen Wechseljahrs auf 3,0 % linear (§ 7 Abs. 4 Satz 1 Nr. 2a EStG) + optional 5,0 % Sonder-AfA (§ 7b EStG bis 4.000 €/m²).
   - **🇦🇹 Österreich:** Beschleunigte Gebäude-AfA (4,5 % im 1. Jahr, 3,0 % im 2. Jahr, danach 1,5 % gem. § 8 Abs. 1a / § 16 Abs. 1 Z 8 EStG).
   - **🇨🇭 Schweiz:** Art. 32 DBG Liegenschaftsunterhaltspauschale (20 % der Bruttomieterträge) + Schuldzinsenabzug (Art. 33 DBG).
2. **Kaufpreisaufteilung & Nachsteuer-Cashflow:**
   - Berechnet abzugsfähige Gebäude-AfA-Bemessungsgrundlage, steuerliches V+V-Ergebnis, Einkommensteuer-Erstattung und Eigenkapitalrendite (Return on Equity).

---

## 📦 Installation & CLI-Nutzung

```bash
pip install -e .
dach-immo-afa --country DE --price 450000 --building-share 78 --mode degressiv_5 --rent 1650
```

---

## ⚠️ Rechtlicher Hinweis (§ 2 RDG / § 5 StBerG / § 34c GewO)

Dieses Paket dient ausschließlich der unverbindlichen finanzmathematischen Orientierung. Es stellt keine Steuer-, Rechts-, Immobilien- oder Anlageberatung dar.
