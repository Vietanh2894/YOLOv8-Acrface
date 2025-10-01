package com.example.facerecognition.service;

import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Base64;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Service để tích hợp với Python Face Recognition API
 */
@Service
public class FaceRecognitionService {

    private final WebClient webClient;
    private final ObjectMapper objectMapper;
    private static final String API_BASE_URL = "http://localhost:8000/api"; // Changed to FastAPI port

    public FaceRecognitionService() {
        this.webClient = WebClient.builder()
                .baseUrl(API_BASE_URL)
                .build();
        this.objectMapper = new ObjectMapper();
    }

    /**
     * Kiểm tra trạng thái hệ thống Face Recognition
     */
    public Mono<HealthResponse> checkHealth() {
        return webClient.get()
                .uri("/health")
                .retrieve()
                .bodyToMono(HealthResponse.class);
    }

    /**
     * Đăng ký khuôn mặt mới
     */
    public Mono<FaceRegisterResponse> registerFace(String name, String base64Image, String description) {
        FaceRegisterRequest request = new FaceRegisterRequest();
        request.setName(name);
        request.setImage(base64Image);
        request.setDescription(description);

        return webClient.post()
                .uri("/face/register")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(FaceRegisterResponse.class);
    }

    /**
     * Đăng ký khuôn mặt từ file path
     */
    public Mono<FaceRegisterResponse> registerFaceFromFile(String name, String imagePath, String description) {
        try {
            String base64Image = encodeImageToBase64(imagePath);
            return registerFace(name, base64Image, description);
        } catch (IOException e) {
            return Mono.error(new RuntimeException("Không thể đọc file ảnh: " + imagePath, e));
        }
    }

    /**
     * Nhận diện khuôn mặt trong ảnh
     */
    public Mono<FaceRecognizeResponse> recognizeFace(String base64Image, Double threshold) {
        FaceRecognizeRequest request = new FaceRecognizeRequest();
        request.setImage(base64Image);
        request.setThreshold(threshold != null ? threshold : 0.6);

        return webClient.post()
                .uri("/face/recognize")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(FaceRecognizeResponse.class);
    }

    /**
     * Nhận diện khuôn mặt từ file path
     */
    public Mono<FaceRecognizeResponse> recognizeFaceFromFile(String imagePath, Double threshold) {
        try {
            String base64Image = encodeImageToBase64(imagePath);
            return recognizeFace(base64Image, threshold);
        } catch (IOException e) {
            return Mono.error(new RuntimeException("Không thể đọc file ảnh: " + imagePath, e));
        }
    }

    /**
     * So sánh hai ảnh khuôn mặt
     */
    public Mono<FaceCompareResponse> compareFaces(String base64Image1, String base64Image2, Double threshold) {
        FaceCompareRequest request = new FaceCompareRequest();
        request.setImage1(base64Image1);
        request.setImage2(base64Image2);
        request.setThreshold(threshold != null ? threshold : 0.6);

        return webClient.post()
                .uri("/face/compare")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(FaceCompareResponse.class);
    }

    /**
     * So sánh hai ảnh từ file paths
     */
    public Mono<FaceCompareResponse> compareFacesFromFiles(String imagePath1, String imagePath2, Double threshold) {
        try {
            String base64Image1 = encodeImageToBase64(imagePath1);
            String base64Image2 = encodeImageToBase64(imagePath2);
            return compareFaces(base64Image1, base64Image2, threshold);
        } catch (IOException e) {
            return Mono.error(new RuntimeException("Không thể đọc file ảnh", e));
        }
    }

    /**
     * Lấy danh sách tất cả khuôn mặt đã đăng ký
     */
    public Mono<FaceListResponse> listRegisteredFaces() {
        return webClient.get()
                .uri("/face/list")
                .retrieve()
                .bodyToMono(FaceListResponse.class);
    }

    /**
     * Xóa khuôn mặt theo ID
     */
    public Mono<DeleteFaceResponse> deleteFace(Long faceId) {
        return webClient.delete()
                .uri("/face/delete/" + faceId)
                .retrieve()
                .bodyToMono(DeleteFaceResponse.class);
    }

    /**
     * Chuyển file ảnh thành base64 string
     */
    private String encodeImageToBase64(String imagePath) throws IOException {
        byte[] imageBytes = Files.readAllBytes(Path.of(imagePath));
        return Base64.getEncoder().encodeToString(imageBytes);
    }

    // DTO Classes

    public static class HealthResponse {
        private String status;
        private String message;
        private String timestamp;
        private Integer totalRegisteredFaces;
        private String version;

        // Getters and Setters
        public String getStatus() {
            return status;
        }

        public void setStatus(String status) {
            this.status = status;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }

        public String getTimestamp() {
            return timestamp;
        }

        public void setTimestamp(String timestamp) {
            this.timestamp = timestamp;
        }

        public Integer getTotalRegisteredFaces() {
            return totalRegisteredFaces;
        }

        public void setTotalRegisteredFaces(Integer totalRegisteredFaces) {
            this.totalRegisteredFaces = totalRegisteredFaces;
        }

        public String getVersion() {
            return version;
        }

        public void setVersion(String version) {
            this.version = version;
        }
    }

    public static class FaceRegisterRequest {
        private String name;
        private String image;
        private String description;

        // Getters and Setters
        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getImage() {
            return image;
        }

        public void setImage(String image) {
            this.image = image;
        }

        public String getDescription() {
            return description;
        }

        public void setDescription(String description) {
            this.description = description;
        }
    }

    public static class FaceRegisterResponse {
        private Boolean success;
        private String message;
        private FaceRegisterData data;

        // Getters and Setters
        public Boolean getSuccess() {
            return success;
        }

        public void setSuccess(Boolean success) {
            this.success = success;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }

        public FaceRegisterData getData() {
            return data;
        }

        public void setData(FaceRegisterData data) {
            this.data = data;
        }

        public static class FaceRegisterData {
            private Long faceId;
            private String personName;
            private Double confidence;
            private Integer embeddingDimension;
            private String description;

            // Getters and Setters
            public Long getFaceId() {
                return faceId;
            }

            public void setFaceId(Long faceId) {
                this.faceId = faceId;
            }

            public String getPersonName() {
                return personName;
            }

            public void setPersonName(String personName) {
                this.personName = personName;
            }

            public Double getConfidence() {
                return confidence;
            }

            public void setConfidence(Double confidence) {
                this.confidence = confidence;
            }

            public Integer getEmbeddingDimension() {
                return embeddingDimension;
            }

            public void setEmbeddingDimension(Integer embeddingDimension) {
                this.embeddingDimension = embeddingDimension;
            }

            public String getDescription() {
                return description;
            }

            public void setDescription(String description) {
                this.description = description;
            }
        }
    }

    public static class FaceRecognizeRequest {
        private String image;
        private Double threshold;

        // Getters and Setters
        public String getImage() {
            return image;
        }

        public void setImage(String image) {
            this.image = image;
        }

        public Double getThreshold() {
            return threshold;
        }

        public void setThreshold(Double threshold) {
            this.threshold = threshold;
        }
    }

    public static class FaceRecognizeResponse {
        private Boolean success;
        private String message;
        private FaceRecognizeData data;

        // Getters and Setters
        public Boolean getSuccess() {
            return success;
        }

        public void setSuccess(Boolean success) {
            this.success = success;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }

        public FaceRecognizeData getData() {
            return data;
        }

        public void setData(FaceRecognizeData data) {
            this.data = data;
        }
    }

    public static class FaceRecognizeData {
        private Integer totalFaces;
        private Double thresholdUsed;
        private java.util.List<RecognizedFace> faces;

        // Getters and Setters
        public Integer getTotalFaces() {
            return totalFaces;
        }

        public void setTotalFaces(Integer totalFaces) {
            this.totalFaces = totalFaces;
        }

        public Double getThresholdUsed() {
            return thresholdUsed;
        }

        public void setThresholdUsed(Double thresholdUsed) {
            this.thresholdUsed = thresholdUsed;
        }

        public java.util.List<RecognizedFace> getFaces() {
            return faces;
        }

        public void setFaces(java.util.List<RecognizedFace> faces) {
            this.faces = faces;
        }
    }

    public static class RecognizedFace {
        private Integer faceIndex;
        private BoundingBox boundingBox;
        private Double detectionConfidence;
        private Boolean matchFound;
        private String personName;
        private Double matchSimilarity;
        private Long faceId;
        private Double bestSimilarity;

        // Getters and Setters
        public Integer getFaceIndex() {
            return faceIndex;
        }

        public void setFaceIndex(Integer faceIndex) {
            this.faceIndex = faceIndex;
        }

        public BoundingBox getBoundingBox() {
            return boundingBox;
        }

        public void setBoundingBox(BoundingBox boundingBox) {
            this.boundingBox = boundingBox;
        }

        public Double getDetectionConfidence() {
            return detectionConfidence;
        }

        public void setDetectionConfidence(Double detectionConfidence) {
            this.detectionConfidence = detectionConfidence;
        }

        public Boolean getMatchFound() {
            return matchFound;
        }

        public void setMatchFound(Boolean matchFound) {
            this.matchFound = matchFound;
        }

        public String getPersonName() {
            return personName;
        }

        public void setPersonName(String personName) {
            this.personName = personName;
        }

        public Double getMatchSimilarity() {
            return matchSimilarity;
        }

        public void setMatchSimilarity(Double matchSimilarity) {
            this.matchSimilarity = matchSimilarity;
        }

        public Long getFaceId() {
            return faceId;
        }

        public void setFaceId(Long faceId) {
            this.faceId = faceId;
        }

        public Double getBestSimilarity() {
            return bestSimilarity;
        }

        public void setBestSimilarity(Double bestSimilarity) {
            this.bestSimilarity = bestSimilarity;
        }

        public static class BoundingBox {
            private Integer x1, y1, x2, y2;

            // Getters and Setters
            public Integer getX1() {
                return x1;
            }

            public void setX1(Integer x1) {
                this.x1 = x1;
            }

            public Integer getY1() {
                return y1;
            }

            public void setY1(Integer y1) {
                this.y1 = y1;
            }

            public Integer getX2() {
                return x2;
            }

            public void setX2(Integer x2) {
                this.x2 = x2;
            }

            public Integer getY2() {
                return y2;
            }

            public void setY2(Integer y2) {
                this.y2 = y2;
            }
        }
    }

    public static class FaceCompareRequest {
        private String image1;
        private String image2;
        private Double threshold;

        // Getters and Setters
        public String getImage1() {
            return image1;
        }

        public void setImage1(String image1) {
            this.image1 = image1;
        }

        public String getImage2() {
            return image2;
        }

        public void setImage2(String image2) {
            this.image2 = image2;
        }

        public Double getThreshold() {
            return threshold;
        }

        public void setThreshold(Double threshold) {
            this.threshold = threshold;
        }
    }

    public static class FaceCompareResponse {
        private Boolean success;
        private String message;
        private FaceCompareData data;

        // Getters and Setters
        public Boolean getSuccess() {
            return success;
        }

        public void setSuccess(Boolean success) {
            this.success = success;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }

        public FaceCompareData getData() {
            return data;
        }

        public void setData(FaceCompareData data) {
            this.data = data;
        }

        public static class FaceCompareData {
            private Double similarity;
            private Boolean isSamePerson;
            private Double threshold;
            private Double confidence;
            private ImageInfo image1Info;
            private ImageInfo image2Info;

            // Getters and Setters
            public Double getSimilarity() {
                return similarity;
            }

            public void setSimilarity(Double similarity) {
                this.similarity = similarity;
            }

            public Boolean getIsSamePerson() {
                return isSamePerson;
            }

            public void setIsSamePerson(Boolean isSamePerson) {
                this.isSamePerson = isSamePerson;
            }

            public Double getThreshold() {
                return threshold;
            }

            public void setThreshold(Double threshold) {
                this.threshold = threshold;
            }

            public Double getConfidence() {
                return confidence;
            }

            public void setConfidence(Double confidence) {
                this.confidence = confidence;
            }

            public ImageInfo getImage1Info() {
                return image1Info;
            }

            public void setImage1Info(ImageInfo image1Info) {
                this.image1Info = image1Info;
            }

            public ImageInfo getImage2Info() {
                return image2Info;
            }

            public void setImage2Info(ImageInfo image2Info) {
                this.image2Info = image2Info;
            }

            public static class ImageInfo {
                private Integer facesCount;
                private Double detectionConfidence;

                // Getters and Setters
                public Integer getFacesCount() {
                    return facesCount;
                }

                public void setFacesCount(Integer facesCount) {
                    this.facesCount = facesCount;
                }

                public Double getDetectionConfidence() {
                    return detectionConfidence;
                }

                public void setDetectionConfidence(Double detectionConfidence) {
                    this.detectionConfidence = detectionConfidence;
                }
            }
        }
    }

    public static class FaceListResponse {
        private Boolean success;
        private String message;
        private FaceListData data;

        // Getters and Setters
        public Boolean getSuccess() {
            return success;
        }

        public void setSuccess(Boolean success) {
            this.success = success;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }

        public FaceListData getData() {
            return data;
        }

        public void setData(FaceListData data) {
            this.data = data;
        }

        public static class FaceListData {
            private Integer totalFaces;
            private java.util.List<FaceInfo> faces;

            // Getters and Setters
            public Integer getTotalFaces() {
                return totalFaces;
            }

            public void setTotalFaces(Integer totalFaces) {
                this.totalFaces = totalFaces;
            }

            public java.util.List<FaceInfo> getFaces() {
                return faces;
            }

            public void setFaces(java.util.List<FaceInfo> faces) {
                this.faces = faces;
            }

            public static class FaceInfo {
                private Long faceId;
                private String name;
                private Integer embeddingDimension;

                // Getters and Setters
                public Long getFaceId() {
                    return faceId;
                }

                public void setFaceId(Long faceId) {
                    this.faceId = faceId;
                }

                public String getName() {
                    return name;
                }

                public void setName(String name) {
                    this.name = name;
                }

                public Integer getEmbeddingDimension() {
                    return embeddingDimension;
                }

                public void setEmbeddingDimension(Integer embeddingDimension) {
                    this.embeddingDimension = embeddingDimension;
                }
            }
        }
    }

    public static class DeleteFaceResponse {
        private Boolean success;
        private String message;

        // Getters and Setters
        public Boolean getSuccess() {
            return success;
        }

        public void setSuccess(Boolean success) {
            this.success = success;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }
    }
}