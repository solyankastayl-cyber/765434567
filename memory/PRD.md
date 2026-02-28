# Fractal Platform PRD

## Original Problem Statement
1. Развернуть код Fractal Platform из GitHub
2. Реализовать v2.3 Capital Scaling (Risk Budget Targeting)
3. Создать User Brain Page v3 — институциональный AI Macro Risk Dashboard

## System Version
- **Core**: v2.2.0-production-baseline (FROZEN)
- **Capital Scaling**: v2.3.0-production (ACTIVE)
- **Brain Page**: v3.0

## What's Been Implemented

### 2026-02-28 — v2.3 Capital Scaling
- [x] System freeze (v2.2.0)
- [x] Capital Scaling module (10/10 tests pass)
- [x] P13 validation: Sharpe +1.19, MaxDD -24.45%
- [x] Production activation (capitalMode=on)

### 2026-02-28 — Brain Page v3
- [x] Backend API: /api/ui/brain/overview
- [x] Aggregated BrainOverviewPack structure
- [x] Frontend: BrainOverviewPage.jsx

**UI Components:**
- Health Strip (scenario, posture, guard, scale factor)
- Macro Indicators (9 cards grid)
- Macro Engine Output (score, regime, drivers, stability)
- Macro → Market Transmission (3 channels)
- Forecast by Horizon (30D/90D/180D/365D table)
- Scenario & Recommendations
- Allocation Pipeline (Base → After Brain → Final)
- Capital Scaling block (scale factor, drivers)
- Model Transparency (audit)

## API Endpoints

### Capital Scaling
```
GET  /api/capital-scaling/health
GET  /api/capital-scaling/preview
POST /api/capital-scaling/apply
GET  /api/capital-scaling/config
GET  /api/capital-scaling/test
```

### Brain Overview
```
GET /api/ui/brain/overview
GET /api/ui/brain/health
```

### Engine
```
GET /api/engine/global?brain=1&optimizer=1&capital=1
```

## Frontend Routes
- `/brain` — Brain Overview Page v3
- `/intelligence/brain` — альтернативный путь

## Test Results
- Capital Scaling: 10/10 PASS
- P13 Validation: PASS
- Brain Overview API: PASS
- Frontend: PASS (loads in ~10-15s)

## Backlog

### P0 (Done)
- [x] Deploy platform ✓
- [x] v2.3 Capital Scaling ✓
- [x] Brain Page v3 ✓

### P1 (Next)
- [ ] Add Brain Page to Intelligence menu
- [ ] Cache API response for faster load
- [ ] Populate FRED macro data

### P2 (Future)
- [ ] Admin Brain Page (parameter tuning)
- [ ] Historical scaleFactor visualization
- [ ] Portfolio vol calculation
