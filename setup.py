#!/usr/bin/env python3
"""
Face Recognition System Setup Script
Tự động cài đặt dependencies và thiết lập hệ thống
"""

import subprocess
import sys
import os

def install_package(package):
    """Cài đặt package qua pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Đã cài đặt {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Lỗi cài đặt {package}")
        return False

def main():
    print("🚀 Bắt đầu setup Face Recognition System")
    print("="*50)
    
    # Đọc requirements
    requirements_file = "requirements_face_recognition.txt"
    if not os.path.exists(requirements_file):
        print(f"❌ Không tìm thấy file {requirements_file}")
        return False
    
    with open(requirements_file, 'r') as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"📦 Sẽ cài đặt {len(packages)} packages:")
    for pkg in packages:
        print(f"   - {pkg}")
    
    print("\n🔧 Bắt đầu cài đặt...")
    
    # Upgrade pip trước
    print("⬆️ Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Cài đặt từng package
    failed_packages = []
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n❌ Một số package cài đặt thất bại:")
        for pkg in failed_packages:
            print(f"   - {pkg}")
        return False
    
    print(f"\n✅ Đã cài đặt thành công tất cả {len(packages)} packages!")
    
    # Test import
    print("\n🧪 Kiểm tra import các thư viện chính...")
    
    try:
        import cv2
        print("✅ OpenCV: OK")
    except ImportError:
        print("❌ OpenCV: Failed")
    
    try:
        import numpy as np
        print("✅ NumPy: OK")
    except ImportError:
        print("❌ NumPy: Failed")
    
    try:
        from ultralytics import YOLO
        print("✅ Ultralytics YOLO: OK")
    except ImportError:
        print("❌ Ultralytics YOLO: Failed")
    
    try:
        import insightface
        print("✅ InsightFace: OK")
    except ImportError:
        print("❌ InsightFace: Failed")
    
    try:
        import pymysql
        print("✅ PyMySQL: OK")
    except ImportError:
        print("❌ PyMySQL: Failed")
    
    print("\n🎉 Setup hoàn tất!")
    print("📝 Để chạy hệ thống:")
    print("   python face_recognition_system.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)