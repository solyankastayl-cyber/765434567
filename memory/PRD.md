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

## Decision Engine Philosophy (State-Oriented)
Brain/DXY/SPX — это не trading dashboard. Это decision engine.

**Терминология (State-Oriented):**
- ~~SELL~~ → **BEARISH** (красный)
- ~~BUY~~ → **BULLISH** (зелёный)
- ~~HOLD~~ → **NEUTRAL** (серый)

**Header Strip формат:**
`BULLISH SPX | Confidence: 60% | Risk: NORMAL | Phase: Distribution`

**Verdict Card:**
- Market State: BULLISH/BEARISH/NEUTRAL
- Directional Bias: SPX ↑/↓/—
- Expected (P50)
- Range (P10-P90)
- Position Size

## What's Been Implemented

### Session 1: Deployment (2026-02-28)
- Развёртывание проекта из GitHub
- TypeScript backend (Fastify) с Python proxy
- Cold Start bootstrap данных

### Session 2: DXY Horizon Dropdown (2026-02-28)
- HorizonDropdown компонент в DxyFractalPage.jsx
- Опции: 7D, 14D, 30D, 90D, 180D, 365D
- При смене горизонта перезагружаются все данные

### Session 3: State-Oriented Refactoring (2026-02-28)
**DXY Page:**
- Header Strip: BEARISH USD | Confidence | Risk | Regime
- Verdict Card: Market State + Directional Bias (без Action/SELL)
- Убраны дублирования
- Пунктирные подчёркивания убраны
- Macro Impact постоянно открыт + tooltip

**SPX Page (/fractal/spx):**
- UnifiedControlRow: BULLISH/BEARISH/NEUTRAL вместо BUY/SELL/HOLD
- State-oriented primary signal

**Компоненты обновлены:**
- `/app/frontend/src/pages/DxyFractalPage.jsx`
- `/app/frontend/src/components/spx/SpxHeaderStrip.jsx`
- `/app/frontend/src/components/spx/SpxVerdictCard.jsx` (новый)
- `/app/frontend/src/components/fractal/UnifiedControlRow.jsx`

## Active Modules
1. **BTC Fractal Terminal** - /fractal (FROZEN)
2. **DXY Fractal Decision Engine** - /dxy (active development)
3. **SPX Fractal Terminal** - /fractal/spx (state-oriented update)
4. **Macro Brain v4** - /brain
5. **Admin Panel** - /admin

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Базовое развёртывание
- [x] DXY Horizon Dropdown
- [x] State-Oriented терминология (BULLISH/BEARISH/NEUTRAL)
- [x] DXY Header Strip унификация
- [x] SPX Header унификация

### P1 (High Priority)
- [ ] SPX Verdict Card integration в /fractal/spx
- [ ] Fix NaN% в Forward Performance
- [ ] NO TRADE → Execution Mode отдельный блок
- [ ] Risk Context consistency

### P2 (Medium Priority)
- [ ] Brain v4 state-oriented update
- [ ] BTC Terminal state-oriented update
- [ ] Убрать дублирующие статусы везде

## Frozen Modules (No Changes to Logic)
- BTC Fractal Terminal (building mode)
- Brain base functionality
- Admin authentication

## Next Tasks
1. SPX Verdict Card в FractalPage
2. Fix NaN% display
3. Execution Mode блок
