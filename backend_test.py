import requests
import sys
import json
from datetime import datetime

class AkumaFinderAPITester:
    def __init__(self, base_url="https://devil-fruit-db.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        print(f"   Response: List with {len(response_data)} items")
                    elif isinstance(response_data, dict):
                        print(f"   Response keys: {list(response_data.keys())}")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                self.failed_tests.append({
                    'name': name,
                    'expected': expected_status,
                    'actual': response.status_code,
                    'response': response.text[:200]
                })

            return success, response.json() if success and response.text else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                'name': name,
                'error': str(e)
            })
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_init_database(self):
        """Test database initialization"""
        return self.run_test("Initialize Database", "POST", "init-database", 200)

    def test_get_all_fruits(self):
        """Test getting all fruits"""
        return self.run_test("Get All Fruits", "GET", "fruits", 200)

    def test_get_fruits_with_filters(self):
        """Test fruits with various filters"""
        # Test type filter
        success1, _ = self.run_test("Get Logia Fruits", "GET", "fruits", 200, params={"type": "Logia"})
        
        # Test rarity filter
        success2, _ = self.run_test("Get Mythical Fruits", "GET", "fruits", 200, params={"rarity": "Mítica"})
        
        # Test availability filter
        success3, _ = self.run_test("Get Available Fruits", "GET", "fruits", 200, params={"available": True})
        
        # Test sorting
        success4, _ = self.run_test("Get Fruits Sorted by Price", "GET", "fruits", 200, params={"sort_by": "price_desc"})
        
        return all([success1, success2, success3, success4])

    def test_get_fruit_by_id(self):
        """Test getting specific fruit by ID"""
        # First get all fruits to get a valid ID
        success, fruits_data = self.test_get_all_fruits()
        if success and fruits_data and len(fruits_data) > 0:
            fruit_id = fruits_data[0]['id']
            return self.run_test(f"Get Fruit by ID ({fruit_id})", "GET", f"fruits/{fruit_id}", 200)
        else:
            print("❌ Cannot test fruit by ID - no fruits available")
            return False

    def test_search_fruits(self):
        """Test fruit search functionality"""
        # Test basic search
        success1, _ = self.run_test("Search by Description", "POST", "search", 200, 
                                   data={"description": "fogo"})
        
        # Test search with budget
        success2, _ = self.run_test("Search with Budget", "POST", "search", 200, 
                                   data={"budget": 1000000000, "description": "poder"})
        
        # Test search with type
        success3, _ = self.run_test("Search by Type", "POST", "search", 200, 
                                   data={"fruit_type": "Logia"})
        
        # Test search with rarity
        success4, _ = self.run_test("Search by Rarity", "POST", "search", 200, 
                                   data={"rarity": "Mítica"})
        
        # Test search with fighting style
        success5, _ = self.run_test("Search by Fighting Style", "POST", "search", 200, 
                                   data={"fighting_style": "Luta de longe"})
        
        return all([success1, success2, success3, success4, success5])

    def test_rankings(self):
        """Test all ranking endpoints"""
        rankings = [
            ("Most Expensive", "rankings/expensive"),
            ("Most Destructive", "rankings/destructive"),
            ("Most Rare", "rankings/rare"),
            ("Best Defense", "rankings/defense"),
            ("Best Speed", "rankings/speed")
        ]
        
        results = []
        for name, endpoint in rankings:
            success, _ = self.run_test(name, "GET", endpoint, 200)
            results.append(success)
        
        return all(results)

    def test_black_market(self):
        """Test black market endpoint"""
        return self.run_test("Black Market", "GET", "black-market", 200)

    def test_invalid_endpoints(self):
        """Test error handling for invalid endpoints"""
        # Test non-existent fruit ID
        success1, _ = self.run_test("Invalid Fruit ID", "GET", "fruits/invalid-id", 404)
        
        return success1

def main():
    print("🏴‍☠️ Starting Akuma Finder API Tests...")
    print("=" * 60)
    
    tester = AkumaFinderAPITester()
    
    # Run all tests
    print("\n📡 Testing API Connectivity...")
    tester.test_root_endpoint()
    
    print("\n🗄️ Testing Database...")
    tester.test_init_database()
    
    print("\n🍎 Testing Fruit Endpoints...")
    tester.test_get_all_fruits()
    tester.test_get_fruits_with_filters()
    tester.test_get_fruit_by_id()
    
    print("\n🔍 Testing Search...")
    tester.test_search_fruits()
    
    print("\n🏆 Testing Rankings...")
    tester.test_rankings()
    
    print("\n💰 Testing Black Market...")
    tester.test_black_market()
    
    print("\n❌ Testing Error Handling...")
    tester.test_invalid_endpoints()
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.failed_tests:
        print(f"\n❌ Failed Tests ({len(tester.failed_tests)}):")
        for i, test in enumerate(tester.failed_tests, 1):
            print(f"   {i}. {test['name']}")
            if 'error' in test:
                print(f"      Error: {test['error']}")
            else:
                print(f"      Expected: {test['expected']}, Got: {test['actual']}")
    
    success_rate = (tester.tests_passed / tester.tests_run) * 100 if tester.tests_run > 0 else 0
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())