import java.net.http.*;
import java.net.URI;

public class API {
    private static final String API_KEY = "7fd11cd495201239c5feb50b";

    public String fetchExchangeRates(String baseCurrency) {
        String apiUrl = "https://v6.exchangerate-api.com/v6/" + API_KEY + "/latest/" + baseCurrency;

        try {
            HttpClient client = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(apiUrl))
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200) {
                return response.body();
            } else {
                System.out.println("Error: No se pudo obtener datos de la API. Código de estado: " + response.statusCode());
            }
        } catch (Exception e) {
            System.out.println("Error al realizar la solicitud a la API: " + e.getMessage());
        }

        return null;
    }
}
