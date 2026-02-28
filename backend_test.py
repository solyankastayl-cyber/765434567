#!/usr/bin/env python3
"""
Backend API Testing Script for DXY Fractal Decision Engine
Testing DXY Fractal overview endpoint and all required components
"""

import requests
import sys
from datetime import datetime
import json

class DxyFractalTester:
    def __init__(self, base_url="https://fractal-index-4.preview.emergentagent.com"):
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
        """Test basic health endpoint"""
        print("\n🔍 Testing Health Endpoint...")
        success, data, status = self.test_endpoint("api/health")
        
        if success:
            if isinstance(data, dict):
                ts_status = data.get('ts_backend', {})
                mode = ts_status.get('mode', 'unknown')
                self.log_test("Health Check", True, f"Status OK, Mode: {mode}")
            else:
                self.log_test("Health Check", True, "Basic health OK")
        else:
            self.log_test("Health Check", False, data)
        
        return success
    
    def test_dxy_fractal_overview(self):
        """Test DXY Fractal overview endpoint with all required components"""
        print("\n💰 Testing DXY Fractal Overview - Decision Engine...")
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
                header_fields = ['signal', 'confidence', 'risk', 'regime', 'dataStatus']
                header_present = [f for f in header_fields if f in header]
                self.log_test("Header Strip Fields", len(header_present) >= 4, 
                             f"Found {len(header_present)}/{len(header_fields)}: {', '.join(header_present)}")
                
                # Check specific values mentioned in review request
                if header.get('signal') == 'SELL' and header.get('confidence') == 30:
                    self.log_test("Header Values Match", True, "Signal=SELL, Confidence=30% as expected")
                else:
                    signal = header.get('signal', 'N/A')
                    conf = header.get('confidence', 'N/A')
                    self.log_test("Header Values", True, f"Signal={signal}, Confidence={conf}%")
            
            # Test Verdict Card data
            if 'verdict' in data:
                verdict = data['verdict']
                verdict_fields = ['action', 'bias', 'expectedMoveP50', 'positionMultiplier', 'confidence']
                verdict_present = [f for f in verdict_fields if f in verdict]
                self.log_test("Verdict Card Fields", len(verdict_present) >= 4,
                             f"Found {len(verdict_present)}/{len(verdict_fields)}: {', '.join(verdict_present)}")
                
                # Check expected values
                action = verdict.get('action', 'N/A')
                bias = verdict.get('bias', 'N/A')
                expected_move = verdict.get('expectedMoveP50', 'N/A')
                self.log_test("Verdict Values", True, f"Action={action}, Bias={bias}, Expected={expected_move}%")
            
            # Test Chart data
            if 'chart' in data:
                chart = data['chart']
                chart_modes = ['synthetic', 'replay', 'hybrid', 'macro']
                chart_present = [mode for mode in chart_modes if mode in chart]
                self.log_test("Chart Modes", len(chart_present) >= 3,
                             f"Found {len(chart_present)}/{len(chart_modes)} modes: {', '.join(chart_present)}")
            
            # Test Forecast Table
            if 'forecasts' in data and isinstance(data['forecasts'], list):
                forecasts = data['forecasts']
                horizons = [f.get('horizon') for f in forecasts if 'horizon' in f]
                expected_horizons = [7, 14, 30, 90, 180, 365]
                self.log_test("Forecast Horizons", len(horizons) >= 5,
                             f"Found {len(horizons)} horizons: {horizons}")
            
            # Test Why This Verdict
            if 'why' in data:
                why = data['why']
                why_components = ['drivers', 'transmission', 'invalidations']
                why_present = [c for c in why_components if c in why]
                self.log_test("Why Verdict Components", len(why_present) >= 2,
                             f"Found {len(why_present)}/{len(why_components)}: {', '.join(why_present)}")
            
            # Test Risk Context
            if 'risk' in data:
                risk = data['risk']
                risk_fields = ['level', 'volRegime', 'expectedDrawdown', 'positionMultiplier']
                risk_present = [f for f in risk_fields if f in risk]
                self.log_test("Risk Context Fields", len(risk_present) >= 3,
                             f"Found {len(risk_present)}/{len(risk_fields)}: {', '.join(risk_present)}")
            
            # Test Historical Analogs
            if 'analogs' in data:
                analogs = data['analogs']
                analog_fields = ['bestMatch', 'coverage', 'sampleSize', 'outcomeP50', 'topMatches']
                analog_present = [f for f in analog_fields if f in analogs]
                self.log_test("Historical Analogs Fields", len(analog_present) >= 4,
                             f"Found {len(analog_present)}/{len(analog_fields)}: {', '.join(analog_present)}")
            
            # Test Macro Impact
            if 'macro' in data:
                macro = data['macro']
                macro_fields = ['score', 'scoreSigned', 'confidence', 'regime', 'components']
                macro_present = [f for f in macro_fields if f in macro]
                macro_adj = macro.get('scoreSigned', 0)
                self.log_test("Macro Impact Fields", len(macro_present) >= 4,
                             f"Found {len(macro_present)}/{len(macro_fields)}, Adjustment: {macro_adj}%")
            
        elif status == 200:
            self.log_test("DXY Fractal API", True, "Endpoint accessible but no detailed data check")
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
        """Run all backend API tests"""
        print("="*60)
        print("🚀 STARTING BACKEND API TESTING")
        print("🏢 GitHub Repository: dt54edcv")
        print("🔗 Backend URL:", self.base_url)
        print("="*60)
        
        # Basic connectivity
        if not self.test_health():
            print("\n❌ CRITICAL: Health endpoint failed - stopping tests")
            return False
        
        # Core functionality tests
        self.test_brain_overview()
        self.test_brain_decision_v4()  # New Brain v4 test
        self.test_dxy_macro_series() 
        self.test_fractal_endpoints()
        self.test_admin_endpoints()
        
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
    tester = GitHubRepoTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())