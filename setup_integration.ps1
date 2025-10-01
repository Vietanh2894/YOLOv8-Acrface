# PowerShell script để setup Face Recognition với Spring Boot Backend

param(
    [Parameter(Mandatory=$true)]
    [string]$SpringBootPath,
    
    [Parameter(Mandatory=$false)]
    [string]$PackageName = "com.example.facerecognition",
    
    [Parameter(Mandatory=$false)]
    [switch]$Docker
)

Write-Host "🚀 FACE RECOGNITION SPRING BOOT INTEGRATION" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Kiểm tra Python API có đang chạy không
Write-Host "📡 Kiểm tra Python API..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get -TimeoutSec 5
    if ($response.status -eq "OK") {
        Write-Host "✅ Python API đang chạy tại localhost:5000" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ Python API chưa chạy. Hãy chạy: python face_api_server.py" -ForegroundColor Red
    Write-Host "Tiếp tục với integration..." -ForegroundColor Yellow
}

# Option 1: Direct Integration
if (-not $Docker) {
    Write-Host "`n🔧 DIRECT INTEGRATION" -ForegroundColor Cyan
    Write-Host "=====================" -ForegroundColor Cyan
    
    # Chạy Python integration script
    Write-Host "📦 Tích hợp files vào Spring Boot project..." -ForegroundColor Yellow
    python integrate_springboot.py $SpringBootPath --package $PackageName
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Integration hoàn thành!" -ForegroundColor Green
        
        Write-Host "`n📋 NEXT STEPS:" -ForegroundColor Cyan
        Write-Host "1. Start Python API:" -ForegroundColor White
        Write-Host "   python face_api_server.py" -ForegroundColor Gray
        
        Write-Host "`n2. Refresh Maven dependencies:" -ForegroundColor White
        Write-Host "   cd $SpringBootPath" -ForegroundColor Gray
        Write-Host "   mvn clean compile" -ForegroundColor Gray
        
        Write-Host "`n3. Start Spring Boot:" -ForegroundColor White
        Write-Host "   mvn spring-boot:run" -ForegroundColor Gray
        
        Write-Host "`n4. Test endpoints:" -ForegroundColor White
        Write-Host "   GET  http://localhost:8080/api/v1/face/health" -ForegroundColor Gray
        Write-Host "   POST http://localhost:8080/api/example/verify-face" -ForegroundColor Gray
        
        # Hỏi có muốn start Python API không
        $startApi = Read-Host "`nBạn có muốn start Python API ngay không? (y/n)"
        if ($startApi -eq "y" -or $startApi -eq "Y") {
            Write-Host "🚀 Starting Python API..." -ForegroundColor Green
            Start-Process powershell -ArgumentList "-NoExit", "-Command", "python face_api_server.py"
        }
    } else {
        Write-Host "❌ Integration failed!" -ForegroundColor Red
        exit 1
    }
    
} else {
    # Option 2: Docker Integration
    Write-Host "`n🐳 DOCKER INTEGRATION" -ForegroundColor Cyan
    Write-Host "=====================" -ForegroundColor Cyan
    
    # Kiểm tra Docker
    try {
        docker --version | Out-Null
        Write-Host "✅ Docker đã được cài đặt" -ForegroundColor Green
    } catch {
        Write-Host "❌ Docker chưa được cài đặt. Hãy cài Docker Desktop." -ForegroundColor Red
        exit 1
    }
    
    # Copy docker files
    Write-Host "📁 Preparing Docker files..." -ForegroundColor Yellow
    Copy-Item "docker-compose-existing-backend.yml" "$SpringBootPath\docker-compose.yml" -Force
    Copy-Item "Dockerfile.face-api" "$SpringBootPath\Dockerfile.face-api" -Force
    Copy-Item "nginx.conf" "$SpringBootPath\nginx.conf" -Force
    
    Write-Host "✅ Docker files copied to Spring Boot project" -ForegroundColor Green
    
    Write-Host "`n📋 DOCKER SETUP STEPS:" -ForegroundColor Cyan
    Write-Host "1. Update docker-compose.yml với your Spring Boot image" -ForegroundColor White
    Write-Host "2. Build và run containers:" -ForegroundColor White
    Write-Host "   cd $SpringBootPath" -ForegroundColor Gray
    Write-Host "   docker-compose up --build" -ForegroundColor Gray
    
    Write-Host "`n🌐 Access URLs:" -ForegroundColor White
    Write-Host "   - Your Spring Boot: http://localhost:8080" -ForegroundColor Gray
    Write-Host "   - Face API: http://localhost:5000" -ForegroundColor Gray
    Write-Host "   - Nginx Proxy: http://localhost:80" -ForegroundColor Gray
}

Write-Host "`n📖 Xem chi tiết trong INTEGRATION_GUIDE.md" -ForegroundColor Blue
Write-Host "🎯 Happy coding!" -ForegroundColor Green