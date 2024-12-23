import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class convertir {
    private JsonObject exchangeRates;

    public void loadExchangeRates(String jsonResponse) {
        JsonObject jsonObject = JsonParser.parseString(jsonResponse).getAsJsonObject();
        exchangeRates = jsonObject.getAsJsonObject("conversion_rates");
    }

    public double convert(String fromCurrency, String toCurrency, double amount) {
        if (exchangeRates == null || !exchangeRates.has(toCurrency)) {
            throw new IllegalArgumentException("Currency not supported!");
        }
        double rate = exchangeRates.get(toCurrency).getAsDouble();
        return amount * rate;
    }
    public void printAllExchangeRates() {
        if (exchangeRates == null) {
            System.out.println("No hay tasas de cambio cargadas.");
            return;
        }

        System.out.println("--- Tasas de Cambio ---");
        for (String currency : exchangeRates.keySet()) {
            double rate = exchangeRates.get(currency).getAsDouble();
            System.out.printf("%s: %.4f%n", currency, rate);
        }
    }
}
