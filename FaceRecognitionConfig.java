package com.example.facerecognition.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;
import reactor.netty.resources.ConnectionProvider;

import java.time.Duration;

/**
 * Configuration cho Face Recognition Service
 */
@Configuration
public class FaceRecognitionConfig {

    @Value("${face.api.base-url:http://localhost:5000/api}")
    private String baseUrl;

    @Value("${face.api.timeout.connection:30}")
    private int connectionTimeout;

    @Value("${face.api.timeout.response:60}")
    private int responseTimeout;

    /**
     * WebClient cho Face Recognition API
     */
    @Bean("faceRecognitionWebClient")
    public WebClient faceRecognitionWebClient() {
        // Cấu hình Connection Provider
        ConnectionProvider provider = ConnectionProvider.builder("face-api")
                .maxConnections(10)
                .maxIdleTime(Duration.ofSeconds(20))
                .maxLifeTime(Duration.ofSeconds(60))
                .pendingAcquireTimeout(Duration.ofSeconds(60))
                .evictInBackground(Duration.ofSeconds(120))
                .build();

        // Cấu hình HTTP Client với timeout
        HttpClient httpClient = HttpClient.create(provider)
                .responseTimeout(Duration.ofSeconds(responseTimeout))
                .option(io.netty.channel.ChannelOption.CONNECT_TIMEOUT_MILLIS,
                        connectionTimeout * 1000);

        return WebClient.builder()
                .baseUrl(baseUrl)
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                .codecs(configurer -> {
                    configurer.defaultCodecs().maxInMemorySize(16 * 1024 * 1024); // 16MB
                })
                .build();
    }
}