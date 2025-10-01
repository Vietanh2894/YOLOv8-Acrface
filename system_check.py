#!/usr/bin/env python3
"""
SYSTEM CHECK SCRIPT
==================
Kiểm tra hệ thống trước khi cài đặt Face Recognition FastAPI Server
"""

import sys
import os
import platform
import subprocess
import psutil
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def print_header():
    """Print header"""
    print("=" * 70)
    print("🔍 FACE RECOGNITION SYSTEM - SYSTEM CHECK")
    print("=" * 70)

def check_python():
    """Check Python version"""
    print("\n🐍 PYTHON CHECK:")
    print(f"   Version: {sys.version}")
    print(f"   Executable: {sys.executable}")
    
    if sys.version_info >= (3, 8):
        print("   ✅ Python version OK")
        return True
    else:
        print("   ❌ Python 3.8+ required")
        return False

def check_system_resources():
    """Check system resources"""
    print("\n💻 SYSTEM RESOURCES:")
    
    # CPU
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    print(f"   CPU: {cpu_count} cores")
    if cpu_freq:
        print(f"   CPU Frequency: {cpu_freq.current:.0f} MHz")
    
    # Memory
    memory = psutil.virtual_memory()
    memory_gb = memory.total / (1024**3)
    print(f"   RAM: {memory_gb:.1f} GB ({memory.percent}% used)")
    
    # Disk
    disk = psutil.disk_usage('/')
    disk_gb = disk.total / (1024**3)
    disk_free_gb = disk.free / (1024**3)
    print(f"   Disk: {disk_gb:.1f} GB total, {disk_free_gb:.1f} GB free")
    
    # Recommendations
    warnings = []
    if memory_gb < 8:
        warnings.append("⚠️ RAM < 8GB - May cause performance issues")
    if disk_free_gb < 10:
        warnings.append("⚠️ Free disk space < 10GB - May not be enough")
    if cpu_count < 4:
        warnings.append("⚠️ CPU cores < 4 - May cause slow processing")
    
    if warnings:
        print("\n   WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
        return False
    else:
        print("   ✅ System resources OK")
        return True

def check_gpu():
    """Check GPU availability"""
    print("\n🎮 GPU CHECK:")
    
    try:
        # Try NVIDIA GPU
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'GeForce' in line or 'RTX' in line or 'GTX' in line or 'Tesla' in line:
                    gpu_info = line.split('|')[1].strip()
                    print(f"   GPU: {gpu_info}")
                    print("   ✅ NVIDIA GPU detected")
                    return True
        
        print("   ⚠️ No NVIDIA GPU detected - Will use CPU")
        return False
        
    except FileNotFoundError:
        print("   ⚠️ nvidia-smi not found - No NVIDIA GPU or drivers")
        return False

def check_mysql():
    """Check MySQL availability"""
    print("\n🗄️ DATABASE CHECK:")
    
    # Check if MySQL service is running
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['sc', 'query', 'mysql'], capture_output=True, text=True)
            if 'RUNNING' in result.stdout:
                print("   ✅ MySQL service is running")
                return True
            else:
                print("   ⚠️ MySQL service not running")
        else:
            result = subprocess.run(['systemctl', 'is-active', 'mysql'], capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ MySQL service is running")
                return True
            else:
                print("   ⚠️ MySQL service not running")
    except:
        pass
    
    # Try to connect to MySQL
    try:
        import pymysql
        conn = pymysql.connect(host='localhost', user='root', password='')
        conn.close()
        print("   ✅ MySQL connection OK")
        return True
    except ImportError:
        print("   ⚠️ PyMySQL not installed")
    except Exception as e:
        print(f"   ⚠️ MySQL connection failed: {e}")
    
    return False

def check_network():
    """Check network connectivity"""
    print("\n🌐 NETWORK CHECK:")
    
    test_urls = [
        'github.com',
        'pypi.org',
        'download.pytorch.org'
    ]
    
    import socket
    
    for url in test_urls:
        try:
            socket.create_connection((url, 80), timeout=5)
            print(f"   ✅ {url} - OK")
        except Exception:
            print(f"   ❌ {url} - Failed")
            return False
    
    return True

def check_dependencies():
    """Check if key dependencies can be imported"""
    print("\n📦 DEPENDENCY CHECK:")
    
    dependencies = {
        'cv2': 'opencv-python',
        'PIL': 'Pillow',
        'numpy': 'numpy',
        'requests': 'requests'
    }
    
    missing = []
    
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Not installed")
            missing.append(package)
    
    if missing:
        print(f"\n   Missing packages: {', '.join(missing)}")
        print("   Run: pip install " + " ".join(missing))
        return False
    
    return True

def check_file_structure():
    """Check if required files exist"""
    print("\n📁 FILE STRUCTURE CHECK:")
    
    required_files = [
        'face_fastapi_server.py',
        'face_recognition_system.py',
        'face_processor.py',
        'database_manager.py'
    ]
    
    missing_files = []
    current_dir = Path.cwd()
    
    for file in required_files:
        file_path = current_dir / file
        if file_path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - Missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n   Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def check_ports():
    """Check if required ports are available"""
    print("\n🔌 PORT CHECK:")
    
    import socket
    
    ports_to_check = [8000, 3306]  # FastAPI, MySQL
    
    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('localhost', port))
            if result == 0:
                print(f"   ⚠️ Port {port} is in use")
            else:
                print(f"   ✅ Port {port} is available")
        finally:
            sock.close()
    
    return True

def generate_report(checks):
    """Generate final report"""
    print("\n" + "=" * 70)
    print("📊 SYSTEM CHECK REPORT")
    print("=" * 70)
    
    passed = sum(checks.values())
    total = len(checks)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {check_name}: {status}")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED!")
        print("   Your system is ready for Face Recognition FastAPI Server")
        print("   Run: python setup_face_recognition.py")
    elif passed >= total - 2:
        print("\n⚠️ MINOR ISSUES DETECTED")
        print("   You can proceed with installation, but may encounter some issues")
        print("   Run: python setup_face_recognition.py")
    else:
        print("\n❌ MAJOR ISSUES DETECTED")
        print("   Please fix the issues above before proceeding")
        print("   Check the INSTALLATION_GUIDE.md for help")
    
    print("\n" + "=" * 70)

def main():
    """Main function"""
    print_header()
    
    checks = {
        'Python Version': check_python(),
        'System Resources': check_system_resources(),
        'GPU Support': check_gpu(),
        'MySQL Database': check_mysql(),
        'Network Connectivity': check_network(),
        'Dependencies': check_dependencies(),
        'File Structure': check_file_structure(),
        'Port Availability': check_ports()
    }
    
    generate_report(checks)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Check interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Check failed: {e}")
        import traceback
        traceback.print_exc()