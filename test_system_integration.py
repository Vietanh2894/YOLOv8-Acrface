#!/usr/bin/env python3
"""
Test script cho toàn bộ Face Recognition System
Bao gồm: Python API, Java Spring Boot API, và Database
"""

import requests
import json
import base64
import time
import os
from pathlib import Path

class FaceRecognitionSystemTest:
    def __init__(self):
        self.python_api_url = "http://localhost:5000/api"
        self.java_api_url = "http://localhost:8080/api/v1/face"
        self.test_results = []
        
    def encode_image_to_base64(self, image_path):
        """Convert image to base64 string"""
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.getBytes()).decode('utf-8')
        return None
    
    def log_result(self, test_name, success, message, response_time=None):
        """Log test result"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'response_time': response_time
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        time_info = f" ({response_time:.3f}s)" if response_time else ""
        print(f"{status} {test_name}{time_info}: {message}")
    
    def test_python_api_health(self):
        """Test Python API health check"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.python_api_url}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK':
                    self.log_result("Python API Health Check", True, "API is healthy", response_time)
                else:
                    self.log_result("Python API Health Check", False, f"Unexpected status: {data}")
            else:
                self.log_result("Python API Health Check", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Python API Health Check", False, f"Connection error: {str(e)}")
    
    def test_java_api_health(self):
        """Test Java API health check"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.java_api_url}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK':
                    self.log_result("Java API Health Check", True, "API is healthy", response_time)
                else:
                    self.log_result("Java API Health Check", False, f"Unexpected status: {data}")
            else:
                self.log_result("Java API Health Check", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Java API Health Check", False, f"Connection error: {str(e)}")
    
    def test_java_api_test_endpoint(self):
        """Test Java API test endpoint"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.java_api_url}/test", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                expected_message = "Face Recognition Controller is working!"
                if response.text == expected_message:
                    self.log_result("Java API Test Endpoint", True, "Controller working", response_time)
                else:
                    self.log_result("Java API Test Endpoint", False, f"Unexpected response: {response.text}")
            else:
                self.log_result("Java API Test Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Java API Test Endpoint", False, f"Connection error: {str(e)}")
    
    def test_face_registration_python(self):
        """Test face registration via Python API"""
        try:
            # Create sample base64 image (1x1 pixel)
            sample_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            
            data = {
                "name": "Test User Python",
                "image": sample_image,
                "description": "Test user from Python API"
            }
            
            start_time = time.time()
            response = requests.post(f"{self.python_api_url}/face/register", 
                                   json=data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_result("Python API Face Registration", True, 
                                  f"Registered with ID: {result.get('face_id')}", response_time)
                    return result.get('face_id')
                else:
                    self.log_result("Python API Face Registration", False, 
                                  result.get('message', 'Unknown error'))
            else:
                self.log_result("Python API Face Registration", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Python API Face Registration", False, f"Error: {str(e)}")
        return None
    
    def test_face_registration_java(self):
        """Test face registration via Java API"""
        try:
            sample_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            
            data = {
                "name": "Test User Java",
                "image": sample_image,
                "description": "Test user from Java API"
            }
            
            start_time = time.time()
            response = requests.post(f"{self.java_api_url}/register", 
                                   json=data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_result("Java API Face Registration", True, 
                                  f"Registered with ID: {result.get('face_id')}", response_time)
                    return result.get('face_id')
                else:
                    self.log_result("Java API Face Registration", False, 
                                  result.get('message', 'Unknown error'))
            else:
                self.log_result("Java API Face Registration", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Java API Face Registration", False, f"Error: {str(e)}")
        return None
    
    def test_face_list_java(self):
        """Test face list via Java API"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.java_api_url}/list", timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    count = len(result.get('faces', []))
                    self.log_result("Java API Face List", True, 
                                  f"Retrieved {count} faces", response_time)
                else:
                    self.log_result("Java API Face List", False, 
                                  result.get('message', 'Unknown error'))
            else:
                self.log_result("Java API Face List", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Java API Face List", False, f"Error: {str(e)}")
    
    def test_face_recognition_java(self):
        """Test face recognition via Java API"""
        try:
            sample_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            
            data = {
                "image": sample_image,
                "threshold": 0.6
            }
            
            start_time = time.time()
            response = requests.post(f"{self.java_api_url}/recognize", 
                                   json=data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    name = result.get('name', 'Unknown')
                    similarity = result.get('similarity', 0)
                    self.log_result("Java API Face Recognition", True, 
                                  f"Recognized: {name} (similarity: {similarity:.3f})", response_time)
                else:
                    self.log_result("Java API Face Recognition", True, 
                                  result.get('message', 'No face found'), response_time)
            else:
                self.log_result("Java API Face Recognition", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Java API Face Recognition", False, f"Error: {str(e)}")
    
    def test_face_comparison_java(self):
        """Test face comparison via Java API"""
        try:
            sample_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            
            data = {
                "image1": sample_image,
                "image2": sample_image,
                "threshold": 0.6
            }
            
            start_time = time.time()
            response = requests.post(f"{self.java_api_url}/compare", 
                                   json=data, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    similarity = result.get('similarity', 0)
                    match = result.get('match', False)
                    self.log_result("Java API Face Comparison", True, 
                                  f"Similarity: {similarity:.3f}, Match: {match}", response_time)
                else:
                    self.log_result("Java API Face Comparison", False, 
                                  result.get('message', 'Comparison failed'))
            else:
                self.log_result("Java API Face Comparison", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("Java API Face Comparison", False, f"Error: {str(e)}")
    
    def test_system_integration(self):
        """Test integration between Python and Java APIs"""
        print("\n🔄 Testing system integration...")
        
        # Register via Python, recognize via Java
        face_id = self.test_face_registration_python()
        if face_id:
            time.sleep(2)  # Wait for database sync
            self.test_face_recognition_java()
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Face Recognition System Tests...\n")
        
        print("📡 Testing API Health...")
        self.test_python_api_health()
        self.test_java_api_health()
        self.test_java_api_test_endpoint()
        
        print("\n🎭 Testing Face Operations...")
        self.test_face_registration_python()
        self.test_face_registration_java()
        self.test_face_list_java()
        self.test_face_recognition_java()
        self.test_face_comparison_java()
        
        self.test_system_integration()
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for r in self.test_results if r['success'])
        failed = len(self.test_results) - passed
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {passed/len(self.test_results)*100:.1f}%")
        
        if failed > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("\n🎯 System Status:", "HEALTHY" if failed == 0 else "NEEDS ATTENTION")
        print("="*60)

def main():
    """Main function"""
    tester = FaceRecognitionSystemTest()
    
    print("Face Recognition System Integration Test")
    print("Make sure both APIs are running:")
    print("  - Python API: python face_api_server.py")
    print("  - Java API: mvn spring-boot:run")
    print()
    
    input("Press Enter to start testing...")
    
    tester.run_all_tests()

if __name__ == "__main__":
    main()