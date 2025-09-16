"""
Performance Benchmark for Hotel Booking Platform
Tests system performance under various load conditions
"""

import asyncio
import aiohttp
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
import json

API_BASE_URL = "http://localhost:8000"

class PerformanceBenchmark:
    def __init__(self):
        self.results = {}
    
    async def benchmark_search_latency(self, concurrent_requests=10, total_requests=100):
        """Benchmark search API latency"""
        print(f"🔍 Benchmarking search latency ({concurrent_requests} concurrent, {total_requests} total)")
        
        search_queries = [
            {"city": "Mumbai"},
            {"city": "Delhi"},
            {"city": "Bangalore"},
            {"hotel_name": "Grand"},
            {"hotel_name": "Royal"},
            {"city": "Chennai", "hotel_name": "Palace"}
        ]
        
        async def make_search_request(session, query):
            start_time = time.time()
            try:
                async with session.post(f"{API_BASE_URL}/api/search", json=query) as response:
                    await response.json()
                    return (time.time() - start_time) * 1000  # Convert to ms
            except Exception as e:
                print(f"Request failed: {e}")
                return None
        
        # Run concurrent requests
        latencies = []
        semaphore = asyncio.Semaphore(concurrent_requests)
        
        async def bounded_request(session, query):
            async with semaphore:
                return await make_search_request(session, query)
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(total_requests):
                query = search_queries[i % len(search_queries)]
                tasks.append(bounded_request(session, query))
            
            results = await asyncio.gather(*tasks)
            latencies = [r for r in results if r is not None]
        
        if latencies:
            avg_latency = statistics.mean(latencies)
            median_latency = statistics.median(latencies)
            p95_latency = sorted(latencies)[int(0.95 * len(latencies))]
            min_latency = min(latencies)
            max_latency = max(latencies)
            
            self.results['search_latency'] = {
                'avg_ms': round(avg_latency, 2),
                'median_ms': round(median_latency, 2),
                'p95_ms': round(p95_latency, 2),
                'min_ms': round(min_latency, 2),
                'max_ms': round(max_latency, 2),
                'total_requests': len(latencies),
                'failed_requests': total_requests - len(latencies)
            }
            
            print(f"  Average: {avg_latency:.2f}ms")
            print(f"  Median: {median_latency:.2f}ms") 
            print(f"  95th percentile: {p95_latency:.2f}ms")
            print(f"  Min: {min_latency:.2f}ms, Max: {max_latency:.2f}ms")
            print(f"  Success rate: {len(latencies)}/{total_requests} ({len(latencies)/total_requests*100:.1f}%)")
        else:
            print("  ❌ All requests failed")
    
    async def benchmark_booking_throughput(self, concurrent_bookings=5):
        """Benchmark booking creation throughput"""
        print(f"📝 Benchmarking booking throughput ({concurrent_bookings} concurrent)")
        
        # First get available rooms
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_BASE_URL}/api/search", 
                                  json={"city": "Mumbai", "limit": 10}) as response:
                hotels = await response.json()
        
        if not hotels or not any(hotel.get("rooms") for hotel in hotels):
            print("  ❌ No rooms available for booking test")
            return
        
        # Get rooms for testing
        available_rooms = []
        for hotel in hotels:
            for room in hotel.get("rooms", []):
                if room.get("is_available"):
                    available_rooms.append(room["id"])
                    if len(available_rooms) >= concurrent_bookings:
                        break
            if len(available_rooms) >= concurrent_bookings:
                break
        
        if len(available_rooms) < concurrent_bookings:
            print(f"  ⚠️  Only {len(available_rooms)} rooms available, reducing concurrent bookings")
            concurrent_bookings = len(available_rooms)
        
        # Create booking requests
        from datetime import date, timedelta
        
        async def make_booking_request(session, room_id, guest_num):
            booking_data = {
                "room_id": room_id,
                "guest_name": f"Benchmark Guest {guest_num}",
                "guest_email": f"benchmark{guest_num}@test.com",
                "check_in_date": (date.today() + timedelta(days=guest_num)).isoformat(),
                "check_out_date": (date.today() + timedelta(days=guest_num + 2)).isoformat()
            }
            
            start_time = time.time()
            try:
                async with session.post(f"{API_BASE_URL}/api/bookings", json=booking_data) as response:
                    result = await response.json()
                    latency = (time.time() - start_time) * 1000
                    return response.status == 200, latency
            except Exception as e:
                return False, (time.time() - start_time) * 1000
        
        # Execute concurrent bookings
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [
                make_booking_request(session, available_rooms[i], i+1) 
                for i in range(concurrent_bookings)
            ]
            results = await asyncio.gather(*tasks)
        
        total_time = (time.time() - start_time) * 1000
        
        successful_bookings = sum(1 for success, _ in results if success)
        booking_latencies = [latency for success, latency in results if success]
        
        if booking_latencies:
            avg_booking_latency = statistics.mean(booking_latencies)
            throughput = (successful_bookings / total_time) * 1000  # bookings per second
            
            self.results['booking_throughput'] = {
                'successful_bookings': successful_bookings,
                'total_bookings': concurrent_bookings,
                'success_rate': successful_bookings / concurrent_bookings * 100,
                'avg_latency_ms': round(avg_booking_latency, 2),
                'total_time_ms': round(total_time, 2),
                'throughput_per_sec': round(throughput, 2)
            }
            
            print(f"  Successful bookings: {successful_bookings}/{concurrent_bookings}")
            print(f"  Average latency: {avg_booking_latency:.2f}ms")
            print(f"  Total time: {total_time:.2f}ms")
            print(f"  Throughput: {throughput:.2f} bookings/second")
        else:
            print("  ❌ All booking requests failed")
    
    async def benchmark_large_dataset_search(self):
        """Benchmark search performance on large dataset"""
        print("🗄️  Benchmarking large dataset search performance")
        
        async with aiohttp.ClientSession() as session:
            # Test the performance endpoint multiple times
            latencies = []
            for i in range(10):
                start_time = time.time()
                try:
                    async with session.get(f"{API_BASE_URL}/api/performance/search") as response:
                        result = await response.json()
                        latency = (time.time() - start_time) * 1000
                        latencies.append(latency)
                        
                        if i == 0:  # Print details on first run
                            print(f"  Dataset size: {result.get('total_hotels_in_db', 0):,} hotels")
                            print(f"  Results found: {result.get('results_count', 0)}")
                except Exception as e:
                    print(f"  Request {i+1} failed: {e}")
            
            if latencies:
                avg_latency = statistics.mean(latencies)
                min_latency = min(latencies)
                max_latency = max(latencies)
                
                self.results['large_dataset_search'] = {
                    'avg_latency_ms': round(avg_latency, 2),
                    'min_latency_ms': round(min_latency, 2),
                    'max_latency_ms': round(max_latency, 2),
                    'test_runs': len(latencies)
                }
                
                print(f"  Average search time: {avg_latency:.2f}ms")
                print(f"  Min: {min_latency:.2f}ms, Max: {max_latency:.2f}ms")
                
                # Performance evaluation
                if avg_latency < 100:
                    print("  🚀 Excellent performance!")
                elif avg_latency < 500:
                    print("  ✅ Good performance")
                else:
                    print("  ⚠️  Performance could be improved")
    
    def print_summary(self):
        """Print benchmark summary"""
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE BENCHMARK SUMMARY")
        print("=" * 60)
        
        if 'search_latency' in self.results:
            print("\n🔍 Search Latency:")
            r = self.results['search_latency']
            print(f"  Average: {r['avg_ms']}ms")
            print(f"  95th percentile: {r['p95_ms']}ms")
            print(f"  Success rate: {r['total_requests'] - r['failed_requests']}/{r['total_requests']}")
        
        if 'booking_throughput' in self.results:
            print("\n📝 Booking Throughput:")
            r = self.results['booking_throughput']
            print(f"  Success rate: {r['success_rate']:.1f}%")
            print(f"  Throughput: {r['throughput_per_sec']} bookings/second")
            print(f"  Average latency: {r['avg_latency_ms']}ms")
        
        if 'large_dataset_search' in self.results:
            print("\n🗄️  Large Dataset Search:")
            r = self.results['large_dataset_search']
            print(f"  Average latency: {r['avg_latency_ms']}ms")
            print(f"  Range: {r['min_latency_ms']}ms - {r['max_latency_ms']}ms")
        
        print("\n🎯 Benchmark completed!")

async def main():
    """Run performance benchmarks"""
    print("🚀 Starting Performance Benchmark Suite")
    print("=" * 60)
    
    benchmark = PerformanceBenchmark()
    
    # Run benchmarks
    await benchmark.benchmark_search_latency(concurrent_requests=10, total_requests=50)
    print()
    await benchmark.benchmark_booking_throughput(concurrent_bookings=5)
    print()
    await benchmark.benchmark_large_dataset_search()
    
    # Print summary
    benchmark.print_summary()

if __name__ == "__main__":
    # Check backend availability
    try:
        import requests
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend is not responding correctly")
            exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Please start the backend server first:")
        print("  cd backend && python main.py")
        exit(1)
    
    asyncio.run(main())
