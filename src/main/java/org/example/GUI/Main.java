package org.example.GUI;


import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Catalogo catalogo = new Catalogo();
        boolean running = true;

        while (running) {
            System.out.println("\n--- Catálogo de Libros ---");
            System.out.println("1. Agregar libro");
            System.out.println("2. Consultar libros");
            System.out.println("3. Consultar autores y agregarlos");
            System.out.println("4. Listar libros por idioma");
            System.out.println("5. Consultar autores por año");
            System.out.println("6. Mostrar todos los autores");
            System.out.println("7. Salir");
            System.out.print("Elige una opción: ");

            int choice = scanner.nextInt();
            scanner.nextLine(); // Consumir el salto de línea

            switch (choice) {
                case 1:
                    catalogo.agregarLibro(scanner);
                    break;
                case 2:
                    catalogo.consultarLibros(scanner);
                    break;
                case 3:
                    catalogo.consultarYAgregarAutores(scanner);
                    break;
                case 4:
                    catalogo.listarLibrosPorIdiomas(scanner);
                    break;
                case 5:
                    catalogo.consultarAutoresPorAnio(scanner);
                    break;
                case 6:
                    catalogo.mostrarAutores();
                    break;
                case 7:
                    running = false;
                    System.out.println("Saliendo del programa...");
                    break;
                default:
                    System.out.println("Opción no válida.");
            }
        }

        scanner.close();
    }
}
