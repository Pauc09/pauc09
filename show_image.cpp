#include <opencv2/opencv.hpp>
#include <iostream>

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Uso: ./show_image <ruta_imagen>\n";
        return 1;
    }

    cv::Mat image = cv::imread(argv[1]);
    if (image.empty()) {
        std::cerr << "Error: No se pudo cargar la imagen\n";
        return 1;
    }

    cv::imshow("Imagen cargada", image);
    cv::waitKey(0);
    cv::destroyAllWindows();
    return 0;
}
