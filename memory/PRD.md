# Fractal Index PRD

## Original Problem Statement
Развернуть код из GitHub репозитория https://github.com/solyankastayl-cyber/dt54edcv
- Модуль фракталов для валютных пар (DXY)
- SPX и Bitcoin логика (в заморозке - поднять без изменений)
- Админка
- Подключение реальных данных на вкладке BRAIN с использованием FRED API
- **Brain v4** - переработка Brain из dashboard в Decision Engine

## Architecture
- **Backend**: TypeScript/Fastify на порту 8002, Python proxy на 8001
- **Frontend**: React на порту 3000
- **Database**: MongoDB
- **External APIs**: FRED API для макроданных

## User Personas
1. **Трейдер** - использует BTC/SPX Fractal для анализа рыночных паттернов
2. **Аналитик** - использует Brain v4 для принятия решений на основе macro-анализа
3. **Администратор** - управляет системой через Admin Panel

## Brain v4 Philosophy
Brain — это не dashboard. Brain — это decision engine.
Он отвечает на 5 вопросов:
1. Где мы сейчас?
2. Куда рынок вероятнее всего движется?
3. Стоит ли покупать?
4. Где риск?
5. Почему ты так думаешь?

## Brain v4 Structure (Decision Engine)
### Layer 1 - Final Verdict (The Answer)
- Market Verdict: regime, dominantBias, posture, confidence
- Primary Action: actionable recommendation
- Size Guidance: multiplier, cash buffer, leverage

### Layer 2 - Why This View (Reasoning)  
- 3-5 причин с цветовой индикацией (supportive/neutral/risk)

### Layer 3 - Market Phase by Horizon
- 30D, 90D, 180D, 365D с phase и strength

### Layer 4 - Risk Map
- Volatility, Tail Risk, Guard Status, Override, Capital Scale

### Layer 5 - Causal Flow (from AE Brain)
- Inflation → Rates → USD → SPX
- Liquidity → Credit Stress → BTC

### Layer 6-9 - Detail (Transparency)
- Macro Indicators с rich tooltips
- Allocation Pipeline
- Capital Scaling
- Model Transparency

### Hidden - Advanced Decomposition
- Synthetic/Replay/Hybrid details (expandable)

## Core Requirements
- [x] BTC Fractal Terminal с прогнозами
- [x] SPX Fractal Terminal с historical pattern matching
- [x] Brain v4 Decision Engine
- [x] Admin Panel
- [x] FRED API интеграция для макроиндикаторов

## What's Been Implemented (2026-02-28)

### Session 1: Deployment
1. Развёртывание проекта из GitHub
2. FRED API интеграция (ключ: 2c0bf55cfd182a3a4d2e4fd017a622f7)
3. Macro данные загружены (16/22 серий)

### Session 2: Brain v4 Implementation
1. **Новый API endpoint**: `/api/ui/brain/decision`
2. **Новый контракт**: `BrainDecisionPack` с 11 компонентами
3. **Новый сервис**: `brain_decision.service.ts`
4. **Новый фронтенд**: `BrainOverviewPageV4.jsx`
5. **Реальные данные FRED** в Brain:
   - Fed Funds Rate: 3.64%
   - Inflation (CPI): 2.5%
   - Unemployment: 4.3%
   - Yield Curve: 1bp
   - Credit Spreads: 173bp
   - Housing: 1404K

## API Endpoints
- `GET /api/ui/brain/decision` - Brain v4 Decision Engine
- `GET /api/ui/brain/overview` - Legacy Brain v3
- `GET /api/dxy-macro-core/series` - FRED macro series
- `POST /api/dxy-macro-core/admin/ingest` - FRED data ingest

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Базовое развёртывание
- [x] Brain v4 Decision Engine

### P1 (High Priority)
- [ ] Оптимизация /api/ui/brain/decision (сейчас 10-15 сек)
- [ ] Расчёт M2 Growth YoY
- [ ] Liquidity Impulse индикатор

### P2 (Medium Priority)
- [ ] CPI YoY расчёт из исторических данных
- [ ] Gold Safe Haven индикатор
- [ ] Кэширование brain decision
- [ ] Автоматический re-ingest FRED данных

## Next Tasks
1. Оптимизировать производительность Brain Decision API
2. Добавить Liquidity Impulse из M2 данных
3. Интегрировать Gold источник данных
