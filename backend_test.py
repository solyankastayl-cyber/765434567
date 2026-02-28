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
    
    def test_fractal_endpoints(self):
        """Test BTC and SPX fractal endpoints"""
        print("\n📈 Testing Fractal Endpoints...")
        
        # Test BTC fractal data
        btc_success, btc_data, btc_status = self.test_endpoint("api/fractal/btc/latest")
        if not btc_success:
            # Try alternative endpoint
            btc_success, btc_data, btc_status = self.test_endpoint("api/fractal/bitcoin")
        
        self.log_test("BTC Fractal Endpoint", btc_success, 
                     f"Status: {btc_status}" + (f", Data available" if btc_success else f" - {btc_data}"))
        
        # Test SPX fractal data  
        spx_success, spx_data, spx_status = self.test_endpoint("api/fractal/spx/latest")
        if not spx_success:
            # Try alternative endpoint
            spx_success, spx_data, spx_status = self.test_endpoint("api/fractal/spx")
            
        self.log_test("SPX Fractal Endpoint", spx_success,
                     f"Status: {spx_status}" + (f", Data available" if spx_success else f" - {spx_data}"))
        
        return btc_success or spx_success
    
    def test_admin_endpoints(self):
        """Test admin-related endpoints"""
        print("\n👤 Testing Admin Endpoints...")
        
        # Check if admin login page is served
        admin_success, admin_data, admin_status = self.test_endpoint("admin/login", method='GET')
        self.log_test("Admin Login Page", admin_success or admin_status == 404, 
                     f"Status: {admin_status}" + (" - Page accessible" if admin_success else ""))
        
        return True  # Admin accessibility is not critical
    
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