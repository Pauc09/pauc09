#include <opencv2/opencv.hpp>
#include <iostream>
#include <algorithm>

using namespace cv;
using namespace std;

void ejercicio4_gray_world() {
    Mat img_bgr = imread("/home/paula/TallerOpenCV/imagenes/taller.jpg");
    if (img_bgr.empty()) {
        cout << "Error: No se pudo cargar la imagen" << endl;
        return;
    }
    
    int rows = img_bgr.rows;
    int cols = img_bgr.cols;
    int total_pixels = rows * cols;
    
    cout << "Aplicando Gray World a imagen de " << rows << "x" << cols << endl;
    
    // TODO: PASO 1 - Calcular suma de cada canal
    long long suma_b = 0;
    long long suma_g = 0;
    long long suma_r = 0;
    
    cout << "Calculando promedios de cada canal..." << endl;
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            Vec3b pixel = img_bgr.at<Vec3b>(i, j);
            suma_b += pixel[0];
            suma_g += pixel[1];
            suma_r += pixel[2];
        }
    }
    
    // TODO: PASO 2 - Calcular promedios
    double avg_b = (double)suma_b / total_pixels;
    double avg_g = (double)suma_g / total_pixels;
    double avg_r = (double)suma_r / total_pixels;
    
    cout << "Promedio B: " << avg_b << endl;
    cout << "Promedio G: " << avg_g << endl;
    cout << "Promedio R: " << avg_r << endl;
    
    // TODO: PASO 3 - Calcular promedio gris
    double gray_avg = (avg_r + avg_g + avg_b) / 3.0;
    
    cout << "Promedio gris: " << gray_avg << endl;
    
    // TODO: PASO 4 - Calcular factores de escala
    double scale_b = gray_avg / avg_b;
    double scale_g = gray_avg / avg_g;
    double scale_r = gray_avg / avg_r;
    
    cout << "Factor de escala B: " << scale_b << endl;
    cout << "Factor de escala G: " << scale_g << endl;
    cout << "Factor de escala R: " << scale_r << endl;
    
    // TODO: PASO 5 - Crear imagen corregida
    Mat img_resultado(rows, cols, CV_8UC3);
    
    cout << "Aplicando correccion..." << endl;
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            Vec3b pixel = img_bgr.at<Vec3b>(i, j);
            
            // Aplicar a cada píxel: R_nuevo = min(R_viejo × scale_R, 255)
            int b_nuevo = (int)(pixel[0] * scale_b);
            int g_nuevo = (int)(pixel[1] * scale_g);
            int r_nuevo = (int)(pixel[2] * scale_r);
            
            // Asegurar que no exceda 255
            if (b_nuevo > 255) b_nuevo = 255;
            if (g_nuevo > 255) g_nuevo = 255;
            if (r_nuevo > 255) r_nuevo = 255;
            
            img_resultado.at<Vec3b>(i, j) = Vec3b(b_nuevo, g_nuevo, r_nuevo);
        }
    }
    
    cout << "\n¡Ejercicio 4 completado!" << endl;
    cout << "\nGray World corrige el balance de blancos asumiendo que" << endl;
    cout << "el promedio de la escena deberia ser gris neutro." << endl;
    
    imshow("Original", img_bgr);
    imshow("Gray World", img_resultado);
    waitKey(0);
    destroyAllWindows();
}

int main() {
    cout << "=== PUNTO 4: GRAY WORLD (CONSTANCIA DE COLOR) ===" << endl;
    ejercicio4_gray_world();
    return 0;
}
