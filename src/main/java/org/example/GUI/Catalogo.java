package org.example.GUI;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.Info.Author;
import org.example.Info.Book;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Catalogo {
    private List<Book> books;
    private List<Author> authors;

    public Catalogo() {
        this.books = new ArrayList<>();
        this.authors = new ArrayList<>();
    }

    // Método para agregar un libro
    public void agregarLibro(Scanner scanner) {
        System.out.print("Ingrese el título del libro: ");
        String title = scanner.nextLine();

        System.out.print("Ingrese los idiomas del libro separados por comas: ");
        String[] languagesInput = scanner.nextLine().split(",");
        for (int i = 0; i < languagesInput.length; i++) {
            languagesInput[i] = languagesInput[i].trim();
        }

        // Crear el libro
        Book book = new Book();
        book.setTitle(title);
        book.setLanguages(languagesInput);
        books.add(book);

        System.out.println("Libro agregado exitosamente: " + book.getTitle());
    }

    // Método para consultar libros por título
    public static void consultarLibros(Scanner scanner) {
        System.out.print("Ingrese el título del libro a buscar (parcial o completo): ");
        String query = scanner.nextLine();

        try {
            HttpClient client = HttpClient.newBuilder()
                    .followRedirects(HttpClient.Redirect.NORMAL) // Seguir redirecciones
                    .build();

            String encodedQuery = URLEncoder.encode(query, StandardCharsets.UTF_8).replace("+", "%20");
            String url = "https://gutendex.com/books?search=" + encodedQuery;

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            // Imprimir el cuerpo de la respuesta
            String responseBody = response.body();
            System.out.println("Cuerpo de la respuesta: " + responseBody);

            if (response.statusCode() == 200 && response.body() != null && !response.body().isEmpty()) {
                ObjectMapper mapper = new ObjectMapper();
                JsonNode jsonNode = mapper.readTree(response.body());
                JsonNode results = jsonNode.get("results");

                if (results != null && results.isArray() && results.size() > 0) {
                    System.out.println("Resultados encontrados:");
                    for (JsonNode bookNode : results) {
                        String title = bookNode.get("title").asText();
                        System.out.println("Título: " + title);
                    }
                } else {
                    System.out.println("No se encontraron libros con el título: " + query);
                }
            } else {
                System.out.println("La API no devolvió resultados. Código de estado: " + response.statusCode());
            }
        } catch (Exception e) {
            System.err.println("Error al consultar la API: " + e.getMessage());
        }
    }



    // Método para listar libros por idioma
    public void listarLibrosPorIdiomas(Scanner scanner) {
        System.out.print("Ingrese el idioma para buscar libros (ejemplo: en, es, fr): ");
        String idioma = scanner.nextLine().trim();

        try {
            HttpClient client = HttpClient.newHttpClient();
            String url = "https://gutendex.com/books?languages=" + idioma;
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            String responseBody = response.body();

            ObjectMapper mapper = new ObjectMapper();
            JsonNode jsonNode = mapper.readTree(responseBody);
            JsonNode results = jsonNode.get("results");

            if (results != null && results.isArray()) {
                System.out.println("Libros disponibles en el idioma '" + idioma + "':");
                for (JsonNode bookNode : results) {
                    String title = bookNode.get("title").asText();
                    System.out.println("Título: " + title);
                }
            } else {
                System.out.println("No se encontraron libros en ese idioma.");
            }
        } catch (Exception e) {
            System.err.println("Error al consultar la API: " + e.getMessage());
        }
    }

    // Método para consultar y agregar autores
    public void consultarYAgregarAutores(Scanner scanner) {
        System.out.print("Ingrese el nombre del autor o palabras clave: ");
        String query = scanner.nextLine();

        try {
            HttpClient client = HttpClient.newBuilder()
                    .followRedirects(HttpClient.Redirect.NORMAL)
                    .build();

            // Codificar la consulta para que funcione con la API
            String encodedQuery = URLEncoder.encode(query, StandardCharsets.UTF_8).replace("+", "%20");
            String url = "https://gutendex.com/books?search=" + encodedQuery;

            // Mostrar la URL generada para depuración
            System.out.println("URL generada: " + url);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200 && response.body() != null && !response.body().isEmpty()) {
                ObjectMapper mapper = new ObjectMapper();
                JsonNode jsonNode = mapper.readTree(response.body());
                JsonNode results = jsonNode.get("results");

                if (results != null && results.isArray() && results.size() > 0) {
                    System.out.println("Autores encontrados:");
                    for (JsonNode bookNode : results) {
                        JsonNode authorsNode = bookNode.get("authors");
                        if (authorsNode != null && authorsNode.isArray()) {
                            for (JsonNode authorNode : authorsNode) {
                                String authorName = authorNode.get("name").asText();
                                Integer birthYear = authorNode.has("birth_year") && !authorNode.get("birth_year").isNull()
                                        ? authorNode.get("birth_year").asInt()
                                        : null;
                                Integer deathYear = authorNode.has("death_year") && !authorNode.get("death_year").isNull()
                                        ? authorNode.get("death_year").asInt()
                                        : null;

                                // Mostrar la información del autor
                                System.out.printf("Nombre: %s, Año de nacimiento: %s, Año de fallecimiento: %s%n",
                                        authorName,
                                        birthYear != null ? birthYear : "Desconocido",
                                        deathYear != null ? deathYear : "Desconocido");

                                // Agregar a la lista local si no existe
                                if (authors.stream().noneMatch(a -> a.getName().equalsIgnoreCase(authorName))) {
                                    authors.add(new Author(authorName, birthYear, deathYear));
                                }
                            }
                        }
                    }
                } else {
                    System.out.println("No se encontraron autores relacionados con esa búsqueda.");
                }
            } else {
                System.out.println("La API no devolvió resultados. Código de estado: " + response.statusCode());
            }
        } catch (Exception e) {
            System.err.println("Error al consultar la API: " + e.getMessage());
        }
    }


    // Método para consultar autores por año
    public void consultarAutoresPorAnio(Scanner scanner) {
        System.out.println("Seleccione el tipo de búsqueda:");
        System.out.println("1. Por año de nacimiento");
        System.out.println("2. Por año de fallecimiento");
        System.out.print("Ingrese su elección: ");
        int opcion = scanner.nextInt();
        scanner.nextLine(); // Consumir el salto de línea

        System.out.print("Ingrese el año: ");
        int anio = scanner.nextInt();
        scanner.nextLine(); // Consumir el salto de línea

        boolean encontrado = false;

        if (opcion == 1) {
            System.out.println("Autores nacidos en el año " + anio + ":");
            for (Author author : authors) {
                if (author.getBirthYear() != null && author.getBirthYear().equals(anio)) {
                    System.out.println(author);
                    encontrado = true;
                }
            }
        } else if (opcion == 2) {
            System.out.println("Autores fallecidos en el año " + anio + ":");
            for (Author author : authors) {
                if (author.getDeathYear() != null && author.getDeathYear().equals(anio)) {
                    System.out.println(author);
                    encontrado = true;
                }
            }
        } else {
            System.out.println("Opción no válida.");
        }

        if (!encontrado) {
            System.out.println("No se encontraron autores para el año indicado.");
        }
    }

    // Método para mostrar todos los autores
    public void mostrarAutores() {
        if (authors.isEmpty()) {
            System.out.println("No hay autores en el catálogo.");
        } else {
            System.out.println("Autores en el catálogo:");
            for (Author author : authors) {
                System.out.println(author);
            }
        }
    }
}
