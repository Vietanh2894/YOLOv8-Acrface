# PowerShell script to fix Spring Boot configs for FastAPI
Write-Host "🔧 Fixing Spring Boot configs for FastAPI (port 8000)..." -ForegroundColor Yellow

$springBootPath = "C:\Users\ADMIN\Downloads\StupidParking\StupidParking"

# Fix FaceRecognitionConfig.java
$faceConfigPath = "$springBootPath\src\main\java\com\example\stupidparking\config\FaceRecognitionConfig.java"
if (Test-Path $faceConfigPath) {
    (Get-Content $faceConfigPath) -replace 'localhost:5000', 'localhost:8000' | Set-Content $faceConfigPath
    Write-Host "✅ Fixed FaceRecognitionConfig.java" -ForegroundColor Green
} else {
    Write-Host "⚠️ FaceRecognitionConfig.java not found" -ForegroundColor Yellow
}

# Fix SimpleFaceRecognitionConfig.java
$simpleFaceConfigPath = "$springBootPath\src\main\java\com\example\stupidparking\config\SimpleFaceRecognitionConfig.java"
if (Test-Path $simpleFaceConfigPath) {
    (Get-Content $simpleFaceConfigPath) -replace 'localhost:5000', 'localhost:8000' | Set-Content $simpleFaceConfigPath
    Write-Host "✅ Fixed SimpleFaceRecognitionConfig.java" -ForegroundColor Green
} else {
    Write-Host "⚠️ SimpleFaceRecognitionConfig.java not found" -ForegroundColor Yellow
}

Write-Host "🎉 All configs updated for FastAPI!" -ForegroundColor Green