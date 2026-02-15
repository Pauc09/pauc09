#include <opencv2/opencv.hpp>
#include <iostream>
#include <cmath>

using namespace cv;
using namespace std;

void ejercicio1_rgb_a_hsv() {
    Mat img_bgr = imread("/home/paula/TallerOpenCV/imagenes/taller.jpg");
    
    if (img_bgr.empty()) {
        cout << "Error: No se pudo cargar la imagen" << endl;
        return;
    }
    
    int rows = img_bgr.rows;
    int cols = img_bgr.cols;
    
    Mat img_hsv(rows, cols, CV_8UC3);
    
    cout << "Convirtiendo RGB a HSV manualmente..." << endl;
    cout << "Procesando " << rows << "x" << cols << " pixeles" << endl;
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            Vec3b pixel_bgr = img_bgr.at<Vec3b>(i, j);
            
            // Obtener valores BGR y normalizar a [0,1]
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
    
    cout << "\n¡Ejercicio 1 completado!" << endl;
    cout << "\nConversion RGB -> HSV:" << endl;
    cout << "  H (Hue): Tono del color [0-180]" << endl;
    cout << "  S (Saturation): Saturacion [0-255]" << endl;
    cout << "  V (Value): Brillo [0-255]" << endl;
    
    // Mostrar ejemplo de un pixel
    Vec3b pixel_original = img_bgr.at<Vec3b>(rows/2, cols/2);
    Vec3b pixel_hsv = img_hsv.at<Vec3b>(rows/2, cols/2);
    
    cout << "\nEjemplo pixel central:" << endl;
    cout << "  BGR original: (" << (int)pixel_original[0] << ", " 
         << (int)pixel_original[1] << ", " << (int)pixel_original[2] << ")" << endl;
    cout << "  HSV convertido: (" << (int)pixel_hsv[0] << ", " 
         << (int)pixel_hsv[1] << ", " << (int)pixel_hsv[2] << ")" << endl;
    
    imshow("Original BGR", img_bgr);
    imshow("HSV (Manual)", img_hsv);
    waitKey(0);
    destroyAllWindows();
}

int main() {
    cout << "=== PUNTO 1: CONVERSION RGB -> HSV ===" << endl;
    ejercicio1_rgb_a_hsv();
    return 0;
}
