import java.util.Scanner;

public class GUI {
    private final API apiHandler = new API();
    private final convertir converter = new convertir();
    private boolean isLoaded = false;

    public void start() {
        Scanner scanner = new Scanner(System.in);
        String option;

        // Moneda base predeterminada
        String baseCurrency = "USD";

        System.out.println("***********************************");
        System.out.println("Bienvenido al Conversor de Monedas");
        System.out.println("Usando la moneda base predeterminada: " + baseCurrency);

        // Intentamos cargar las tasas de cambio al inicio
        loadExchangeRates(baseCurrency);

        do {
            System.out.println("\n--- Menú ---");
            System.out.println("1. Convertir moneda");
            System.out.println("2. Mostrar tasas de cambio disponibles");
            System.out.println("3. Cambiar moneda base (actual: " + baseCurrency + ")");
            System.out.println("4. Salir");
            System.out.print("Seleccione una opción: ");
            option = scanner.nextLine();

            switch (option) {
                case "1":
                    convertCurrency(scanner, baseCurrency);
                    break;
                case "2":
                    showExchangeRates();
                    break;
                case "3":
                    baseCurrency = changeBaseCurrency(scanner);
                    loadExchangeRates(baseCurrency);
                    break;
                case "4":
                    System.out.println("Gracias por usar el Conversor de Monedas. ¡Adiós!");
                    break;
                default:
                    System.out.println("Opción inválida. Intente nuevamente.");
            }
        } while (!option.equals("4"));
    }

    private void loadExchangeRates(String baseCurrency) {
        String jsonResponse = apiHandler.fetchExchangeRates(baseCurrency);
        if (jsonResponse == null) {
            System.out.println("Error al obtener las tasas de cambio. Verifique su conexión a Internet.");
            isLoaded = false;
        } else {
            try {
                converter.loadExchangeRates(jsonResponse);
                isLoaded = true;
                System.out.println("Tasas de cambio cargadas correctamente.");
            } catch (Exception e) {
                System.out.println("Error al procesar las tasas de cambio: " + e.getMessage());
                isLoaded = false;
            }
        }
    }

    private void convertCurrency(Scanner scanner, String baseCurrency) {
        if (!isLoaded) {
            System.out.println("No se han cargado las tasas de cambio. Intente nuevamente más tarde.");
            return;
        }

        System.out.print("Ingrese la cantidad a convertir desde " + baseCurrency + ": ");
        double amount = scanner.nextDouble();
        scanner.nextLine(); // Consumir nueva línea

        System.out.print("Ingrese la moneda de destino (por ejemplo, EUR): ");
        String targetCurrency = scanner.nextLine().toUpperCase();

        try {
            double result = converter.convert(baseCurrency, targetCurrency, amount);
            System.out.printf("Resultado: %.2f %s%n", result, targetCurrency);
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());
        }
    }

    private void showExchangeRates() {
        if (!isLoaded) {
            System.out.println("No se han cargado las tasas de cambio. Intente nuevamente más tarde.");
            return;
        }

        converter.printAllExchangeRates();
    }

    private String changeBaseCurrency(Scanner scanner) {
        System.out.print("Ingrese la nueva moneda base (por ejemplo, EUR): ");
        return scanner.nextLine().toUpperCase();
    }
}
