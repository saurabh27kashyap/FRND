"""
Test Cases for Hotel Room Booking Platform
Tests simultaneous booking scenarios and prevents double booking
"""

import asyncio
import aiohttp
import json
import time
import threading
from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor
import sys

# Test configuration
API_BASE_URL = "http://localhost:8000"
TEST_RESULTS = []

class TestResult:
    def __init__(self, test_name: str, passed: bool, message: str, execution_time: float = 0):
        self.test_name = test_name
        self.passed = passed
        self.message = message
        self.execution_time = execution_time

def log_result(result: TestResult):
    """Log test result"""
    status = "✅ PASS" if result.passed else "❌ FAIL"
    print(f"{status} {result.test_name} ({result.execution_time:.2f}ms)")
    print(f"   {result.message}")
    TEST_RESULTS.append(result)

async def make_request(session, method: str, endpoint: str, data=None):
    """Make HTTP request with error handling"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method.upper() == "POST":
            async with session.post(url, json=data) as response:
                return response.status, await response.json()
        elif method.upper() == "GET":
            async with session.get(url) as response:
                return response.status, await response.json()
        elif method.upper() == "DELETE":
            async with session.delete(url) as response:
                return response.status, await response.json()
    except Exception as e:
        return 500, {"detail": str(e)}

async def test_health_check():
    """Test 1: Health Check"""
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        status, response = await make_request(session, "GET", "/health")
        
    execution_time = (time.time() - start_time) * 1000
    
    if status == 200 and response.get("status") == "healthy":
        log_result(TestResult("Health Check", True, "API is healthy and responsive", execution_time))
    else:
        log_result(TestResult("Health Check", False, f"API health check failed: {response}", execution_time))

async def test_hotel_creation_and_search():
    """Test 2: Hotel Creation and Search"""
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Create a test hotel
        hotel_data = {
            "name": "Test Hotel Mumbai",
            "city": "Mumbai",
            "address": "Test Address, Mumbai",
            "star_rating": 4,
            "description": "A test hotel for automated testing",
            "amenities": ["WiFi", "Pool", "Gym"],
            "rooms": [
                {
                    "room_number": "101",
                    "room_type": "Single",
                    "price": 5000,
                    "max_occupancy": 2,
                    "amenities": ["AC", "TV"],
                    "is_available": True
                }
            ]
        }
        
        create_status, create_response = await make_request(session, "POST", "/api/hotels", hotel_data)
        
        if create_status != 200:
            execution_time = (time.time() - start_time) * 1000
            log_result(TestResult("Hotel Creation", False, f"Failed to create hotel: {create_response}", execution_time))
            return None
        
        hotel_id = create_response["id"]
        
        # Test search by city
        search_data = {"city": "Mumbai", "limit": 10}
        search_status, search_response = await make_request(session, "POST", "/api/search", search_data)
        
        execution_time = (time.time() - start_time) * 1000
        
        if search_status == 200 and len(search_response) > 0:
            found_hotel = any(hotel["name"] == "Test Hotel Mumbai" for hotel in search_response)
            if found_hotel:
                log_result(TestResult("Hotel Search", True, f"Successfully created and found hotel in search results", execution_time))
                return hotel_id
            else:
                log_result(TestResult("Hotel Search", False, "Hotel not found in search results", execution_time))
        else:
            log_result(TestResult("Hotel Search", False, f"Search failed: {search_response}", execution_time))
    
    return None

async def test_simultaneous_booking():
    """Test 3: Simultaneous Booking Prevention"""
    start_time = time.time()
    
    # First, get a room to book
    async with aiohttp.ClientSession() as session:
        # Search for hotels to get a room
        search_data = {"city": "Mumbai", "limit": 1}
        search_status, search_response = await make_request(session, "POST", "/api/search", search_data)
        
        if search_status != 200 or not search_response:
            log_result(TestResult("Simultaneous Booking", False, "No hotels found for booking test", 0))
            return
        
        hotel = search_response[0]
        if not hotel["rooms"]:
            log_result(TestResult("Simultaneous Booking", False, "No rooms available for booking test", 0))
            return
        
        room = hotel["rooms"][0]
        room_id = room["id"]
        
        # Prepare booking data for overlapping dates
        tomorrow = date.today() + timedelta(days=1)
        day_after = date.today() + timedelta(days=3)
        
        booking_data_1 = {
            "room_id": room_id,
            "guest_name": "Test Guest 1",
            "guest_email": "guest1@test.com",
            "check_in_date": tomorrow.isoformat(),
            "check_out_date": day_after.isoformat()
        }
        
        booking_data_2 = {
            "room_id": room_id,
            "guest_name": "Test Guest 2", 
            "guest_email": "guest2@test.com",
            "check_in_date": (tomorrow + timedelta(days=1)).isoformat(),  # Overlapping dates
            "check_out_date": (day_after + timedelta(days=1)).isoformat()
        }
        
        # Create multiple sessions for simultaneous requests
        async def make_booking(session, booking_data, booking_num):
            return await make_request(session, "POST", "/api/bookings", booking_data)
        
        # Execute simultaneous bookings
        async with aiohttp.ClientSession() as session1, aiohttp.ClientSession() as session2:
            results = await asyncio.gather(
                make_booking(session1, booking_data_1, 1),
                make_booking(session2, booking_data_2, 2),
                return_exceptions=True
            )
        
        execution_time = (time.time() - start_time) * 1000
        
        # Analyze results
        successful_bookings = sum(1 for status, _ in results if status == 200)
        failed_bookings = sum(1 for status, _ in results if status != 200)
        
        if successful_bookings == 1 and failed_bookings == 1:
            log_result(TestResult("Simultaneous Booking", True, 
                                f"Double booking prevented successfully. 1 booking succeeded, 1 failed as expected", 
                                execution_time))
        else:
            log_result(TestResult("Simultaneous Booking", False, 
                                f"Double booking prevention failed. {successful_bookings} succeeded, {failed_bookings} failed", 
                                execution_time))

async def test_booking_edge_cases():
    """Test 4: Booking Edge Cases"""
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Get a room for testing
        search_data = {"city": "Delhi", "limit": 1}
        search_status, search_response = await make_request(session, "POST", "/api/search", search_data)
        
        if search_status != 200 or not search_response or not search_response[0]["rooms"]:
            log_result(TestResult("Booking Edge Cases", False, "No rooms available for edge case testing", 0))
            return
        
        room_id = search_response[0]["rooms"][0]["id"]
        
        # Test Case 1: Same check-in and check-out date (should fail)
        same_date = date.today() + timedelta(days=1)
        invalid_booking = {
            "room_id": room_id,
            "guest_name": "Edge Case Guest",
            "guest_email": "edge@test.com",
            "check_in_date": same_date.isoformat(),
            "check_out_date": same_date.isoformat()
        }
        
        status1, response1 = await make_request(session, "POST", "/api/bookings", invalid_booking)
        
        # Test Case 2: Past date booking (should fail)
        past_date = date.today() - timedelta(days=1)
        past_booking = {
            "room_id": room_id,
            "guest_name": "Past Date Guest",
            "guest_email": "past@test.com",
            "check_in_date": past_date.isoformat(),
            "check_out_date": (past_date + timedelta(days=1)).isoformat()
        }
        
        status2, response2 = await make_request(session, "POST", "/api/bookings", past_booking)
        
        # Test Case 3: Valid booking (should succeed)
        valid_start = date.today() + timedelta(days=5)
        valid_end = date.today() + timedelta(days=7)
        valid_booking = {
            "room_id": room_id,
            "guest_name": "Valid Guest",
            "guest_email": "valid@test.com",
            "check_in_date": valid_start.isoformat(),
            "check_out_date": valid_end.isoformat()
        }
        
        status3, response3 = await make_request(session, "POST", "/api/bookings", valid_booking)
        
        execution_time = (time.time() - start_time) * 1000
        
        # Evaluate results
        edge_case_1_pass = status1 != 200  # Should fail
        edge_case_2_pass = status2 != 200  # Should fail  
        edge_case_3_pass = status3 == 200  # Should succeed
        
        if edge_case_1_pass and edge_case_2_pass and edge_case_3_pass:
            log_result(TestResult("Booking Edge Cases", True, 
                                "All edge cases handled correctly: same date rejected, past date rejected, valid booking accepted", 
                                execution_time))
        else:
            failures = []
            if not edge_case_1_pass: failures.append("same date booking allowed")
            if not edge_case_2_pass: failures.append("past date booking allowed")
            if not edge_case_3_pass: failures.append("valid booking rejected")
            
            log_result(TestResult("Booking Edge Cases", False, 
                                f"Edge case failures: {', '.join(failures)}", 
                                execution_time))

async def test_search_performance():
    """Test 5: Search Performance with Large Dataset"""
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Test performance endpoint
        perf_status, perf_response = await make_request(session, "GET", "/api/performance/search")
        
        execution_time = (time.time() - start_time) * 1000
        
        if perf_status == 200:
            db_size = perf_response.get("total_hotels_in_db", 0)
            search_time = perf_response.get("execution_time_ms", 0)
            results_count = perf_response.get("results_count", 0)
            
            # Performance criteria: search should complete in under 500ms for large datasets
            performance_acceptable = search_time < 500
            
            if performance_acceptable and db_size >= 1000:
                log_result(TestResult("Search Performance", True, 
                                    f"Search performed well: {search_time}ms for {db_size:,} hotels, found {results_count} results", 
                                    execution_time))
            elif db_size < 1000:
                log_result(TestResult("Search Performance", False, 
                                    f"Dataset too small for performance test: only {db_size} hotels", 
                                    execution_time))
            else:
                log_result(TestResult("Search Performance", False, 
                                    f"Search performance poor: {search_time}ms for {db_size:,} hotels", 
                                    execution_time))
        else:
            log_result(TestResult("Search Performance", False, 
                                f"Performance test endpoint failed: {perf_response}", 
                                execution_time))

async def run_all_tests():
    """Run all test cases"""
    print("🚀 Starting Hotel Booking Platform Test Suite")
    print("=" * 60)
    
    # Run tests in sequence
    await test_health_check()
    hotel_id = await test_hotel_creation_and_search()
    await test_simultaneous_booking()
    await test_booking_edge_cases()
    await test_search_performance()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total_tests = len(TEST_RESULTS)
    passed_tests = sum(1 for result in TEST_RESULTS if result.passed)
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests > 0:
        print("\n❌ FAILED TESTS:")
        for result in TEST_RESULTS:
            if not result.passed:
                print(f"  - {result.test_name}: {result.message}")
    
    print("\n🎯 Test Suite Completed!")
    return failed_tests == 0

if __name__ == "__main__":
    # Check if backend is running
    print("Checking if backend is running on http://localhost:8000...")
    
    try:
        import requests
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
        else:
            print("❌ Backend is not responding correctly")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Please start the backend server first:")
        print("  cd backend && python main.py")
        sys.exit(1)
    
    # Run async tests
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
