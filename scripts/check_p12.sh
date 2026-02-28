#!/bin/bash
# P12 Run Status Checker
# Usage: ./check_p12.sh <run_id>

RUN_ID="${1:-twophase_dxy_1772281596039_1f853275}"
API_URL="http://localhost:8002"

result=$(curl -s "$API_URL/api/brain/v2/adaptive/status?id=$RUN_ID" 2>/dev/null)
status=$(echo "$result" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status','unknown'))" 2>/dev/null)

echo "Run ID: $RUN_ID"
echo "Status: $status"

if [ "$status" == "complete" ] || [ "$status" == "completed" ]; then
    echo "$result" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print()
print('='*60)
print('P12 PHASE A RESULTS (Enhanced Metrics)')
print('='*60)

report = d.get('report', {})
best = report.get('best', {})
metrics = best.get('metrics', {})

print()
print('📊 6 STANDARD METRICS:')
print(f'  avgDeltaHitRatePp: {metrics.get(\"avgDeltaHitRatePp\", \"N/A\")} (target: ≥2)')
print(f'  minDeltaPp: {metrics.get(\"minDeltaPp\", \"N/A\")} (target: ≥-1)')
print(f'  flipRatePerYear: {metrics.get(\"flipRatePerYear\", \"N/A\")} (target: ≤6)')
print(f'  avgOverrideIntensity: {metrics.get(\"avgOverrideIntensity\", \"N/A\")}')
print(f'  maxOverrideIntensity: {metrics.get(\"maxOverrideIntensity\", \"N/A\")} (target: ≤0.60)')
print(f'  stabilityScore: {metrics.get(\"stabilityScore\", \"N/A\")}')

print()
print('🎯 SCENARIO RATES:')
rates = metrics.get('scenarioRates', {})
base_rate = rates.get('BASE', 0)
risk_rate = rates.get('RISK', 0)
tail_rate = rates.get('TAIL', 0)
print(f'  BASE: {base_rate*100:.1f}% (target: 55-80%)')
print(f'  RISK: {risk_rate*100:.1f}% (target: 15-40%)')
print(f'  TAIL: {tail_rate*100:.1f}% (target: 2-20%)')

print()
print('⚡ OVERRIDE INTENSITY BY SCENARIO:')
intensity = metrics.get('overrideIntensityByScenario', {})
base_int = intensity.get('BASE', 0)
risk_int = intensity.get('RISK', 0)
tail_int = intensity.get('TAIL', 0)
print(f'  baseAvgIntensity: {base_int:.4f} (target: ≤0.35) {\"✅\" if base_int <= 0.35 else \"❌\"}'  )
print(f'  riskAvgIntensity: {risk_int:.4f} (target: ≤0.45) {\"✅\" if risk_int <= 0.45 else \"❌\"}')
print(f'  tailAvgIntensity: {tail_int:.4f} (target: ≤0.60) {\"✅\" if tail_int <= 0.60 else \"❌\"}')

print()
print('📈 DELTA BY HORIZON:')
horizons = metrics.get('deltaByHorizon', {})
print(f'  30D:  {horizons.get(\"d30\", 0):.2f}pp')
print(f'  90D:  {horizons.get(\"d90\", 0):.2f}pp')
print(f'  180D: {horizons.get(\"d180\", 0):.2f}pp')
print(f'  365D: {horizons.get(\"d365\", 0):.2f}pp')

print()
print('🚦 GATES:')
gates = report.get('gates', {})
print(f'  Passed: {gates.get(\"passed\", \"N/A\")}')
checks = gates.get('checks', {})
for k, v in checks.items():
    print(f'    {k}: {\"✅\" if v else \"❌\"}')
if gates.get('reasons'):
    print(f'  Failed reasons:')
    for r in gates.get('reasons', []):
        print(f'    - {r}')

print()
print('📋 RECOMMENDATION:', report.get('recommendation', 'N/A'))
print('='*60)
"
else
    echo "Run still in progress..."
fi
