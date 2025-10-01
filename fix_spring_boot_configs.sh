#!/bin/bash
# Fix Spring Boot configs for FastAPI integration

echo "🔧 Fixing Spring Boot configs for FastAPI (port 8000)..."

# Find and replace in Java files
SPRING_BOOT_PATH="C:/Users/ADMIN/Downloads/StupidParking/StupidParking"

# Fix FaceRecognitionConfig.java
if [ -f "$SPRING_BOOT_PATH/src/main/java/com/example/stupidparking/config/FaceRecognitionConfig.java" ]; then
    sed -i 's/localhost:5000/localhost:8000/g' "$SPRING_BOOT_PATH/src/main/java/com/example/stupidparking/config/FaceRecognitionConfig.java"
    echo "✅ Fixed FaceRecognitionConfig.java"
fi

# Fix SimpleFaceRecognitionConfig.java  
if [ -f "$SPRING_BOOT_PATH/src/main/java/com/example/stupidparking/config/SimpleFaceRecognitionConfig.java" ]; then
    sed -i 's/localhost:5000/localhost:8000/g' "$SPRING_BOOT_PATH/src/main/java/com/example/stupidparking/config/SimpleFaceRecognitionConfig.java"
    echo "✅ Fixed SimpleFaceRecognitionConfig.java"
fi

echo "🎉 All configs updated for FastAPI!"