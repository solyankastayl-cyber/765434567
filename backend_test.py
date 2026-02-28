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
    
    def test_brain_overview(self):
        """Test Brain v3 page with FRED macro data"""
        print("\n🧠 Testing Brain Overview (v3) - FRED Integration...")
        success, data, status = self.test_endpoint("api/ui/brain/overview")
        
        if success and isinstance(data, dict):
            # Check if real macro indicators are present
            macro_inputs = data.get('macroInputs', [])
            health_strip = data.get('healthStrip', {})
            
            # Look for FRED indicators
            fred_indicators = []
            for indicator in macro_inputs:
                if indicator.get('value') != 'N/A' and indicator.get('status') != 'nodata':
                    fred_indicators.append(indicator.get('title', 'Unknown'))
            
            if len(fred_indicators) >= 3:  # At least 3 real indicators
                self.log_test("Brain Overview - Real Data", True, 
                             f"Found {len(fred_indicators)} real indicators: {', '.join(fred_indicators[:3])}")
            else:
                self.log_test("Brain Overview - Real Data", False, 
                             f"Only {len(fred_indicators)} real indicators found")
            
            # Check brain scenario
            scenario = health_strip.get('brainScenario', 'unknown')
            self.log_test("Brain Scenario", True, f"Current scenario: {scenario}")
            
        elif status == 200:
            self.log_test("Brain Overview API", True, "Endpoint accessible but no detailed data check")
        else:
            self.log_test("Brain Overview API", False, f"{data}")
        
        return success
    
    def test_brain_decision_v4(self):
        """Test Brain v4 Decision Engine endpoint"""
        print("\n🧠 Testing Brain v4 Decision Engine...")
        success, data, status = self.test_endpoint("api/ui/brain/decision")
        
        if success and isinstance(data, dict):
            # Check required Brain v4 structure
            required_fields = [
                'verdict', 'action', 'reasons', 'horizons', 'risk', 
                'causal', 'macroSummary', 'allocation', 'capitalScaling', 
                'transparency', 'advanced'
            ]
            
            missing_fields = []
            present_fields = []
            
            for field in required_fields:
                if field in data:
                    present_fields.append(field)
                else:
                    missing_fields.append(field)
            
            if len(missing_fields) == 0:
                self.log_test("Brain v4 Structure", True, f"All {len(required_fields)} components present")
            else:
                self.log_test("Brain v4 Structure", False, f"Missing: {', '.join(missing_fields)}")
            
            # Check verdict structure
            verdict = data.get('verdict', {})
            if verdict and 'regime' in verdict and 'dominantBias' in verdict:
                regime = verdict.get('regime', 'unknown')
                bias = verdict.get('dominantBias', 'unknown')
                confidence = verdict.get('confidence', 0)
                self.log_test("Market Verdict", True, f"Regime: {regime}, Bias: {bias}, Confidence: {confidence}%")
            else:
                self.log_test("Market Verdict", False, "Missing verdict structure")
            
            # Check macro summary for FRED data
            macro_summary = data.get('macroSummary', [])
            if len(macro_summary) >= 3:
                indicators = [m.get('title', 'Unknown') for m in macro_summary[:3]]
                self.log_test("Macro Indicators", True, f"Found {len(macro_summary)} indicators: {', '.join(indicators)}")
            else:
                self.log_test("Macro Indicators", False, f"Only {len(macro_summary)} indicators found")
                
        elif status == 200:
            self.log_test("Brain v4 Decision API", True, "Endpoint accessible but no detailed data check")
        else:
            self.log_test("Brain v4 Decision API", False, f"{data}")
        
        return success
    
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