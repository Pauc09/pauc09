#include <opencv2/opencv.hpp>
#include <iostream>
#include <cmath>

using namespace cv;
using namespace std;

void ejercicio2_modificar_saturacion() {
    Mat img_bgr = imread("../../imagenes/taller.jpg");
    
    if (img_bgr.empty()) {
        cout << "Error: No se pudo cargar la imagen" << endl;
        return;
    }
    
    int rows = img_bgr.rows;
    int cols = img_bgr.cols;
    
    Mat img_hsv(rows, cols, CV_8UC3);
    
    // TODO: Copiar código de conversión BGR→HSV aquí
    // Conversión BGR → HSV (del ejercicio 1)
    cout << "Convirtiendo BGR -> HSV..." << endl;
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            Vec3b pixel_bgr = img_bgr.at<Vec3b>(i, j);
            
            // Obtener valores BGR y normalizar
            double b = pixel_bgr[0] / 255.0;
            double g = pixel_bgr[1] / 255.0;
            double r = pixel_bgr[2] / 255.0;
            
            // Calcular Cmax, Cmin, Delta
            double cmax = max({r, g, b});
            double cmin = min({r, g, b});
            double delta = cmax - cmin;
            
            // Calcular Hue (H)
            double h = 0;
            if (delta != 0) {
                if (cmax == r) {
                    h = 60.0 * fmod(((g - b) / delta), 6.0);
                } else if (cmax == g) {
                    h = 60.0 * (((b - r) / delta) + 2.0);
                } else if (cmax == b) {
                    h = 60.0 * (((r - g) / delta) + 4.0);
                }
            }
            if (h < 0) h += 360.0;
            
            // H_opencv = H / 2 (OpenCV usa [0,180] en vez de [0,360])
            uchar h_opencv = (uchar)(h / 2.0);
            
            // Calcular Saturation (S)
            double s = (cmax == 0) ? 0 : (delta / cmax);
            uchar s_opencv = (uchar)(s * 255.0);
            
            // Calcular Value (V)
            uchar v_opencv = (uchar)(cmax * 255.0);
            
            // Asignar valores HSV al píxel
            img_hsv.at<Vec3b>(i, j) = Vec3b(h_opencv, s_opencv, v_opencv);
        }
    }
    
    cout << "Modificando saturacion..." << endl;
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            Vec3b pixel_hsv = img_hsv.at<Vec3b>(i, j);
            
            // PASO 1: Obtener valores H, S, V
            uchar h = pixel_hsv[0];
            uchar s = pixel_hsv[1];
            uchar v = pixel_hsv[2];
            
            // PASO 2: Multiplicar S por 1.5 (sin exceder 255)
            int s_nuevo = (int)(s * 1.5);
            if (s_nuevo > 255) s_nuevo = 255;
            
            // PASO 3: Asignar nuevos valores
            img_hsv.at<Vec3b>(i, j) = Vec3b(h, (uchar)s_nuevo, v);
        }
    }
    
    Mat img_resultado(rows, cols, CV_8UC3);
    
    // TODO: Implementar conversión HSV → BGR
    // Usa las fórmulas inversas explicadas en la teoría
    cout << "Convirtiendo HSV -> BGR..." << endl;
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            Vec3b pixel_hsv = img_hsv.at<Vec3b>(i, j);
            
            // Desnormalizar
            double h = pixel_hsv[0] * 2.0;
            double s = pixel_hsv[1] / 255.0;
            double v = pixel_hsv[2] / 255.0;
            
            // Calcular C, X, m
            double c = v * s;
            double x = c * (1.0 - fabs(fmod(h / 60.0, 2.0) - 1.0));
            double m = v - c;
            
            double r_prima, g_prima, b_prima;
            
            // Según el rango de H
            if (h >= 0 && h < 60) {
                r_prima = c; g_prima = x; b_prima = 0;
            } else if (h >= 60 && h < 120) {
                r_prima = x; g_prima = c; b_prima = 0;
            } else if (h >= 120 && h < 180) {
                r_prima = 0; g_prima = c; b_prima = x;
            } else if (h >= 180 && h < 240) {
                r_prima = 0; g_prima = x; b_prima = c;
            } else if (h >= 240 && h < 300) {
                r_prima = x; g_prima = 0; b_prima = c;
            } else {
                r_prima = c; g_prima = 0; b_prima = x;
            }
            
            // Convertir a [0,255]
            uchar b = (uchar)((b_prima + m) * 255.0);
            uchar g = (uchar)((g_prima + m) * 255.0);
            uchar r = (uchar)((r_prima + m) * 255.0);
            
            img_resultado.at<Vec3b>(i, j) = Vec3b(b, g, r);
        }
    }
    
    imshow("Original", img_bgr);
    imshow("Saturacion Aumentada", img_resultado);
    waitKey(0);
    destroyAllWindows();
}

int main() {
    cout << "=== PUNTO 2: MODIFICAR SATURACION ===" << endl;
    ejercicio2_modificar_saturacion();
    return 0;
}
