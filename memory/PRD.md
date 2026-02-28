# Fractal Index PRD

## Original Problem Statement
Развернуть код из GitHub репозитория https://github.com/solyankastayl-cyber/dt54edcv
- Модуль фракталов для валютных пар (DXY)
- SPX и Bitcoin логика (в заморозке - поднять без изменений)
- Админка
- Подключение реальных данных на вкладке BRAIN с использованием FRED API
- **Brain v4 (Macro Brain)** - переработка Brain из dashboard в Decision Engine
- **DXY Fractal** - полная переработка в Decision Engine формат

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

## DXY Fractal Structure (Decision Engine)
### 0) Header Strip
- Signal, Confidence, Risk, Regime, Data Status

### 1) Verdict Card
- Action (BUY/SELL/HOLD)
- Bias (USD UP/DOWN/NEUTRAL)  
- Expected Move P50, Range P10-P90
- Position Size, Confidence
- Invalidations

### 2) Chart Modes
- Synthetic (Baseline Fractal)
- Replay (Historical Analogs)
- Hybrid (Combined)
- Macro (Final View with adjustment) ★

### 3) Forecast by Horizon Table
- 7D, 14D, 30D, 90D, 180D, 365D
- Synthetic, Replay, Hybrid, Macro Adj, Final, Confidence

### 4) Why This Verdict
- Key Drivers (Fed, Inflation, Credit)
- Macro Transmission (Inflation→Rates→USD→DXY)
- Invalidations

### 5) Risk Context
- Risk Level, Vol Regime, Expected Drawdown
- Position Size, Capital Scaling

### 6) Historical Analogs
- Best Match, Coverage, Sample Size
- Outcome P50, Range
- Top Matches Table

### 7) Macro Impact (collapsible)
- Score, Confidence, Regime, Delta
- Components breakdown

## What's Been Implemented (2026-02-28)

### Session 1: Deployment
- Развёртывание проекта из GitHub
- FRED API интеграция

### Session 2: Macro Brain
- Brain v4 Decision Engine
- Убраны Model Transparency/Decomposition
- Черные тултипы на заголовках

### Session 3: DXY Fractal Decision Engine
1. **Новый API endpoint**: `/api/ui/fractal/dxy/overview`
2. **Агрегированный пакет данных** с 9 компонентами
3. **Verdict-first структура** на фронтенде
4. **Реальные данные** из DXY Terminal + Macro Score
5. **Маршруты обновлены**: `/dxy` и `/fractal/dxy`

## API Endpoints
- `GET /api/ui/brain/decision` - Macro Brain Decision Engine
- `GET /api/ui/fractal/dxy/overview?h=90` - DXY Fractal Decision Engine
- `GET /api/fractal/dxy/terminal` - Raw DXY terminal data

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Базовое развёртывание
- [x] Macro Brain Decision Engine  
- [x] DXY Fractal Decision Engine

### P1 (High Priority)
- [ ] Интегрировать реальный Chart компонент в DXY page
- [ ] Кликабельный выбор горизонта (перезагрузка данных)
- [ ] SPX/BTC терминалы в Decision Engine формат

### P2 (Medium Priority)
- [ ] Кэширование API ответов
- [ ] WebSocket для realtime updates

## Next Tasks
1. Подключить FractalMainChart к DXY Decision Engine
2. Применить Decision Engine подход к SPX и BTC
3. Добавить кэширование для ускорения загрузки
