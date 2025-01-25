package org.example.API;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.Info.Book;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Api {
    private static final String BASE_URL = "https://gutendex.com/books/";

    public static Book[] searchBooksByTitle(String title) throws Exception {
        String url = BASE_URL + "?search=" + title;

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        ObjectMapper mapper = new ObjectMapper();
        // Mapea la respuesta JSON a un arreglo de libros
        return mapper.readValue(response.body(), Book[].class);
    }
}
