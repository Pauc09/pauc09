#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <cmath>

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Uso: ./programa <ruta_imagen>\n";
        return 1;
    }

    std::string ruta = argv[1];

    // Cargar imagen en BGR
    cv::Mat img = cv::imread(ruta, cv::IMREAD_COLOR);
    if (img.empty()) {
        std::cerr << "Error: No se pudo cargar la imagen: " << ruta << "\n";
        return 1;
    }

    std::cout << "Imagen cargada: " << img.cols << "x" << img.rows << " pixeles\n\n";

    // ---- MENU: escoger escala ----
    std::cout << "============================================\n";
    std::cout << "       MENU DE ESCALADO DE IMAGEN\n";
    std::cout << "============================================\n";
    std::cout << "1) Escala 0.5x (reducir a la mitad)\n";
    std::cout << "2) Escala 1.0x (tamaño original)\n";
    std::cout << "3) Escala 2.0x (duplicar tamaño)\n";
    std::cout << "4) Escala personalizada\n";
    std::cout << "============================================\n";
    std::cout << "Selecciona una opcion: ";

    int op = 0;
    std::cin >> op;

    double factor = 1.0;  // DECLARACIÓN DE LA VARIABLE factor
    
    if (op == 1) {
        factor = 0.5;
        std::cout << "\n✓ Escalando a 0.5x (50%)\n";
    }
    else if (op == 2) {
        factor = 1.0;
        std::cout << "\n✓ Manteniendo tamaño original (100%)\n";
    }
    else if (op == 3) {
        factor = 2.0;
        std::cout << "\n✓ Escalando a 2.0x (200%)\n";
    }
    else if (op == 4) {
        std::cout << "Ingresa el factor de escala (ej: 0.75, 1.5, 3.0): ";
        std::cin >> factor;
        if (factor <= 0) {
            std::cerr << "Error: Factor invalido.\n";
            return 1;
        }
        std::cout << "\n✓ Escalando a " << factor << "x\n";
    }
    else {
        std::cerr << "Error: Opcion invalida.\n";
        return 1;
    }

    // Función para limitar valores entre 0-255
    auto clamp255 = [](int v) -> unsigned char {
        if (v < 0) return 0;
        if (v > 255) return 255;
        return (unsigned char)v;
    };

    // ---- ESCALADO MANUAL PIXEL POR PIXEL (Nearest Neighbor) ----
    int w = img.cols, h = img.rows;
    int newW = std::max(1, (int)std::lround(w * factor));
    int newH = std::max(1, (int)std::lround(h * factor));

    std::cout << "\nProcesando escalado: " << w << "x" << h 
              << " -> " << newW << "x" << newH << "\n";

    cv::Mat escalada(newH, newW, CV_8UC3);

    // ESCALADO MANUAL
    for (int y = 0; y < newH; y++) {
        int srcY = (int)std::floor(y / factor);
        if (srcY < 0) srcY = 0;
        if (srcY >= h) srcY = h - 1;

        for (int x = 0; x < newW; x++) {
            int srcX = (int)std::floor(x / factor);
            if (srcX < 0) srcX = 0;
            if (srcX >= w) srcX = w - 1;

            escalada.at<cv::Vec3b>(y, x) = img.at<cv::Vec3b>(srcY, srcX);
        }
    }

    std::cout << "✓ Escalado completado\n\n";

    // ---- CONVERSIONES MANUALES PIXEL POR PIXEL ----
    std::cout << "Convirtiendo a diferentes espacios de color...\n";

    // 1) ESCALA DE GRISES
    cv::Mat grises(newH, newW, CV_8UC1);

    // 2) HSV 
    cv::Mat hsvImg(newH, newW, CV_8UC3);

    // 3) YUV
    cv::Mat yuvImg(newH, newW, CV_8UC3);

    // PROCESAMIENTO PIXEL POR PIXEL
    for (int y = 0; y < newH; y++) {
        for (int x = 0; x < newW; x++) {
            cv::Vec3b bgr = escalada.at<cv::Vec3b>(y, x);
            int B = bgr[0];
            int G = bgr[1];
            int R = bgr[2];

            // ===== 1. CONVERSION A GRISES MANUAL =====
            // Fórmula de luminancia: Y = 0.299R + 0.587G + 0.114B
            int gray = (int)std::lround(0.299 * R + 0.587 * G + 0.114 * B);
            grises.at<unsigned char>(y, x) = clamp255(gray);

            // ===== 2. CONVERSION A HSV MANUAL =====
            double r = R / 255.0;
            double g = G / 255.0;
            double b = B / 255.0;

            double cmax = std::max(r, std::max(g, b));
            double cmin = std::min(r, std::min(g, b));
            double delta = cmax - cmin;

            double H = 0.0;   // Hue: 0..360
            double S = 0.0;   // Saturation: 0..1
            double V = cmax;  // Value: 0..1

            // Calcular Hue
            if (delta == 0.0) {
                H = 0.0;
            } else if (cmax == r) {
                H = 60.0 * std::fmod(((g - b) / delta), 6.0);
            } else if (cmax == g) {
                H = 60.0 * (((b - r) / delta) + 2.0);
            } else { // cmax == b
                H = 60.0 * (((r - g) / delta) + 4.0);
            }
            if (H < 0.0) H += 360.0;

            // Calcular Saturation
            if (cmax != 0.0) S = delta / cmax;
            else S = 0.0;

            // Convertir a rango OpenCV: H:0..179, S:0..255, V:0..255
            int Hcv = (int)std::lround(H / 2.0);
            int Scv = (int)std::lround(S * 255.0);
            int Vcv = (int)std::lround(V * 255.0);

            hsvImg.at<cv::Vec3b>(y, x) = cv::Vec3b(clamp255(Hcv), clamp255(Scv), clamp255(Vcv));

            // ===== 3. CONVERSION A YUV MANUAL (BT.601) =====
            // Y  =  0.299R + 0.587G + 0.114B
            // U  = -0.168736R - 0.331264G + 0.5B + 128
            // V  =  0.5R - 0.418688G - 0.081312B + 128
            int Y = (int)std::lround(0.299 * R + 0.587 * G + 0.114 * B);
            int U = (int)std::lround(-0.168736 * R - 0.331264 * G + 0.5 * B + 128);
            int Vv = (int)std::lround(0.5 * R - 0.418688 * G - 0.081312 * B + 128);

            yuvImg.at<cv::Vec3b>(y, x) = cv::Vec3b(clamp255(Y), clamp255(U), clamp255(Vv));
        }
    }

    std::cout << "✓ Conversiones completadas\n\n";

    // ---- GUARDAR IMAGENES ----
    std::cout << "============================================\n";
    std::cout << "         GUARDANDO IMAGENES\n";
    std::cout << "============================================\n";

    cv::imwrite("escalada.png", escalada);
    std::cout << "✓ escalada.png guardada\n";

    cv::imwrite("grises.png", grises);
    std::cout << "✓ grises.png guardada\n";

    cv::imwrite("hsv.png", hsvImg);
    std::cout << "✓ hsv.png guardada\n";

    cv::imwrite("yuv.png", yuvImg);
    std::cout << "✓ yuv.png guardada\n";

    std::cout << "============================================\n";
    std::cout << "Todas las imagenes guardadas en el directorio actual\n";
    std::cout << "============================================\n\n";

    // Mostrar las imágenes
    std::cout << "Presiona cualquier tecla en las ventanas para cerrar...\n";
    
    cv::imshow("1. Original (BGR)", img);
    cv::imshow("2. Escalada (BGR)", escalada);
    cv::imshow("3. Escala de Grises", grises);
    cv::imshow("4. HSV", hsvImg);
    cv::imshow("5. YUV", yuvImg);

    cv::waitKey(0);
    cv::destroyAllWindows();
    
    return 0;
}
