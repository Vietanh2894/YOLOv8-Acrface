@echo off
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo 🚀 FACE RECOGNITION SPRING BOOT INTEGRATION
echo ==========================================

if "%1"=="" (
    echo ❌ Error: Please provide Spring Boot project path
    echo Usage: setup_integration.bat "C:\path\to\your\springboot\project"
    exit /b 1
)

set "SPRINGBOOT_PATH=%~1"
set "PACKAGE_NAME=%2"
if "%PACKAGE_NAME%"=="" set "PACKAGE_NAME=com.example.facerecognition"

echo 📁 Spring Boot Path: %SPRINGBOOT_PATH%
echo 📦 Package Name: %PACKAGE_NAME%
echo.

echo 📡 Checking Python API...
curl -s -m 5 "http://localhost:5000/api/health" > nul 2>&1
if %errorlevel%==0 (
    echo ✅ Python API is running at localhost:5000
) else (
    echo ⚠️ Python API not running. Please start: python face_api_server.py
    echo Continuing with integration...
)

echo.
echo 🔧 DIRECT INTEGRATION
echo =====================

echo 📦 Integrating files into Spring Boot project...
python integrate_springboot.py "%SPRINGBOOT_PATH%" --package "%PACKAGE_NAME%"

if %errorlevel%==0 (
    echo.
    echo ✅ Integration completed successfully!
    echo.
    echo 📋 NEXT STEPS:
    echo 1. Start Python API:
    echo    python face_api_server.py
    echo.
    echo 2. Check if your project uses Gradle or Maven:
    echo    - If Gradle: ./gradlew build
    echo    - If Maven:  mvn clean compile
    echo.
    echo 3. Start Spring Boot:
    echo    - If Gradle: ./gradlew bootRun
    echo    - If Maven:  mvn spring-boot:run
    echo.
    echo 4. Test endpoints:
    echo    GET  http://localhost:8080/api/v1/face/health
    echo    POST http://localhost:8080/api/example/verify-face
    echo.
    
    set /p start_api=Do you want to start Python API now? (y/n): 
    if /i "!start_api!"=="y" (
        echo 🚀 Starting Python API...
        start "Python Face API" cmd /k "python face_api_server.py"
    )
) else (
    echo ❌ Integration failed!
    exit /b 1
)

echo.
echo 📖 See INTEGRATION_GUIDE.md for details
echo 🎯 Happy coding!
pause
