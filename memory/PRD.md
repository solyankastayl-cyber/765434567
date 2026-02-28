# Fractal Index PRD

## Original Problem Statement
Развернуть код из GitHub репозитория https://github.com/solyankastayl-cyber/dt54edcv
- Модуль фракталов для валютных пар (DXY)
- SPX и Bitcoin логика (в заморозке - поднять без изменений)
- Админка
- Подключение реальных данных на вкладке BRAIN с использованием FRED API

## Architecture
- **Backend**: TypeScript/Fastify на порту 8002, Python proxy на 8001
- **Frontend**: React на порту 3000
- **Database**: MongoDB
- **External APIs**: FRED API для макроданных

## User Personas
1. **Трейдер** - использует BTC/SPX Fractal для анализа рыночных паттернов
2. **Аналитик** - использует Brain v3 для macro-анализа
3. **Администратор** - управляет системой через Admin Panel

## Core Requirements
- [x] BTC Fractal Terminal с прогнозами
- [x] SPX Fractal Terminal с historical pattern matching
- [x] Brain v3 Overview с реальными macro данными
- [x] Admin Panel
- [x] FRED API интеграция для макроиндикаторов

## What's Been Implemented (2026-02-28)
1. **Развёртывание проекта** - код из GitHub склонирован и настроен
2. **FRED API интеграция** - ключ 2c0bf55cfd182a3a4d2e4fd017a622f7 добавлен
3. **Macro данные загружены** - 16/22 серий из FRED (FEDFUNDS, CPIAUCSL, UNRATE, T10Y2Y, BAA10Y, HOUST и др.)
4. **Brain Overview обновлён** - показывает реальные данные:
   - Fed Funds Rate: 3.64%
   - Inflation (CPI): 2.5%
   - Unemployment: 4.3%
   - Yield Curve: 1bp
   - Credit Spreads: 173bp
   - Housing: 1404K

## Prioritized Backlog

### P0 (Critical)
- [x] Базовое развёртывание
- [x] Реальные macro данные в Brain

### P1 (High Priority)
- [ ] Оптимизация /api/ui/brain/overview (сейчас 45+ сек)
- [ ] Расчёт M2 Growth YoY
- [ ] Liquidity Impulse индикатор
- [ ] Gold Safe Haven индикатор

### P2 (Medium Priority)
- [ ] CPI YoY расчёт из исторических данных
- [ ] Кэширование brain overview
- [ ] Автоматический re-ingest FRED данных

## Next Tasks
1. Оптимизировать производительность Brain Overview API
2. Добавить расчёт M2 Growth YoY из исторических данных
3. Интегрировать Liquidity Impulse из существующих компонентов
4. Добавить источник данных для Gold (GLD или похожий)
