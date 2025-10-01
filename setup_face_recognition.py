#!/usr/bin/env python3
"""
SETUP SCRIPT CHO FACE RECOGNITION FASTAPI SERVER
===============================================
Script này sẽ thiết lập toàn bộ môi trường và dependencies
cần thiết để chạy Face Recognition FastAPI Server

Chức năng:
- Kiểm tra và cài đặt Python packages
- Kiểm tra GPU/CUDA support
- Thiết lập database MySQL
- Download và setup AI models
- Kiểm tra cấu hình hệ thống
- Chạy FastAPI server
"""

import sys
import os
import subprocess
import json
import platform
import importlib
import urllib.request
import zipfile
import shutil
from pathlib import Path
import logging
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FaceRecognitionSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.os_info = platform.system()
        self.architecture = platform.machine()
        
        # Required packages với versions
        self.required_packages = {
            'fastapi': '0.104.1',
            'uvicorn[standard]': '0.24.0',
            'pydantic': '2.5.0',
            'python-multipart': '0.0.6',
            'requests': '2.31.0',
            'opencv-python': '4.8.1.78',
            'pillow': '10.1.0',
            'numpy': '1.24.3',
            'pymysql': '1.1.0',
            'cryptography': '41.0.7',
            'insightface': '0.7.3',
            'onnxruntime': '1.16.3',
            'scikit-learn': '1.3.2',
            'matplotlib': '3.8.2',
            'ultralytics': '8.0.206'
        }
        
        # GPU packages (optional)
        self.gpu_packages = {
            'onnxruntime-gpu': '1.16.3',
            'torch': '2.1.1+cu118',
            'torchvision': '0.16.1+cu118'
        }
        
        # Model URLs và paths
        self.models = {
            'yolov8n-face.pt': {
                'url': 'https://github.com/akanametov/yolov8-face/releases/download/v0.0.0/yolov8n-face.pt',
                'path': 'models/yolov8n-face.pt'
            },
            'buffalo_l': {
                'url': 'https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip',
                'path': 'models/buffalo_l'
            }
        }
        
        # Database config
        self.db_config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'face_recognition_db'
        }

    def print_header(self):
        """In header thông tin"""
        print("=" * 80)
        print("🚀 FACE RECOGNITION FASTAPI SERVER SETUP")
        print("=" * 80)
        print(f"📍 Project Directory: {self.project_root}")
        print(f"🐍 Python Version: {self.python_version}")
        print(f"💻 Operating System: {self.os_info} ({self.architecture})")
        print(f"🕒 Setup Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

    def check_python_version(self):
        """Kiểm tra Python version"""
        logger.info("Checking Python version...")
        
        if sys.version_info < (3, 8):
            logger.error(f"❌ Python 3.8+ required, but found {self.python_version}")
            return False
        
        logger.info(f"✅ Python version OK: {self.python_version}")
        return True

    def install_package(self, package, version=None):
        """Cài đặt một package"""
        try:
            if version:
                package_spec = f"{package}=={version}"
            else:
                package_spec = package
            
            logger.info(f"Installing {package_spec}...")
            
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', package_spec
            ], capture_output=True, text=True, check=True)
            
            logger.info(f"✅ Successfully installed {package}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install {package}: {e.stderr}")
            return False

    def check_and_install_packages(self):
        """Kiểm tra và cài đặt packages"""
        logger.info("Checking and installing required packages...")
        
        # Upgrade pip first
        logger.info("Upgrading pip...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      capture_output=True, text=True)
        
        failed_packages = []
        
        for package, version in self.required_packages.items():
            try:
                # Check if package exists
                if '==' in package:
                    package_name = package.split('==')[0]
                elif '[' in package:
                    package_name = package.split('[')[0]
                else:
                    package_name = package
                
                importlib.import_module(package_name.replace('-', '_'))
                logger.info(f"✅ {package} already installed")
                
            except ImportError:
                if not self.install_package(package, version):
                    failed_packages.append(package)
        
        if failed_packages:
            logger.error(f"❌ Failed to install: {', '.join(failed_packages)}")
            return False
        
        logger.info("✅ All required packages installed successfully")
        return True

    def check_gpu_support(self):
        """Kiểm tra GPU support"""
        logger.info("Checking GPU support...")
        
        try:
            import torch
            if torch.cuda.is_available():
                gpu_count = torch.cuda.device_count()
                gpu_name = torch.cuda.get_device_name(0)
                logger.info(f"✅ CUDA available: {gpu_count} GPU(s) detected")
                logger.info(f"🎮 GPU: {gpu_name}")
                
                # Install GPU packages
                for package, version in self.gpu_packages.items():
                    self.install_package(package, version)
                
                return True
            else:
                logger.info("⚠️ CUDA not available, using CPU")
                return False
                
        except ImportError:
            logger.info("⚠️ PyTorch not installed, skipping GPU check")
            return False

    def create_directories(self):
        """Tạo các thư mục cần thiết"""
        logger.info("Creating necessary directories...")
        
        directories = [
            'models',
            'logs',
            'temp',
            'data',
            'uploads'
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(exist_ok=True)
            logger.info(f"✅ Created directory: {directory}")

    def download_file(self, url, destination):
        """Download file từ URL"""
        try:
            logger.info(f"Downloading {url}...")
            
            # Create directory if not exists
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            urllib.request.urlretrieve(url, destination)
            logger.info(f"✅ Downloaded: {destination}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to download {url}: {e}")
            return False

    def extract_zip(self, zip_path, extract_to):
        """Giải nén zip file"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            logger.info(f"✅ Extracted: {zip_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to extract {zip_path}: {e}")
            return False

    def setup_models(self):
        """Download và setup AI models"""
        logger.info("Setting up AI models...")
        
        for model_name, model_info in self.models.items():
            model_path = self.project_root / model_info['path']
            
            if model_path.exists():
                logger.info(f"✅ Model already exists: {model_name}")
                continue
            
            # Download model
            if model_name.endswith('.zip'):
                zip_path = self.project_root / 'temp' / f"{model_name}.zip"
                if self.download_file(model_info['url'], zip_path):
                    self.extract_zip(zip_path, model_path.parent)
                    zip_path.unlink()  # Delete zip file
            else:
                if not self.download_file(model_info['url'], model_path):
                    logger.error(f"❌ Failed to download {model_name}")
                    return False
        
        logger.info("✅ All models setup completed")
        return True

    def setup_database(self):
        """Setup MySQL database"""
        logger.info("Setting up MySQL database...")
        
        try:
            import pymysql
            
            # Connect without database first
            connection = pymysql.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            
            with connection.cursor() as cursor:
                # Create database if not exists
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
                logger.info(f"✅ Database '{self.db_config['database']}' created/verified")
                
                # Use database
                cursor.execute(f"USE {self.db_config['database']}")
                
                # Create faces table
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS faces (
                    face_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    embedding JSON NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_name (name)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
                
                cursor.execute(create_table_sql)
                logger.info("✅ Database table 'faces' created/verified")
            
            connection.commit()
            connection.close()
            
            logger.info("✅ Database setup completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database setup failed: {e}")
            logger.info("💡 Make sure MySQL is running and credentials are correct")
            return False

    def create_config_files(self):
        """Tạo các file config"""
        logger.info("Creating configuration files...")
        
        # Database config
        db_config_content = f"""# Database Configuration
DATABASE_CONFIG = {{
    'host': '{self.db_config['host']}',
    'port': {self.db_config['port']},
    'user': '{self.db_config['user']}',
    'password': '{self.db_config['password']}',
    'database': '{self.db_config['database']}'
}}

# Face Recognition Config
FACE_RECOGNITION_CONFIG = {{
    'similarity_threshold': 0.6,
    'max_faces_per_image': 5,
    'yolo_model_path': 'models/yolov8n-face.pt',
    'insightface_model': 'buffalo_l',
    'insightface_model_path': 'models/buffalo_l'
}}

# Server Config
SERVER_CONFIG = {{
    'host': '0.0.0.0',
    'port': 8000,
    'reload': True,
    'log_level': 'info'
}}
"""
        
        config_path = self.project_root / 'config.py'
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(db_config_content)
        
        logger.info(f"✅ Created: {config_path}")
        
        # Environment file
        env_content = f"""# Environment Variables
PYTHONPATH={self.project_root}
CUDA_VISIBLE_DEVICES=0
OMP_NUM_THREADS=4
"""
        
        env_path = self.project_root / '.env'
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        logger.info(f"✅ Created: {env_path}")

    def create_startup_scripts(self):
        """Tạo startup scripts"""
        logger.info("Creating startup scripts...")
        
        # Windows batch script
        batch_content = f"""@echo off
echo Starting Face Recognition FastAPI Server...
cd /d "{self.project_root}"
python face_fastapi_server.py
pause
"""
        
        batch_path = self.project_root / 'start_server.bat'
        with open(batch_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        logger.info(f"✅ Created: {batch_path}")
        
        # Linux/Mac shell script
        shell_content = f"""#!/bin/bash
echo "Starting Face Recognition FastAPI Server..."
cd "{self.project_root}"
python3 face_fastapi_server.py
"""
        
        shell_path = self.project_root / 'start_server.sh'
        with open(shell_path, 'w', encoding='utf-8') as f:
            f.write(shell_content)
        
        # Make executable on Unix systems
        if self.os_info != 'Windows':
            os.chmod(shell_path, 0o755)
        
        logger.info(f"✅ Created: {shell_path}")

    def create_requirements_file(self):
        """Tạo requirements.txt"""
        logger.info("Creating requirements.txt...")
        
        requirements_content = "\n".join([
            f"{package}=={version}" for package, version in self.required_packages.items()
        ])
        
        requirements_path = self.project_root / 'requirements.txt'
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        
        logger.info(f"✅ Created: {requirements_path}")

    def create_docker_files(self):
        """Tạo Docker files"""
        logger.info("Creating Docker configuration...")
        
        # Dockerfile
        dockerfile_content = f"""FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    libgl1-mesa-glx \\
    libglib2.0-0 \\
    libsm6 \\
    libxext6 \\
    libxrender-dev \\
    libgomp1 \\
    wget \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p models logs temp data uploads

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "face_fastapi_server.py"]
"""
        
        dockerfile_path = self.project_root / 'Dockerfile'
        with open(dockerfile_path, 'w', encoding='utf-8') as f:
            f.write(dockerfile_content)
        
        # Docker Compose
        compose_content = f"""version: '3.8'

services:
  face-recognition-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
      - ./data:/app/data
    environment:
      - PYTHONPATH=/app
    depends_on:
      - mysql
    restart: unless-stopped

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: {self.db_config['password'] or 'root'}
      MYSQL_DATABASE: {self.db_config['database']}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    restart: unless-stopped

volumes:
  mysql_data:
"""
        
        compose_path = self.project_root / 'docker-compose.yml'
        with open(compose_path, 'w', encoding='utf-8') as f:
            f.write(compose_content)
        
        logger.info(f"✅ Created Docker files")

    def test_installation(self):
        """Test cài đặt"""
        logger.info("Testing installation...")
        
        # Test imports
        test_imports = [
            'fastapi',
            'uvicorn',
            'cv2',
            'PIL',
            'numpy',
            'pymysql',
            'insightface'
        ]
        
        for module in test_imports:
            try:
                importlib.import_module(module)
                logger.info(f"✅ {module} import OK")
            except ImportError as e:
                logger.error(f"❌ {module} import failed: {e}")
                return False
        
        # Test file structure
        required_files = [
            'face_fastapi_server.py',
            'face_recognition_system.py',
            'face_processor.py',
            'database_manager.py'
        ]
        
        for file in required_files:
            file_path = self.project_root / file
            if file_path.exists():
                logger.info(f"✅ {file} exists")
            else:
                logger.error(f"❌ {file} missing")
                return False
        
        logger.info("✅ Installation test passed")
        return True

    def run_server(self):
        """Chạy FastAPI server"""
        logger.info("Starting FastAPI server...")
        
        try:
            # Change to project directory
            os.chdir(self.project_root)
            
            # Run server
            subprocess.run([
                sys.executable, 'face_fastapi_server.py'
            ], check=True)
            
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"❌ Server failed to start: {e}")

    def run_setup(self):
        """Chạy toàn bộ setup process"""
        self.print_header()
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Installing packages", self.check_and_install_packages),
            ("Checking GPU support", self.check_gpu_support),
            ("Creating directories", self.create_directories),
            ("Setting up models", self.setup_models),
            ("Setting up database", self.setup_database),
            ("Creating config files", self.create_config_files),
            ("Creating startup scripts", self.create_startup_scripts),
            ("Creating requirements.txt", self.create_requirements_file),
            ("Creating Docker files", self.create_docker_files),
            ("Testing installation", self.test_installation)
        ]
        
        print("\n📋 SETUP PROCESS:")
        print("-" * 50)
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            try:
                success = step_func()
                if success:
                    print(f"✅ {step_name} completed")
                else:
                    print(f"❌ {step_name} failed")
                    return False
            except Exception as e:
                print(f"❌ {step_name} error: {e}")
                return False
        
        print("\n" + "=" * 80)
        print("🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\n📚 USAGE:")
        print("• Run server: python face_fastapi_server.py")
        print("• Or use batch: start_server.bat (Windows)")
        print("• Or use shell: ./start_server.sh (Linux/Mac)")
        print("• API docs: http://localhost:8000/docs")
        print("• Health check: http://localhost:8000/api/v1/simple-face/health")
        
        # Ask if user wants to start server now
        response = input("\n🚀 Start server now? (y/n): ").lower()
        if response == 'y':
            self.run_server()
        
        return True


def main():
    """Main function"""
    try:
        setup = FaceRecognitionSetup()
        setup.run_setup()
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()