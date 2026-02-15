#include <opencv2/opencv.hpp>
#include <iostream>
#include <cmath>

using namespace cv;
using namespace std;

int main() {
    Mat img = imread("/home/paula/TallerOpenCV/imagenes/taller.jpg");
    if (img.empty()) {
        cout << "Error al cargar imagen" << endl;
        return -1;
    }
    
    int rows = img.rows;
    int cols = img.cols;
    
    double cx = cols / 2.0;
    double cy = rows / 2.0;
    double d_max = sqrt(cx * cx + cy * cy);
    
    Mat img_vignette = img.clone();
    
    cout << "Creando viñeteo artificial..." << endl;
    
    // CREAR viñeteo (oscurecer esquinas)
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            Vec3b pixel = img.at<Vec3b>(i, j);
            
            double dx = j - cx;
            double dy = i - cy;
            double d = sqrt(dx * dx + dy * dy);
            double d_norm = d / d_max;
            
            // Factor de oscurecimiento: más lejos del centro = más oscuro
            // Oscurecimiento = 1 - k * d_norm²
            double oscurecimiento = 1.0 - 0.5 * d_norm * d_norm;
            
            int b = (int)(pixel[0] * oscurecimiento);
            int g = (int)(pixel[1] * oscurecimiento);
            int r = (int)(pixel[2] * oscurecimiento);
            
            img_vignette.at<Vec3b>(i, j) = Vec3b(b, g, r);
        }
    }
    
    string output = "/home/paula/TallerOpenCV/imagenes/taller_vignette.jpg";
    imwrite(output, img_vignette);
    
    cout << "Imagen con viñeteo guardada: " << output << endl;
    
    imshow("Original", img);
    imshow("Con Viñeteo Artificial", img_vignette);
    waitKey(0);
    
    return 0;
}
