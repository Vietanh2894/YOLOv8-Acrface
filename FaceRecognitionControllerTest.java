package com.example.facerecognition.controller;

import com.example.facerecognition.service.FaceRecognitionService;
import com.example.facerecognition.service.FaceRecognitionService.*;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Mono;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.anyDouble;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.when;

@WebFluxTest(FaceRecognitionController.class)
public class FaceRecognitionControllerTest {

    @Autowired
    private WebTestClient webTestClient;

    @MockBean
    private FaceRecognitionService faceService;

    @Test
    public void testHealthEndpoint() {
        HealthResponse healthResponse = new HealthResponse();
        healthResponse.setStatus("OK");

        when(faceService.checkHealth())
                .thenReturn(Mono.just(healthResponse));

        webTestClient.get()
                .uri("/api/v1/face/health")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.status").isEqualTo("OK");
    }

    @Test
    public void testRegisterFaceEndpoint() {
        FaceRegisterResponse registerResponse = new FaceRegisterResponse();
        registerResponse.setSuccess(true);
        registerResponse.setMessage("Face registered successfully");
        registerResponse.setFaceId(1L);

        when(faceService.registerFace(anyString(), anyString(), anyString()))
                .thenReturn(Mono.just(registerResponse));

        FaceRegisterRequest request = new FaceRegisterRequest();
        request.setName("Test User");
        request.setImage("base64imagedata");
        request.setDescription("Test description");

        webTestClient.post()
                .uri("/api/v1/face/register")
                .bodyValue(request)
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.success").isEqualTo(true)
                .jsonPath("$.message").isEqualTo("Face registered successfully")
                .jsonPath("$.face_id").isEqualTo(1);
    }

    @Test
    public void testRecognizeFaceEndpoint() {
        FaceRecognizeResponse recognizeResponse = new FaceRecognizeResponse();
        recognizeResponse.setSuccess(true);
        recognizeResponse.setMessage("Face recognized");
        recognizeResponse.setName("Test User");
        recognizeResponse.setFaceId(1L);
        recognizeResponse.setSimilarity(0.85);

        when(faceService.recognizeFace(anyString(), anyDouble()))
                .thenReturn(Mono.just(recognizeResponse));

        FaceRecognizeRequest request = new FaceRecognizeRequest();
        request.setImage("base64imagedata");
        request.setThreshold(0.6);

        webTestClient.post()
                .uri("/api/v1/face/recognize")
                .bodyValue(request)
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.success").isEqualTo(true)
                .jsonPath("$.message").isEqualTo("Face recognized")
                .jsonPath("$.name").isEqualTo("Test User")
                .jsonPath("$.face_id").isEqualTo(1)
                .jsonPath("$.similarity").isEqualTo(0.85);
    }

    @Test
    public void testCompareFacesEndpoint() {
        FaceCompareResponse compareResponse = new FaceCompareResponse();
        compareResponse.setSuccess(true);
        compareResponse.setMessage("Faces compared successfully");
        compareResponse.setSimilarity(0.92);
        compareResponse.setMatch(true);

        when(faceService.compareFaces(anyString(), anyString(), anyDouble()))
                .thenReturn(Mono.just(compareResponse));

        FaceCompareRequest request = new FaceCompareRequest();
        request.setImage1("base64imagedata1");
        request.setImage2("base64imagedata2");
        request.setThreshold(0.6);

        webTestClient.post()
                .uri("/api/v1/face/compare")
                .bodyValue(request)
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.success").isEqualTo(true)
                .jsonPath("$.message").isEqualTo("Faces compared successfully")
                .jsonPath("$.similarity").isEqualTo(0.92)
                .jsonPath("$.match").isEqualTo(true);
    }

    @Test
    public void testTestEndpoint() {
        webTestClient.get()
                .uri("/api/v1/face/test")
                .exchange()
                .expectStatus().isOk()
                .expectBody(String.class)
                .isEqualTo("Face Recognition Controller is working!");
    }
}