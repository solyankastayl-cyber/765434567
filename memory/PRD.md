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

## NEW: Macro-Adjusted Hybrid Projection (SPX)

### Philosophy
Не просто "DXY Overlay". Это **новый слой модели**:
```
SPX Hybrid → базовый прогноз
+
DXY Macro Final → корректирующий фактор
=
SPX Macro-Adjusted Hybrid (новая основная линия)
```

### Formula
```
SPX_final = SPX_hybrid + (β × overlayWeight × DXY_delta)
```

Where:
- **β** = SPX/DXY sensitivity coefficient (typically negative, -0.35 to -0.50)
- **overlayWeight** = f(corr, confidence, quality, regime)
- **DXY_delta** = expected DXY move (%)
- SPX and DXY inversely correlated: DXY BEARISH → positive SPX adjustment

### Backend: MacroOverlayEngine
- Location: `/app/backend/src/modules/spx-macro-overlay/`
- API: `GET /api/spx/macro-overlay?horizon=30d`
- Returns: adjusted projection + baseHybrid + dxyMacro + meta

### Frontend: SpxMacroView
- Location: `/app/frontend/src/components/spx/SpxMacroOverlay.jsx`
- Mode selector: Synthetic | Replay | Hybrid | **Macro ★**
- Chart: 3 lines (Adjusted solid, Base/DXY dotted)

### Guard Conditions
Overlay disabled (w=0) if:
- abs(corr) < 0.15
- confidence < 0.45
- quality < 40
- dataStatus != 'REAL'

## Decision Engine Philosophy (State-Oriented)

**Терминология:**
- ~~SELL~~ → **BEARISH** (красный)
- ~~BUY~~ → **BULLISH** (зелёный)
- ~~HOLD~~ → **NEUTRAL** (серый)

**Header Strip:**
`BULLISH SPX | Confidence: 60% | Risk: NORMAL | Phase: Distribution`

**Verdict Card:**
- Market State: BULLISH/BEARISH/NEUTRAL
- Directional Bias: SPX ↑/↓/—
- Expected (P50)
- Range (P10-P90)
- Position Size

## What's Been Implemented

### Session 1: Deployment (2026-02-28)
- Развёртывание из GitHub
- TypeScript backend + Python proxy
- Cold Start bootstrap

### Session 2: DXY Horizon Dropdown (2026-02-28)
- Dropdown с опциями: 7D, 14D, 30D, 90D, 180D, 365D
- Обновление всех данных страницы при смене

### Session 3: State-Oriented Refactoring (2026-02-28)
- DXY: BEARISH USD | Confidence | Risk | Regime
- SPX: BULLISH/BEARISH/NEUTRAL вместо BUY/SELL/HOLD
- Убраны дублирования статусов

### Session 4: SPX Macro Overlay (2026-02-28)
**Backend:**
- `MacroOverlayEngine` - калибрация β/corr по горизонтам
- API `/api/spx/macro-overlay` - adjusted projection
- Guards: minAbsCorr, minConfidence, minQuality

**Frontend:**
- `SpxMacroOverlay.jsx` - Macro ★ режим
- MACRO IMPACT panel: Base/Adjustment/Total/Strength
- Chart: 3 линии с легендой

**Калибровка:**
- Beta by horizon: 7d→-0.35, 30d→-0.42, 365d→-0.50
- Corr by horizon: 7d→-0.28, 30d→-0.35, 365d→-0.42
- Max adjustment: ±5%

## Active Modules
1. **BTC Fractal Terminal** - /fractal (FROZEN)
2. **DXY Fractal Decision Engine** - /dxy (active)
3. **SPX Fractal Terminal** - /fractal/spx (Macro ★ added)
4. **Macro Brain v4** - /brain
5. **Admin Panel** - /admin

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Deployment
- [x] DXY Horizon Dropdown
- [x] State-Oriented (BULLISH/BEARISH/NEUTRAL)
- [x] SPX Macro ★ режим
- [x] MacroOverlayEngine backend

### P1 (High Priority)
- [ ] SPX Verdict Card с macro influence строкой
- [ ] Fix overlayWeight calculation (currently 0%)
- [ ] DXY series в macro overlay

### P2 (Medium Priority)
- [ ] Brain v4 state-oriented
- [ ] BTC Terminal state-oriented
- [ ] Live β/corr calibration

## Next Tasks
1. Fix overlayWeight = 0% issue
2. Add "Macro Contribution: +X%" to SPX header
3. Improve series data quality
