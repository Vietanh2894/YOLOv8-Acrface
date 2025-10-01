#!/usr/bin/env python3
"""
Script tự động tích hợp Face Recognition vào Java Spring Boot project
"""

import os
import shutil
import sys
from pathlib import Path
import argparse

class SpringBootIntegrator:
    def __init__(self, spring_boot_path, package_name="com.example.facerecognition"):
        self.spring_boot_path = Path(spring_boot_path)
        self.package_name = package_name
        self.package_path = package_name.replace(".", "/")
        self.src_main_java = self.spring_boot_path / "src" / "main" / "java"
        self.src_main_resources = self.spring_boot_path / "src" / "main" / "resources"
        
    def validate_spring_boot_project(self):
        """Kiểm tra xem đây có phải Spring Boot project không"""
        pom_xml = self.spring_boot_path / "pom.xml"
        build_gradle = self.spring_boot_path / "build.gradle"
        build_gradle_kts = self.spring_boot_path / "build.gradle.kts"
        
        if not (pom_xml.exists() or build_gradle.exists() or build_gradle_kts.exists()):
            raise Exception("Không tìm thấy pom.xml, build.gradle, hoặc build.gradle.kts. Đây có phải Spring Boot project?")
        
        if not self.src_main_java.exists():
            raise Exception("Không tìm thấy thư mục src/main/java")
        
        # Determine if it's Maven or Gradle
        self.is_maven = pom_xml.exists()
        self.is_gradle = build_gradle.exists() or build_gradle_kts.exists()
        self.gradle_kts = build_gradle_kts.exists()
        
        return True
    
    def create_package_structure(self):
        """Tạo cấu trúc package"""
        base_package = self.src_main_java / self.package_path
        
        # Tạo các thư mục cần thiết
        directories = [
            base_package / "config",
            base_package / "controller", 
            base_package / "service",
            base_package / "dto" / "face"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Tạo thư mục: {directory}")
        
        return base_package
    
    def copy_java_files(self, base_package):
        """Copy các file Java cần thiết"""
        current_dir = Path(__file__).parent
        
        # Mapping files to copy
        files_to_copy = {
            "FaceRecognitionConfig.java": base_package / "config" / "FaceRecognitionConfig.java",
            "FaceRecognitionController.java": base_package / "controller" / "FaceRecognitionController.java", 
            "FaceRecognitionService.java": base_package / "service" / "FaceRecognitionService.java"
        }
        
        for source_file, target_file in files_to_copy.items():
            source_path = current_dir / source_file
            
            if source_path.exists():
                # Đọc file và thay đổi package name
                with open(source_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Thay đổi package declaration
                content = self.update_package_declaration(content, source_file)
                
                # Ghi file
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Copy và update: {source_file} -> {target_file}")
            else:
                print(f"❌ Không tìm thấy file: {source_file}")
    
    def update_package_declaration(self, content, filename):
        """Update package declaration trong Java files"""
        if "Config.java" in filename:
            return content.replace(
                "package com.example.facerecognition.config;",
                f"package {self.package_name}.config;"
            )
        elif "Controller.java" in filename:
            content = content.replace(
                "package com.example.facerecognition.controller;",
                f"package {self.package_name}.controller;"
            )
            content = content.replace(
                "import com.example.facerecognition.service.FaceRecognitionService;",
                f"import {self.package_name}.service.FaceRecognitionService;"
            )
            return content
        elif "Service.java" in filename:
            return content.replace(
                "package com.example.facerecognition.service;",
                f"package {self.package_name}.service;"
            )
        
        return content
    
    def update_build_file(self):
        """Thêm dependencies vào build file (Maven hoặc Gradle)"""
        if self.is_maven:
            self.update_pom_xml()
        elif self.is_gradle:
            self.update_gradle_build()
    
    def update_pom_xml(self):
        """Thêm dependencies vào pom.xml"""
        pom_path = self.spring_boot_path / "pom.xml"
        
        if not pom_path.exists():
            print("⚠️ Không tìm thấy pom.xml, bỏ qua việc update dependencies")
            return
        
        with open(pom_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Kiểm tra xem đã có webflux dependency chưa
        if "spring-boot-starter-webflux" not in content:
            # Tìm vị trí </dependencies> cuối cùng
            dependency_insert_pos = content.rfind("</dependencies>")
            
            if dependency_insert_pos != -1:
                webflux_dependency = """
		<!-- Face Recognition WebFlux Dependency -->
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-webflux</artifactId>
		</dependency>
"""
                
                new_content = (content[:dependency_insert_pos] + 
                             webflux_dependency + 
                             content[dependency_insert_pos:])
                
                with open(pom_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("✅ Đã thêm spring-boot-starter-webflux vào pom.xml")
            else:
                print("❌ Không tìm thấy tag </dependencies> trong pom.xml")
        else:
            print("ℹ️ WebFlux dependency đã tồn tại trong pom.xml")
    
    def update_gradle_build(self):
        """Thêm dependencies vào build.gradle hoặc build.gradle.kts"""
        if self.gradle_kts:
            build_file = self.spring_boot_path / "build.gradle.kts"
            dependency_syntax = 'implementation("org.springframework.boot:spring-boot-starter-webflux")'
        else:
            build_file = self.spring_boot_path / "build.gradle"
            dependency_syntax = "implementation 'org.springframework.boot:spring-boot-starter-webflux'"
        
        with open(build_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "spring-boot-starter-webflux" not in content:
            # Tìm dependencies block
            dependencies_start = content.find("dependencies {")
            
            if dependencies_start != -1:
                # Tìm dòng đầu tiên trong dependencies block
                first_impl_pos = content.find("implementation", dependencies_start)
                
                if first_impl_pos != -1:
                    # Insert before first implementation
                    webflux_dep = f"\t{dependency_syntax}\n\t"
                    new_content = content[:first_impl_pos] + webflux_dep + content[first_impl_pos:]
                else:
                    # Insert after dependencies {
                    insert_pos = content.find("{", dependencies_start) + 1
                    webflux_dep = f"\n\t{dependency_syntax}\n"
                    new_content = content[:insert_pos] + webflux_dep + content[insert_pos:]
                
                with open(build_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ Đã thêm spring-boot-starter-webflux vào {build_file.name}")
            else:
                print(f"❌ Không tìm thấy dependencies block trong {build_file.name}")
        else:
            print(f"ℹ️ WebFlux dependency đã tồn tại trong {build_file.name}")
    
    def update_application_properties(self):
        """Thêm cấu hình vào application.properties"""
        props_path = self.src_main_resources / "application.properties"
        
        # Tạo file nếu chưa tồn tại
        if not props_path.exists():
            props_path.touch()
        
        with open(props_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Kiểm tra xem đã có config face recognition chưa
        if "face.api.base-url" not in content:
            face_config = """
# Face Recognition API Configuration (FastAPI)
face.api.base-url=http://localhost:8000/api
face.api.timeout.connection=30
face.api.timeout.response=60

# Multipart Configuration for face image uploads
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
"""
            
            with open(props_path, 'a', encoding='utf-8') as f:
                f.write(face_config)
            
            print("✅ Đã thêm Face Recognition config vào application.properties")
        else:
            print("ℹ️ Face Recognition config đã tồn tại trong application.properties")
    
    def create_usage_example(self, base_package):
        """Tạo file example sử dụng"""
        example_content = f"""package {self.package_name}.example;

import {self.package_name}.service.FaceRecognitionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import reactor.core.publisher.Mono;

import java.io.IOException;
import java.util.Base64;
import java.util.Map;

/**
 * Example integration của Face Recognition vào existing controller
 */
@RestController
@RequestMapping("/api/example")
public class FaceExampleController {{
    
    @Autowired
    private FaceRecognitionService faceService;
    
    @PostMapping("/employee/register-face")
    public Mono<ResponseEntity<?>> registerEmployeeFace(
            @RequestParam("employeeId") Long employeeId,
            @RequestParam("photo") MultipartFile photo) {{
        
        try {{
            String base64Image = Base64.getEncoder()
                .encodeToString(photo.getBytes());
            
            return faceService.registerFace(
                    "Employee-" + employeeId, 
                    base64Image, 
                    "Employee ID: " + employeeId
                )
                .map(response -> {{
                    if (response.getSuccess()) {{
                        return ResponseEntity.ok(Map.of(
                            "success", true,
                            "message", "Face registered successfully",
                            "faceId", response.getFaceId()
                        ));
                    }} else {{
                        return ResponseEntity.badRequest()
                            .body(Map.of("success", false, "message", response.getMessage()));
                    }}
                }});
                
        }} catch (IOException e) {{
            return Mono.just(ResponseEntity.badRequest()
                .body(Map.of("success", false, "message", "Failed to process image")));
        }}
    }}
    
    @PostMapping("/verify-face")
    public Mono<ResponseEntity<?>> verifyFace(
            @RequestParam("photo") MultipartFile photo,
            @RequestParam(value = "threshold", defaultValue = "0.7") Double threshold) {{
        
        try {{
            String base64Image = Base64.getEncoder()
                .encodeToString(photo.getBytes());
            
            return faceService.recognizeFace(base64Image, threshold)
                .map(response -> {{
                    if (response.getSuccess() && response.getSimilarity() > threshold) {{
                        return ResponseEntity.ok(Map.of(
                            "verified", true,
                            "name", response.getName(),
                            "similarity", response.getSimilarity(),
                            "faceId", response.getFaceId()
                        ));
                    }} else {{
                        return ResponseEntity.status(401)
                            .body(Map.of("verified", false, "message", "Face not recognized"));
                    }}
                }});
                
        }} catch (IOException e) {{
            return Mono.just(ResponseEntity.badRequest()
                .body(Map.of("verified", false, "message", "Failed to process image")));
        }}
    }}
}}
"""
        
        example_dir = base_package / "example"
        example_dir.mkdir(exist_ok=True)
        example_file = example_dir / "FaceExampleController.java"
        
        with open(example_file, 'w', encoding='utf-8') as f:
            f.write(example_content)
        
        print(f"✅ Tạo file example: {example_file}")
    
    def integrate(self):
        """Thực hiện tích hợp"""
        print("🚀 Bắt đầu tích hợp Face Recognition vào Spring Boot project...")
        print(f"📁 Project path: {self.spring_boot_path}")
        print(f"📦 Package name: {self.package_name}")
        print()
        
        try:
            # Validate project
            self.validate_spring_boot_project()
            print("✅ Đã xác thực Spring Boot project")
            
            # Create package structure
            base_package = self.create_package_structure()
            
            # Copy Java files
            self.copy_java_files(base_package)
            
            # Update build file (Maven or Gradle)
            self.update_build_file()
            
            # Update application.properties
            self.update_application_properties()
            
            # Create usage example
            self.create_usage_example(base_package)
            
            print()
            print("🎉 TÍCH HỢP HOÀN THÀNH!")
            print("="*50)
            print("📋 Các bước tiếp theo:")
            print("1. Chạy FastAPI server: python face_fastapi_server.py")
            if self.is_gradle:
                print("2. Refresh Gradle dependencies: ./gradlew build")
                print("3. Start Spring Boot: ./gradlew bootRun")
            else:
                print("2. Refresh Maven dependencies: mvn clean compile")
                print("3. Start Spring Boot: mvn spring-boot:run")
            print("4. Test API tại: http://localhost:8080/api/example/verify-face")
            print("5. FastAPI docs: http://localhost:8000/docs")
            print()
            print("📖 Xem thêm trong file INTEGRATION_GUIDE.md")
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Tích hợp Face Recognition vào Spring Boot project')
    parser.add_argument('spring_boot_path', help='Đường dẫn đến Spring Boot project')
    parser.add_argument('--package', default='com.example.facerecognition', 
                       help='Package name (default: com.example.facerecognition)')
    
    args = parser.parse_args()
    
    integrator = SpringBootIntegrator(args.spring_boot_path, args.package)
    integrator.integrate()

if __name__ == "__main__":
    main()