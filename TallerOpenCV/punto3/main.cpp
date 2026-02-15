#include <opencv2/opencv.hpp>
#include <iostream>
#include <cmath>
#include <vector>
#include <cstdlib>
#include <ctime>

using namespace cv;
using namespace std;

struct Pixel {
    double r, g, b;
    Pixel() : r(0), g(0), b(0) {}
    Pixel(double r_, double g_, double b_) : r(r_), g(g_), b(b_) {}
};

double distancia_euclidiana(const Pixel& p1, const Pixel& p2) {
    // TODO: Implementar
    double dr = p1.r - p2.r;
    double dg = p1.g - p2.g;
    double db = p1.b - p2.b;
    return sqrt(dr*dr + dg*dg + db*db);
}

void ejercicio3_kmeans_manual(int K = 5) {
    Mat img_bgr = imread("/home/paula/TallerOpenCV/imagenes/taller.jpg");
    if (img_bgr.empty()) {
        cout << "Error: No se pudo cargar la imagen" << endl;
        return;
    }
    
    // Redimensionar para acelerar
    Mat img_small;
    resize(img_bgr, img_small, Size(160, 120));
    
    int rows = img_small.rows;
    int cols = img_small.cols;
    int total_pixels = rows * cols;
    
    cout << "Procesando " << total_pixels << " píxeles con K=" << K << endl;
    
    // TODO: PASO 1 - Crear array de píxeles
    // Almacenar todos los píxeles en un vector
    vector<Pixel> pixels;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            Vec3b bgr = img_small.at<Vec3b>(i, j);
            pixels.push_back(Pixel(bgr[2], bgr[1], bgr[0]));  // BGR -> RGB
        }
    }
    
    // TODO: PASO 2 - Inicializar K centroides aleatorios
    vector<Pixel> centroides;
    srand(time(NULL));
    for (int k = 0; k < K; k++) {
        int idx = rand() % total_pixels;
        centroides.push_back(pixels[idx]);
    }
    
    // TODO: PASO 3 - Array para almacenar asignaciones
    // Cada píxel se asigna a un cluster [0, K-1]
    vector<int> asignaciones(total_pixels);
    
    // TODO: PASO 4 - Iterar K-Means
    int max_iteraciones = 20;
    for (int iter = 0; iter < max_iteraciones; iter++) {
        cout << "Iteración " << (iter + 1) << "/" << max_iteraciones << endl;
        
        // PASO 4a: Asignar cada píxel al centroide más cercano
        for (int p = 0; p < total_pixels; p++) {
            double min_dist = distancia_euclidiana(pixels[p], centroides[0]);
            int min_idx = 0;
            
            for (int k = 1; k < K; k++) {
                double dist = distancia_euclidiana(pixels[p], centroides[k]);
                if (dist < min_dist) {
                    min_dist = dist;
                    min_idx = k;
                }
            }
            asignaciones[p] = min_idx;
        }
        
        // PASO 4b: Recalcular centroides
        // Crear arrays para sumar RGB de cada cluster
        vector<Pixel> suma_centroides(K);
        vector<int> contadores(K, 0);
        
        for (int p = 0; p < total_pixels; p++) {
            int cluster = asignaciones[p];
            suma_centroides[cluster].r += pixels[p].r;
            suma_centroides[cluster].g += pixels[p].g;
            suma_centroides[cluster].b += pixels[p].b;
            contadores[cluster]++;
        }
        
        // Calcular promedio para cada centroide
        for (int k = 0; k < K; k++) {
            if (contadores[k] > 0) {
                centroides[k].r = suma_centroides[k].r / contadores[k];
                centroides[k].g = suma_centroides[k].g / contadores[k];
                centroides[k].b = suma_centroides[k].b / contadores[k];
            }
        }
    }
    
    // TODO: PASO 5 - Crear imagen cuantizada
    // Reemplazar cada píxel por el color de su centroide
    Mat img_quantized(rows, cols, CV_8UC3);
    int idx = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            int cluster = asignaciones[idx++];
            uchar r = (uchar)centroides[cluster].r;
            uchar g = (uchar)centroides[cluster].g;
            uchar b = (uchar)centroides[cluster].b;
            img_quantized.at<Vec3b>(i, j) = Vec3b(b, g, r);  // RGB -> BGR
        }
    }
    
    // TODO: PASO 6 - Crear paleta de colores
    Mat paleta(50, K * 50, CV_8UC3);
    for (int k = 0; k < K; k++) {
        uchar r = (uchar)centroides[k].r;
        uchar g = (uchar)centroides[k].g;
        uchar b = (uchar)centroides[k].b;
        rectangle(paleta, Point(k * 50, 0), Point((k + 1) * 50, 50), 
                  Scalar(b, g, r), -1);
    }
    
    cout << "\n¡Ejercicio 3 completado!" << endl;
    cout << "Centroides finales:" << endl;
    for (int k = 0; k < K; k++) {
        cout << "  Cluster " << k << ": RGB(" 
             << (int)centroides[k].r << ", " 
             << (int)centroides[k].g << ", " 
             << (int)centroides[k].b << ")" << endl;
    }
    
    imshow("Original", img_small);
    imshow("K-Means Manual K=" + to_string(K), img_quantized);
    imshow("Paleta", paleta);
    waitKey(0);
    destroyAllWindows();
}

int main() {
    cout << "=== PUNTO 3: K-MEANS MANUAL ===" << endl;
    cout << "\nIngrese el valor de K (numero de colores): ";
    int k;
    cin >> k;
    
    if (k < 2 || k > 20) {
        cout << "Usando K=5 por defecto" << endl;
        k = 5;
    }
    
    ejercicio3_kmeans_manual(k);
    return 0;
}
