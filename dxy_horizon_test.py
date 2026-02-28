#!/usr/bin/env python3
"""
Test DXY Fractal API with different horizon parameters
"""

import requests
import sys
import json
from datetime import datetime

class DxyHorizonTester:
    def __init__(self, base_url="https://spx-bitcoin-core.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.results = {}

    def test_horizon_api(self, horizon):
        """Test DXY API with specific horizon"""
        url = f"{self.base_url}/api/ui/fractal/dxy/overview?h={horizon}"
        
        self.tests_run += 1
        print(f"\n🔍 Testing DXY API with horizon {horizon}...")
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('ok'):
                    self.tests_passed += 1
                    print(f"✅ API Success for {horizon}D")
                    
                    # Extract key verdict data
                    verdict = data.get('verdict', {})
                    header = data.get('header', {})
                    
                    result = {
                        'horizon': horizon,
                        'header_signal': header.get('signal'),
                        'header_confidence': header.get('confidence'),
                        'verdict_action': verdict.get('action'),
                        'verdict_bias': verdict.get('bias'),
                        'verdict_expected': verdict.get('expectedMoveP50'),
                        'verdict_confidence': verdict.get('confidence'),
                        'forecasts_count': len(data.get('forecasts', []))
                    }
                    
                    self.results[horizon] = result
                    
                    print(f"   Signal: {result['header_signal']}")
                    print(f"   Action: {result['verdict_action']}")
                    print(f"   Bias: {result['verdict_bias']}")
                    print(f"   Expected: {result['verdict_expected']}%")
                    print(f"   Forecasts: {result['forecasts_count']} entries")
                    
                    return True
                else:
                    print(f"❌ API Error for {horizon}D: {data.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ HTTP Error for {horizon}D: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Exception for {horizon}D: {str(e)}")
            return False

    def compare_horizons(self):
        """Compare results across different horizons"""
        print(f"\n📊 Horizon Comparison Results:")
        print("=" * 80)
        
        horizons = sorted(self.results.keys())
        
        if len(horizons) < 2:
            print("Not enough successful results to compare")
            return
            
        print(f"{'Horizon':<8} {'Signal':<8} {'Action':<8} {'Bias':<12} {'Expected':<10} {'Forecasts':<10}")
        print("-" * 70)
        
        for h in horizons:
            r = self.results[h]
            print(f"{h}D{'':<6} {r['header_signal'] or 'N/A':<8} {r['verdict_action'] or 'N/A':<8} {r['verdict_bias'] or 'N/A':<12} {r['verdict_expected'] or 'N/A':<10} {r['forecasts_count']:<10}")
        
        # Check for differences
        signals = set(r['header_signal'] for r in self.results.values())
        actions = set(r['verdict_action'] for r in self.results.values()) 
        biases = set(r['verdict_bias'] for r in self.results.values())
        
        print(f"\nUnique Signals: {len(signals)} - {signals}")
        print(f"Unique Actions: {len(actions)} - {actions}")
        print(f"Unique Biases: {len(biases)} - {biases}")
        
        if len(signals) > 1 or len(actions) > 1 or len(biases) > 1:
            print("✅ PASS: Data changes across different horizons")
            return True
        else:
            print("⚠️ WARN: No differences found across horizons")
            return False

def main():
    print("=== DXY Horizon API Testing ===")
    
    tester = DxyHorizonTester()
    
    # Test multiple horizons as used in the dropdown
    horizons = [7, 14, 30, 90, 180, 365]
    
    for h in horizons:
        tester.test_horizon_api(h)
    
    # Compare results
    differences_found = tester.compare_horizons()
    
    # Print summary
    print(f"\n📋 Test Summary:")
    print(f"Tests run: {tester.tests_run}")
    print(f"Tests passed: {tester.tests_passed}")
    print(f"Success rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if differences_found:
        print("✅ Horizon parameter properly affects API responses")
    else:
        print("⚠️ No horizon-based differences detected")
    
    return 0 if tester.tests_passed >= 4 else 1

if __name__ == "__main__":
    sys.exit(main())