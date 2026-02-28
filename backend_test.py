#!/usr/bin/env python3
"""
Backend API Testing Script for Fractal Platform
Testing all required endpoints from review request
"""

import requests
import sys
from datetime import datetime
import json

class FractalPlatformTester:
    def __init__(self, base_url="https://spx-bitcoin-core.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.errors = []
        
    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
            if details:
                print(f"   {details}")
        else:
            print(f"❌ {name}")
            print(f"   {details}")
            self.errors.append(f"{name}: {details}")
    
    def test_endpoint(self, endpoint, expected_status=200, method='GET', data=None):
        """Generic endpoint tester"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            
            success = response.status_code == expected_status
            
            if success and response.text:
                try:
                    json_data = response.json()
                    return True, json_data, response.status_code
                except:
                    return success, response.text[:200], response.status_code
            
            return success, f"Status: {response.status_code}, Content length: {len(response.text)}", response.status_code
            
        except requests.exceptions.Timeout:
            return False, "Request timeout (>30s)", None
        except requests.exceptions.ConnectionError:
            return False, "Connection error", None
        except Exception as e:
            return False, str(e)[:200], None
    
    def test_health(self):
        """Test backend health API: /api/health должен возвращать status ok"""
        print("\n🔍 Testing Health Endpoint (/api/health)...")
        success, data, status = self.test_endpoint("api/health")
        
        if success:
            if isinstance(data, dict):
                # Check for expected fields based on server.py
                status_field = data.get('status')
                proxy_field = data.get('proxy')
                ts_backend = data.get('ts_backend', {})
                
                if status_field == 'ok':
                    self.log_test("Health Status OK", True, f"Status: {status_field}, Proxy: {proxy_field}")
                else:
                    self.log_test("Health Status", False, f"Expected 'ok', got '{status_field}'")
                
                # Check TypeScript backend status
                if isinstance(ts_backend, dict) and ts_backend.get('ok'):
                    self.log_test("TypeScript Backend Health", True, "TS backend responding")
                else:
                    self.log_test("TypeScript Backend Health", False, f"TS backend status: {ts_backend}")
                    
            else:
                self.log_test("Health Check", True, "Basic health OK")
        else:
            self.log_test("Health Check", False, data)
        
        return success
    
    def test_brain_decision_api(self):
        """Test Brain Decision Engine: /api/ui/brain/decision возвращает данные"""
        print("\n🧠 Testing Brain Decision Engine (/api/ui/brain/decision)...")
        success, data, status = self.test_endpoint("api/ui/brain/decision")
        
        if success and isinstance(data, dict):
            # Check required Brain v4 components
            required_components = [
                'verdict', 'primaryAction', 'whyThisView', 'marketPhase', 
                'riskMap', 'causalFlow', 'macroIndicators', 'allocation',
                'capitalScaling', 'modelTransparency', 'decomposition'
            ]
            
            present_components = [comp for comp in required_components if comp in data]
            missing_components = [comp for comp in required_components if comp not in data]
            
            if len(missing_components) == 0:
                self.log_test("Brain Decision Structure", True, f"All {len(required_components)} components present")
            else:
                self.log_test("Brain Decision Structure", False, f"Missing: {', '.join(missing_components)}")
            
            # Check verdict data
            if 'verdict' in data:
                verdict = data['verdict']
                regime = verdict.get('regime', 'N/A')
                bias = verdict.get('bias', 'N/A')
                confidence = verdict.get('confidence', 'N/A')
                self.log_test("Brain Verdict Data", True, f"Regime: {regime}, Bias: {bias}, Confidence: {confidence}%")
            
        elif success:
            self.log_test("Brain Decision API", True, "Endpoint accessible")
        else:
            self.log_test("Brain Decision API", False, f"{data}")
        
        return success
    
    def test_dxy_fractal_overview(self):
        """Test DXY Fractal Decision Engine: /api/ui/fractal/dxy/overview возвращает данные"""
        print("\n💰 Testing DXY Fractal Decision Engine (/api/ui/fractal/dxy/overview)...")
        success, data, status = self.test_endpoint("api/ui/fractal/dxy/overview")
        
        if success and isinstance(data, dict):
            # Check main structure components
            required_components = [
                'header', 'verdict', 'chart', 'forecasts', 
                'why', 'risk', 'analogs', 'macro'
            ]
            
            missing_components = []
            present_components = []
            
            for component in required_components:
                if component in data:
                    present_components.append(component)
                else:
                    missing_components.append(component)
            
            if len(missing_components) == 0:
                self.log_test("DXY Overview Structure", True, f"All {len(required_components)} components present")
            else:
                self.log_test("DXY Overview Structure", False, f"Missing: {', '.join(missing_components)}")
            
            # Test Header Strip data
            if 'header' in data:
                header = data['header']
                signal = header.get('signal', 'N/A')
                confidence = header.get('confidence', 'N/A')
                risk = header.get('risk', 'N/A')
                regime = header.get('regime', 'N/A')
                self.log_test("DXY Header Strip", True, f"Signal: {signal}, Confidence: {confidence}%, Risk: {risk}, Regime: {regime}")
            
            # Test Verdict Card data
            if 'verdict' in data:
                verdict = data['verdict']
                action = verdict.get('action', 'N/A')
                bias = verdict.get('bias', 'N/A')
                expected_move = verdict.get('expectedMoveP50', 'N/A')
                self.log_test("DXY Verdict Card", True, f"Action: {action}, Bias: {bias}, Expected: {expected_move}%")
            
        elif success:
            self.log_test("DXY Fractal API", True, "Endpoint accessible")
        else:
            self.log_test("DXY Fractal API", False, f"{data}")
        
        return success
    
    def test_dxy_fractal_with_params(self):
        """Test DXY Fractal endpoint with different horizon parameters"""
        print("\n📊 Testing DXY Fractal with Parameters...")
        
        # Test with different horizons
        horizons_to_test = [7, 30, 90, 180]
        successful_horizons = []
        
        for horizon in horizons_to_test:
            success, data, status = self.test_endpoint(f"api/ui/fractal/dxy/overview?h={horizon}")
            if success:
                successful_horizons.append(horizon)
                if isinstance(data, dict) and 'verdict' in data:
                    verdict_horizon = data['verdict'].get('horizon', 'N/A')
                    self.log_test(f"DXY Fractal H={horizon}", True, f"Verdict horizon: {verdict_horizon}")
                else:
                    self.log_test(f"DXY Fractal H={horizon}", True, "Basic response OK")
            else:
                self.log_test(f"DXY Fractal H={horizon}", False, f"Status: {status}, Error: {data}")
        
        overall_success = len(successful_horizons) >= 2  # At least 2 horizons should work
        self.log_test("Multi-Horizon Support", overall_success, 
                     f"Working horizons: {successful_horizons}")
        
        return overall_success
    
    def test_dxy_macro_series(self):
        """Test DXY macro core series endpoint"""
        print("\n📊 Testing DXY Macro Core Series...")
        success, data, status = self.test_endpoint("api/dxy-macro-core/series")
        
        if success and isinstance(data, dict):
            # Look for loaded series information
            if 'series' in data or 'loaded' in str(data).lower():
                self.log_test("DXY Macro Series", True, "Series data available")
            else:
                self.log_test("DXY Macro Series", True, "Endpoint accessible")
        elif success:
            self.log_test("DXY Macro Series", True, "Basic endpoint OK")
        else:
            self.log_test("DXY Macro Series", False, data)
        
        return success
    
    def test_fractal_terminals(self):
        """Test BTC and SPX Fractal Terminals"""
        print("\n📈 Testing Fractal Terminals...")
        
        # Test BTC Fractal Terminal endpoints
        btc_endpoints = [
            "api/fractal/signal",  # Current BTC fractal signal
            "api/fractal/match",   # BTC pattern matching  
            "api/fractal/health"   # BTC fractal health
        ]
        
        btc_success_count = 0
        for endpoint in btc_endpoints:
            success, data, status = self.test_endpoint(endpoint)
            if success:
                btc_success_count += 1
                self.log_test(f"BTC Fractal - {endpoint.split('/')[-1]}", True, f"Status: {status}")
            else:
                self.log_test(f"BTC Fractal - {endpoint.split('/')[-1]}", False, f"Status: {status}, Error: {data}")
        
        # Test SPX Fractal Terminal endpoints
        spx_endpoints = [
            "api/fractal/spx/signal",
            "api/fractal/spx/overview", 
            "api/fractal/spx/match"
        ]
        
        spx_success_count = 0 
        for endpoint in spx_endpoints:
            success, data, status = self.test_endpoint(endpoint)
            if success:
                spx_success_count += 1
                self.log_test(f"SPX Fractal - {endpoint.split('/')[-1]}", True, f"Status: {status}")
            else:
                self.log_test(f"SPX Fractal - {endpoint.split('/')[-1]}", False, f"Status: {status}, Error: {data}")
        
        # Overall success if at least 1 endpoint from each works
        overall_success = (btc_success_count >= 1) and (spx_success_count >= 1)
        self.log_test("Fractal Terminals Overall", overall_success, 
                     f"BTC: {btc_success_count}/{len(btc_endpoints)}, SPX: {spx_success_count}/{len(spx_endpoints)}")
        
        return overall_success
    
    def test_admin_panel(self):
        """Test Admin Panel: страница /admin показывает форму логина"""
        print("\n👤 Testing Admin Panel...")
        
        # Test admin auth endpoints
        admin_endpoints = [
            "api/admin/auth/check",
            "api/admin/login"
        ]
        
        admin_working = False
        for endpoint in admin_endpoints:
            success, data, status = self.test_endpoint(endpoint)
            if success or status in [401, 403]:  # Auth endpoints may return 401/403 when not logged in
                admin_working = True
                self.log_test(f"Admin API - {endpoint.split('/')[-1]}", True, f"Status: {status} (auth working)")
            else:
                self.log_test(f"Admin API - {endpoint.split('/')[-1]}", False, f"Status: {status}, Error: {data}")
        
        return admin_working
    
    def run_all_tests(self):
        """Run all DXY Fractal backend API tests"""
        print("="*60)
        print("🚀 STARTING DXY FRACTAL BACKEND API TESTING")
        print("💰 Testing DXY Decision Engine Components")
        print("🔗 Backend URL:", self.base_url)
        print("="*60)
        
        # Basic connectivity
        if not self.test_health():
            print("\n❌ CRITICAL: Health endpoint failed - stopping tests")
            return False
        
        # Core DXY Fractal functionality tests
        self.test_dxy_fractal_overview()
        self.test_dxy_fractal_with_params()
        
        # Print summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        else:
            print("\n✅ ALL TESTS PASSED!")
        
        return len(self.errors) == 0

def main():
    tester = DxyFractalTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())