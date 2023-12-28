# Streamread: anOCR Processor for Scanned Books

This project is a Streamlit-based application designed to perform Optical Character Recognition (OCR) on scanned book pages. It allows users to upload images of book pages, adjust preprocessing settings, and then extract text using OCR. The project aims to provide an easy-to-use interface for digitizing text from physical rare books that are not available on common e-book or audio book platforms.

## Features

- Upload multiple images of pages.
- Adjust preprocessing settings such as Gaussian blur and Otsu thresholding.
- Split page processing for two-page layouts.
- Download extracted text in `.txt` format.
- Preview images with adjustable split lines before OCR.
- Progress bar to indicate OCR process status.

## Installation

To run this project, you need to have Python installed on your machine. The project is built using Streamlit, along with other libraries like OpenCV, NumPy, and Pytesseract.

1. **Clone the Repository**

git clone https://github.com/guillaumeisobar/streamread.git
cd ocr-processor-for-scanned-books

2. **Install Required Libraries**

streamlit
opencv-python
pytesseract
Pillow
numpy

3. **Run the Application**

streamlit run app.py

## Usage

After starting the application, navigate to `http://localhost:8501` in your web browser. You can then use the application to upload scanned book pages and perform OCR to extract the text.

1. **Upload Images**: Use the file uploader to select and upload the scanned images of book pages.
2. **Adjust Settings**: Use the sliders in the sidebar to adjust preprocessing settings like scale factor, blur kernel size, and Otsu threshold value.
3. **Set Split Lines**: If you have two-page layouts, adjust the split lines to separate left and right pages.
4. **Start OCR**: Click on 'Start OCR Process' to begin text extraction.
5. **Download Results**: After the OCR process completes, you can download the extracted text.

## Contributing

Contributions to the project are welcome! If you have suggestions or improvements, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web application framework.
- [OpenCV](https://opencv.org/) and [Pytesseract](https://github.com/madmaze/pytesseract) for image processing and OCR capabilities.


