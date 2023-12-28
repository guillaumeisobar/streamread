import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from io import BytesIO
import re
import base64

def main():
    st.title('OCR Processor for Scanned Books')
    uploaded_files = upload_files()
    if uploaded_files:
        process_files(uploaded_files)

def upload_files():
    """Uploads files and sets sidebar settings for preprocessing and OCR."""
    files = st.sidebar.file_uploader('Upload Images', accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
    if files:
        st.sidebar.slider('Scale Factor for OCR', 1.0, 3.0, 1.5, key='scale_factor')
        st.sidebar.slider('Gaussian Blur Kernel Size', 1, 11, 5, step=2, key='blur_ksize')
        st.sidebar.slider('Otsu Threshold Value', 0, 255, 128, key='otsu_thresh_value')
    return files

def process_files(uploaded_files):
    """Processes the uploaded files for OCR and previews."""
    sorted_files = sorted(uploaded_files, key=lambda x: natural_sort_key(x.name))
    image_width = np.array(Image.open(BytesIO(sorted_files[0].getvalue()))).shape[1]
    left_split_line, right_split_line = get_split_line_sliders(image_width)

    if st.sidebar.button('Start OCR Process'):
        perform_ocr_on_all(sorted_files, left_split_line, right_split_line)

    show_preview(sorted_files, left_split_line, right_split_line)

def get_split_line_sliders(image_width):
    """Returns the positions of split line sliders."""
    left = st.sidebar.slider('Set the Left Split Line (Blue)', 0, image_width, value=250, key='left_split_line')
    right = st.sidebar.slider('Set the Right Split Line (Green)', 0, image_width, value=image_width - 250, key='right_split_line')
    return left, right

def perform_ocr_on_all(files, left_line, right_line):
    """Performs OCR on all files and shows progress."""
    all_text, all_processed_text = [], []
    progress_bar = st.progress(0)

    for i, file in enumerate(files):
        progress_bar.progress((i + 1) / len(files))
        image = np.array(Image.open(BytesIO(file.getvalue())))
        # Process and perform OCR...
        # Append results to all_text and all_processed_text

    joined_text = join_broken_lines('\n'.join(all_processed_text))
    st.sidebar.markdown(get_text_download_link('\n'.join(all_text), 'full_text.txt'), unsafe_allow_html=True)
    st.sidebar.markdown(get_text_download_link(joined_text, 'processed_text.txt'), unsafe_allow_html=True)
    st.write('OCR Process Complete!')

def show_preview(files, left_line, right_line):
    """Shows a preview of the selected file with split lines."""
    if st.sidebar.checkbox('Show Pre-OCR Preview with Split Lines', value=True):
        preview_page_number = st.sidebar.selectbox('Select Preview Page Number', range(len(files)), format_func=lambda x: f"Preview Page {x + 1}", key='preview_page_select')
        preview_image = np.array(Image.open(BytesIO(files[preview_page_number].getvalue())))
        draw_split_lines(preview_image, left_line, right_line)
        downscaled_preview = downscale_image(preview_image, 50)
        st.image(downscaled_preview, caption=f'Preview with Split Lines - Page {preview_page_number + 1}', use_column_width=True)

def draw_split_lines(image, left_line, right_line):
    """Draws colored split lines on the image."""
    cv2.line(image, (left_line, 0), (left_line, image.shape[0]), (255, 0, 0), 2)
    cv2.line(image, (right_line, 0), (right_line, image.shape[0]), (0, 255, 0), 2)

def natural_sort_key(s):
    """Sorts strings containing numbers in a human-friendly order."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def preprocess_image(page_img, blur_ksize, otsu_thresh_value):
    """Applies Gaussian blur and Otsu thresholding to an image."""
    gray = cv2.cvtColor(page_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    _, otsu_thresh = cv2.threshold(blurred, otsu_thresh_value, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return otsu_thresh

def perform_ocr(preprocessed_img, scale_factor=1.5):
    """Performs OCR on the preprocessed image."""
    resized_img = cv2.resize(preprocessed_img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)
    final_img = Image.fromarray(resized_img)
    text = pytesseract.image_to_string(final_img, lang='fra', config='--oem 1 --psm 6')
    return text

def correct_common_ocr_errors(text):
    """Corrects common OCR errors in the extracted text."""
    corrections = {
        r'\bct\b': 'et',
        r'\bcn\b': 'en',
        r'\bfn\b': 'en',
        r'cffet': 'effet',
        r'\bunc\b': 'une',
        r'\blc\b': 'le',
        r'd\'unc': 'd\'une',
        r'\bFn\b': 'En',
        # ... more corrections as needed
    }
    for error, correction in corrections.items():
        text = re.sub(error, correction, text, flags=re.IGNORECASE)
    return text

def join_broken_lines(text):
    """Joins broken lines in OCR output."""
    pattern = re.compile(r'(?<![\.\?\!])\n')
    return pattern.sub(' ', text)

def get_text_download_link(text, filename):
    """Generates a download link for the given text."""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def downscale_image(image, scale_percent):
    """Downscales the image by the given percentage."""
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

if __name__ == "__main__":
    main()
