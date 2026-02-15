#include <opencv2/opencv.hpp>
#include <iostream>
#include <cmath>

using namespace cv;
using namespace std;

void ejercicio7_vignette(double k = 0.4) {
    Mat img_bgr = imread("/home/paula/TallerOpenCV/imagenes/taller.jpg");
    if (img_bgr.empty()) {
        cout << "Error: No se pudo cargar la imagen" << endl;
        return;
    }
    
    int rows = img_bgr.rows;
    int cols = img_bgr.cols;
    
    cout << "Aplicando correccion de viñeteo con k = " << k << endl;
    
    // PASO 1 - Calcular centro de la imagen
    double cx = cols / 2.0;
    double cy = rows / 2.0;
    
    cout << "Centro: (" << cx << ", " << cy << ")" << endl;
    
    // PASO 2 - Calcular distancia máxima
    double d_max = sqrt(cx * cx + cy * cy);
    
    cout << "Distancia maxima: " << d_max << endl;
    
    // PASO 3 - Aplicar corrección
    Mat img_resultado = img_bgr.clone();
    
    cout << "Aplicando correccion..." << endl;
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            Vec3b pixel = img_bgr.at<Vec3b>(i, j);
            
            // Calcular distancia al centro
            double dx = j - cx;
            double dy = i - cy;
            double d = sqrt(dx * dx + dy * dy);
            
            // Distancia normalizada
            double r = d / d_max;
            
            // Factor de corrección más suave
            // factor = 1 + k * r²
            double factor = 1.0 + k * r * r;
            
            // Aplicar factor
            int b_nuevo = (int)(pixel[0] * factor);
            int g_nuevo = (int)(pixel[1] * factor);
            int r_nuevo = (int)(pixel[2] * factor);
            
            // Limitar a 255
            if (b_nuevo > 255) b_nuevo = 255;
            if (g_nuevo > 255) g_nuevo = 255;
            if (r_nuevo > 255) r_nuevo = 255;
            
            img_resultado.at<Vec3b>(i, j) = Vec3b(b_nuevo, g_nuevo, r_nuevo);
        }
    }
    
    cout << "\n¡Ejercicio 7 completado!" << endl;
    
    imshow("Original", img_bgr);
    imshow("Viñeteo Corregido k=" + to_string(k), img_resultado);
    waitKey(0);
    destroyAllWindows();
}

int main() {
    cout << "=== PUNTO 7: CORRECCION DE VIÑETEO ===" << endl;
    cout << "\nIngrese k (0.3-0.8): ";
    double k;
    cin >> k;
    
    if (k < 0 || k > 2) {
        cout << "Usando k=0.5 por defecto" << endl;
        k = 0.5;
    }
    
    ejercicio7_vignette(k);
    return 0;
}
