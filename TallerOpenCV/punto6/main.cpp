#include <opencv2/opencv.hpp>
#include <iostream>
#include <cmath>

using namespace cv;
using namespace std;

void ejercicio6_gamma(double gamma = 1.5) {
    Mat img_bgr = imread("/home/paula/TallerOpenCV/imagenes/taller.jpg");
    if (img_bgr.empty()) {
        cout << "Error: No se pudo cargar la imagen" << endl;
        return;
    }
    
    int rows = img_bgr.rows;
    int cols = img_bgr.cols;
    
    cout << "Aplicando correccion gamma = " << gamma << endl;
    cout << "  gamma < 1: Aclara la imagen" << endl;
    cout << "  gamma = 1: Sin cambio" << endl;
    cout << "  gamma > 1: Oscurece la imagen" << endl;
    
    // TODO: PASO 1 - Crear tabla de lookup (para eficiencia)
    // Pre-calcular la transformación para todos los valores 0-255
    uchar tabla_lookup[256];
    
    cout << "\nCreando tabla de lookup..." << endl;
    
    for (int i = 0; i < 256; i++) {
        // Formula: pixel_out = 255 × (pixel_in / 255)^gamma
        double normalizado = i / 255.0;
        double resultado = pow(normalizado, gamma);
        tabla_lookup[i] = (uchar)(resultado * 255.0);
    }
    
    // Mostrar algunos valores de ejemplo
    cout << "Ejemplos de la tabla:" << endl;
    cout << "  pixel_in=0   -> pixel_out=" << (int)tabla_lookup[0] << endl;
    cout << "  pixel_in=64  -> pixel_out=" << (int)tabla_lookup[64] << endl;
    cout << "  pixel_in=128 -> pixel_out=" << (int)tabla_lookup[128] << endl;
    cout << "  pixel_in=192 -> pixel_out=" << (int)tabla_lookup[192] << endl;
    cout << "  pixel_in=255 -> pixel_out=" << (int)tabla_lookup[255] << endl;
    
    // TODO: PASO 2 - Aplicar transformación a cada píxel
    Mat img_resultado(rows, cols, CV_8UC3);
    
    cout << "\nAplicando correccion a cada pixel..." << endl;
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            Vec3b pixel = img_bgr.at<Vec3b>(i, j);
            
            // Aplicar tabla de lookup a cada canal
            uchar b_nuevo = tabla_lookup[pixel[0]];
            uchar g_nuevo = tabla_lookup[pixel[1]];
            uchar r_nuevo = tabla_lookup[pixel[2]];
            
            img_resultado.at<Vec3b>(i, j) = Vec3b(b_nuevo, g_nuevo, r_nuevo);
        }
    }
    
    cout << "\n¡Ejercicio 6 completado!" << endl;
    
    imshow("Original", img_bgr);
    imshow("Gamma = " + to_string(gamma), img_resultado);
    waitKey(0);
    destroyAllWindows();
}

int main() {
    cout << "=== PUNTO 6: CORRECCION GAMMA ===" << endl;
    cout << "\nIngrese el valor de gamma (recomendado 0.5 - 2.5): ";
    double gamma;
    cin >> gamma;
    
    if (gamma <= 0 || gamma > 5) {
        cout << "Valor invalido. Usando gamma=1.5 por defecto" << endl;
        gamma = 1.5;
    }
    
    ejercicio6_gamma(gamma);
    return 0;
}
