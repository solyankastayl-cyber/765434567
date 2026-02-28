# Fractal Index Platform PRD

## Original Problem Statement
Развёртывание проекта из GitHub репозитория https://github.com/solyankastayl-cyber/dddddd21
- Модуль фракталов для валютных пар (DXY) - основной фокус разработки
- SPX и Bitcoin логика (в заморозке - поднять без изменений)
- Админка
- FRED API для макроданных: 2c0bf55cfd182a3a4d2e4fd017a622f7

## Architecture
- **Backend**: TypeScript/Fastify на порту 8002, Python proxy на 8001
- **Frontend**: React на порту 3000
- **Database**: MongoDB
- **External APIs**: FRED API для макроданных

## Decision Engine Philosophy
Brain/DXY — это не dashboard. Это decision engine.
Отвечает на 5 вопросов:
1. Где мы сейчас? (Regime)
2. Куда рынок движется? (Bias, Expected Move)
3. Что делать? (Action: BUY/SELL/HOLD)
4. Какой риск/размер? (Position Size, Capital Scaling)
5. Почему? (Drivers, Transmission, Invalidations)

## What's Been Implemented

### Session 1: Deployment (2026-02-28)
- Развёртывание проекта из GitHub
- TypeScript backend (Fastify) с Python proxy
- Cold Start bootstrap данных (BTC 5692 candles, DXY 13366 candles, SPX 24000+ candles)
- FRED API интеграция (Fed Funds, CPI, UNRATE)

### Session 2: Horizon Dropdown (2026-02-28)
- **HorizonDropdown компонент** в DxyFractalPage.jsx
- Опции: 7D, 14D, 30D, 90D, 180D, 1Y
- Убран "(90D)" из заголовка "DXY Verdict"
- При смене горизонта перезагружаются все данные страницы:
  - Header Strip (Signal, Regime)
  - Verdict Card (Action, Bias, Expected Move)
  - Chart (обновляется forecast)
  - Forecast by Horizon таблица
  - Historical Matches
  - Risk Context
  - Macro Impact

### Active Modules
1. **BTC Fractal Terminal** - /fractal (FROZEN, production ready)
2. **DXY Fractal Decision Engine** - /dxy (active development)
3. **SPX Fractal Terminal** - /fractal/spx (FROZEN)
4. **Macro Brain v4** - /brain (Decision Engine)
5. **Admin Panel** - /admin

## API Endpoints
- `GET /api/health` - System health check
- `GET /api/ui/brain/decision` - Macro Brain Decision Engine
- `GET /api/ui/fractal/dxy/overview?h={horizon}` - DXY Fractal Decision Engine
- `GET /api/fractal/dxy/terminal` - Raw DXY terminal data
- `GET /api/fractal/signal` - BTC fractal signal
- `GET /api/fractal/spx` - SPX fractal data

## Test Results (2026-02-28)
- Session 1: 88% success (deployment)
- Session 2: 94% success (horizon dropdown)
  - Horizons 7D, 14D, 30D, 90D, 180D работают
  - 1Y имеет backend ограничение

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Базовое развёртывание из GitHub
- [x] TypeScript backend с Python proxy
- [x] Cold Start bootstrap данных
- [x] FRED API интеграция
- [x] Horizon Dropdown для DXY

### P1 (High Priority)
- [ ] Fix 1Y (365D) horizon endpoint
- [ ] Admin backend authentication
- [ ] Интегрировать реальный Chart компонент в DXY page

### P2 (Medium Priority)
- [ ] Brain v4 недостающие компоненты
- [ ] WebSocket для realtime updates
- [ ] Кэширование API ответов

## Frozen Modules (No Changes)
- BTC Fractal Terminal
- SPX Terminal (building mode)
- Brain base functionality

## Next Tasks
1. Fix 1Y horizon endpoint в backend
2. Admin backend authentication
3. Улучшить Chart компонент для DXY
