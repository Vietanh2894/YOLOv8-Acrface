package com.example.facerecognition.controller;

import com.example.facerecognition.service.FaceRecognitionService;
import com.example.facerecognition.service.FaceRecognitionService.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import reactor.core.publisher.Mono;

import java.io.IOException;
import java.util.Base64;

/**
 * REST Controller cho Face Recognition API
 */
@RestController
@RequestMapping("/api/v1/face")
@CrossOrigin(origins = "*") // Cho phép CORS
public class FaceRecognitionController {

    @Autowired
    private FaceRecognitionService faceService;

    /**
     * Kiểm tra trạng thái hệ thống
     */
    @GetMapping("/health")
    public Mono<ResponseEntity<HealthResponse>> checkHealth() {
        return faceService.checkHealth()
                .map(ResponseEntity::ok)
                .onErrorReturn(ResponseEntity.status(500).build());
    }

    /**
     * Đăng ký khuôn mặt từ base64
     */
    @PostMapping("/register")
    public Mono<ResponseEntity<FaceRegisterResponse>> registerFace(
            @RequestBody FaceRegisterRequest request) {

        return faceService.registerFace(
                request.getName(),
                request.getImage(),
                request.getDescription())
                .map(response -> {
                    if (response.getSuccess()) {
                        return ResponseEntity.ok(response);
                    } else {
                        return ResponseEntity.badRequest().body(response);
                    }
                })
                .onErrorReturn(ResponseEntity.status(500).build());
    }

    /**
     * Đăng ký khuôn mặt từ file upload
     */
    @PostMapping("/register-file")
    public Mono<ResponseEntity<FaceRegisterResponse>> registerFaceFromFile(
            @RequestParam("name") String name,
            @RequestParam("image") MultipartFile imageFile,
            @RequestParam(value = "description", required = false) String description) {

        try {
            // Convert MultipartFile to base64
            String base64Image = Base64.getEncoder()
                    .encodeToString(imageFile.getBytes());

            return faceService.registerFace(name, base64Image, description)
                    .map(response -> {
                        if (response.getSuccess()) {
                            return ResponseEntity.ok(response);
                        } else {
                            return ResponseEntity.badRequest().body(response);
                        }
                    })
                    .onErrorReturn(ResponseEntity.status(500).build());

        } catch (IOException e) {
            return Mono.just(ResponseEntity.badRequest().build());
        }
    }

    /**
     * Nhận diện khuôn mặt từ base64
     */
    @PostMapping("/recognize")
    public Mono<ResponseEntity<FaceRecognizeResponse>> recognizeFace(
            @RequestBody FaceRecognizeRequest request) {

        return faceService.recognizeFace(
                request.getImage(),
                request.getThreshold())
                .map(response -> {
                    if (response.getSuccess()) {
                        return ResponseEntity.ok(response);
                    } else {
                        return ResponseEntity.badRequest().body(response);
                    }
                })
                .onErrorReturn(ResponseEntity.status(500).build());
    }

    /**
     * Nhận diện khuôn mặt từ file upload
     */
    @PostMapping("/recognize-file")
    public Mono<ResponseEntity<FaceRecognizeResponse>> recognizeFaceFromFile(
            @RequestParam("image") MultipartFile imageFile,
            @RequestParam(value = "threshold", required = false, defaultValue = "0.6") Double threshold) {

        try {
            String base64Image = Base64.getEncoder()
                    .encodeToString(imageFile.getBytes());

            return faceService.recognizeFace(base64Image, threshold)
                    .map(response -> {
                        if (response.getSuccess()) {
                            return ResponseEntity.ok(response);
                        } else {
                            return ResponseEntity.badRequest().body(response);
                        }
                    })
                    .onErrorReturn(ResponseEntity.status(500).build());

        } catch (IOException e) {
            return Mono.just(ResponseEntity.badRequest().build());
        }
    }

    /**
     * So sánh hai ảnh từ base64
     */
    @PostMapping("/compare")
    public Mono<ResponseEntity<FaceCompareResponse>> compareFaces(
            @RequestBody FaceCompareRequest request) {

        return faceService.compareFaces(
                request.getImage1(),
                request.getImage2(),
                request.getThreshold())
                .map(response -> {
                    if (response.getSuccess()) {
                        return ResponseEntity.ok(response);
                    } else {
                        return ResponseEntity.badRequest().body(response);
                    }
                })
                .onErrorReturn(ResponseEntity.status(500).build());
    }

    /**
     * So sánh hai ảnh từ file uploads
     */
    @PostMapping("/compare-files")
    public Mono<ResponseEntity<FaceCompareResponse>> compareFacesFromFiles(
            @RequestParam("image1") MultipartFile imageFile1,
            @RequestParam("image2") MultipartFile imageFile2,
            @RequestParam(value = "threshold", required = false, defaultValue = "0.6") Double threshold) {

        try {
            String base64Image1 = Base64.getEncoder()
                    .encodeToString(imageFile1.getBytes());
            String base64Image2 = Base64.getEncoder()
                    .encodeToString(imageFile2.getBytes());

            return faceService.compareFaces(base64Image1, base64Image2, threshold)
                    .map(response -> {
                        if (response.getSuccess()) {
                            return ResponseEntity.ok(response);
                        } else {
                            return ResponseEntity.badRequest().body(response);
                        }
                    })
                    .onErrorReturn(ResponseEntity.status(500).build());

        } catch (IOException e) {
            return Mono.just(ResponseEntity.badRequest().build());
        }
    }

    /**
     * Lấy danh sách tất cả khuôn mặt đã đăng ký
     */
    @GetMapping("/list")
    public Mono<ResponseEntity<FaceListResponse>> listRegisteredFaces() {
        return faceService.listRegisteredFaces()
                .map(response -> {
                    if (response.getSuccess()) {
                        return ResponseEntity.ok(response);
                    } else {
                        return ResponseEntity.badRequest().body(response);
                    }
                })
                .onErrorReturn(ResponseEntity.status(500).build());
    }

    /**
     * Xóa khuôn mặt theo ID
     */
    @DeleteMapping("/delete/{faceId}")
    public Mono<ResponseEntity<DeleteFaceResponse>> deleteFace(
            @PathVariable Long faceId) {

        return faceService.deleteFace(faceId)
                .map(response -> {
                    if (response.getSuccess()) {
                        return ResponseEntity.ok(response);
                    } else {
                        return ResponseEntity.notFound().build();
                    }
                })
                .onErrorReturn(ResponseEntity.status(500).build());
    }

    /**
     * Test endpoint để kiểm tra controller hoạt động
     */
    @GetMapping("/test")
    public ResponseEntity<String> test() {
        return ResponseEntity.ok("Face Recognition Controller is working!");
    }
}