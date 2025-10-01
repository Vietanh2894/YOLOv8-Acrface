#!/usr/bin/env python3
"""
Test script cho FastAPI Face Recognition Server
"""

import asyncio
import httpx
import base64
import json
import time
from pathlib import Path

class FastAPITester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.api_url = f"{self.base_url}/api"
        self.timeout = 30
        
    def encode_sample_image(self):
        """Create a small sample image in base64"""
        # 1x1 pixel PNG image
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    async def test_health(self, client: httpx.AsyncClient):
        """Test health endpoint"""
        try:
            response = await client.get(f"{self.api_url}/health")
            print(f"✅ Health Check: {response.status_code} - {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Health Check Failed: {e}")
            return False
    
    async def test_register_face(self, client: httpx.AsyncClient):
        """Test face registration"""
        try:
            data = {
                "name": "Test User FastAPI",
                "image": self.encode_sample_image(),
                "description": "Test user for FastAPI"
            }
            
            response = await client.post(
                f"{self.api_url}/face/register",
                json=data,
                timeout=self.timeout
            )
            
            result = response.json()
            print(f"✅ Register Face: {response.status_code} - {result}")
            return response.status_code == 200 and result.get("success")
            
        except Exception as e:
            print(f"❌ Register Face Failed: {e}")
            return False
    
    async def test_recognize_face(self, client: httpx.AsyncClient):
        """Test face recognition"""
        try:
            data = {
                "image": self.encode_sample_image(),
                "threshold": 0.6
            }
            
            response = await client.post(
                f"{self.api_url}/face/recognize",
                json=data,
                timeout=self.timeout
            )
            
            result = response.json()
            print(f"✅ Recognize Face: {response.status_code} - {result}")
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Recognize Face Failed: {e}")
            return False
    
    async def test_compare_faces(self, client: httpx.AsyncClient):
        """Test face comparison"""
        try:
            data = {
                "image1": self.encode_sample_image(),
                "image2": self.encode_sample_image(),
                "threshold": 0.6
            }
            
            response = await client.post(
                f"{self.api_url}/face/compare",
                json=data,
                timeout=self.timeout
            )
            
            result = response.json()
            print(f"✅ Compare Faces: {response.status_code} - {result}")
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Compare Faces Failed: {e}")
            return False
    
    async def test_list_faces(self, client: httpx.AsyncClient):
        """Test list faces"""
        try:
            response = await client.get(
                f"{self.api_url}/face/list",
                timeout=self.timeout
            )
            
            result = response.json()
            print(f"✅ List Faces: {response.status_code} - Found {result.get('count', 0)} faces")
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ List Faces Failed: {e}")
            return False
    
    async def test_file_upload(self, client: httpx.AsyncClient):
        """Test file upload endpoints"""
        try:
            # Create a test image file
            image_data = base64.b64decode(self.encode_sample_image())
            
            # Test register with file
            files = {"file": ("test.png", image_data, "image/png")}
            data = {"name": "File Test User", "description": "Test file upload"}
            
            response = await client.post(
                f"{self.api_url}/face/register-file",
                files=files,
                data=data,
                timeout=self.timeout
            )
            
            result = response.json()
            print(f"✅ Register File: {response.status_code} - {result}")
            
            # Test recognize with file
            files = {"file": ("test.png", image_data, "image/png")}
            data = {"threshold": "0.6"}
            
            response = await client.post(
                f"{self.api_url}/face/recognize-file",
                files=files,
                data=data,
                timeout=self.timeout
            )
            
            result = response.json()
            print(f"✅ Recognize File: {response.status_code} - {result}")
            return True
            
        except Exception as e:
            print(f"❌ File Upload Test Failed: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting FastAPI Face Recognition Tests...")
        print("=" * 60)
        
        async with httpx.AsyncClient() as client:
            tests = [
                ("Health Check", self.test_health),
                ("Register Face", self.test_register_face),
                ("Recognize Face", self.test_recognize_face),
                ("Compare Faces", self.test_compare_faces),
                ("List Faces", self.test_list_faces),
                ("File Upload", self.test_file_upload)
            ]
            
            results = []
            
            for test_name, test_func in tests:
                print(f"\n🧪 Testing {test_name}...")
                try:
                    result = await test_func(client)
                    results.append((test_name, result))
                except Exception as e:
                    print(f"❌ {test_name} Error: {e}")
                    results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\nPassed: {passed}/{total}")
        print(f"Success Rate: {passed/total*100:.1f}%")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️ Some tests failed. Check the logs above.")
        
        print("\n📚 API Documentation:")
        print(f"  Swagger UI: {self.base_url}/docs")
        print(f"  ReDoc: {self.base_url}/redoc")

async def main():
    print("FastAPI Face Recognition Test Suite")
    print("Make sure FastAPI server is running: python face_fastapi_server.py")
    print()
    
    # Check if server is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ FastAPI server is running")
            else:
                print("⚠️ Server responded but health check failed")
    except Exception:
        print("❌ FastAPI server not running. Please start it first:")
        print("   python face_fastapi_server.py")
        return
    
    input("\nPress Enter to start testing...")
    
    tester = FastAPITester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())