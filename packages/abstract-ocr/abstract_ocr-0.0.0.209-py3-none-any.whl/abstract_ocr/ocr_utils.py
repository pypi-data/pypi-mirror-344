from .functions import *
from moviepy.editor import *
# sort the list
import re
def preprocess_for_ocr(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Enhance contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)

    # Denoise
    denoised = cv2.bilateralFilter(contrast, d=9, sigmaColor=75, sigmaSpace=75)

    # Thresholding
    thresh = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=11,
        C=2
    )

    # Sharpen
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(thresh, -1, sharpen_kernel)

    return sharpened

def is_frame_analyzed(frame_file,video_text_data):
    for values in video_text_data:
        frame = values
        if isinstance(values,dict):
            frame = values.get("frame")
        
        if frame_file == frame:
            return True
        
def analyze_video_text(video_path,output_dir,json_data,remove_phrases=None,video_id=None):
    remove_phrases=remove_phrases or []
    if not video_path or not os.path.isfile(video_path):
        return json_data
    video = VideoFileClip(video_path)
    duration = video.duration
    frame_interval = 1  # Adjust as needed
    for t in range(0, int(duration), frame_interval):
        frame_path = os.path.join(output_dir,f"{video_id}_frame_{t}.jpg")
        if not os.path.isfile(frame_path):
            frame = video.get_frame(t)
            cv2.imwrite(frame_path, cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
    json_data = create_key_value(json_data,'video_text',[])
    for frame_file in os.listdir(output_dir):
        if frame_file.endswith(".jpg"):
            if not is_frame_analyzed(frame_file,json_data['video_text']):
                image_path = os.path.join(output_dir,frame_file)
                raw_text = extract_text_from_image(image_path)
                cleaned_text = clean_text(raw_text)
                text = determine_remove_text(cleaned_text,remove_phrases=json_data['remove_phrases'])
                json_data['video_text'].append({"frame": frame_file, "text": text})
    

    json_data["video_text"].sort(
        key=lambda item: int(re.search(r"_frame_(\d+)\.jpg$", item["frame"]).group(1))
    )
    return json_data

def extract_text_from_image(image_path: str) -> str:
    try:
        processed_img = preprocess_for_ocr(image_path)
        pil_img = Image.fromarray(cv2.bitwise_not(processed_img))  # invert for OCR
        text = pytesseract.image_to_string(pil_img, lang='eng')
        return text
    except Exception as e:
        print(f"[OCR Error] {e}")
        return ""



def download_pdf(url: str, output_path: str):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"PDF downloaded successfully: {output_path}")
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
is_start = False
# Helper functions (as defined previously)
def preprocess_image(image_path: str, output_path: str) -> None:
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)
    denoised = cv2.bilateralFilter(contrast, d=9, sigmaColor=75, sigmaSpace=75)
    thresh = cv2.adaptiveThreshold(
        denoised, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 
        blockSize=11, 
        C=2
    )
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.dilate(thresh, kernel, iterations=1)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(morph, -1, sharpen_kernel)
    cv2.imwrite(output_path, sharpened)

def convert_image_to_text(image_path: str) -> str:
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng')
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s:.,-]', '', text)
    text = text.strip()
    return text

def write_to_file(file_path: str, contents: str) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(contents)

def process_pdf(main_pdf_path: str, pdf_output_dir: str) -> None:
    """Process a PDF into pages, images, text, preprocessed images, preprocessed text, and cleaned preprocessed text."""
    # Get PDF filename without extension
    pdf_name = os.path.splitext(os.path.basename(main_pdf_path))[0]

    # Create subdirectories for this PDF
    pdf_pages_dir = os.path.join(pdf_output_dir, 'pdf_pages')
    os.makedirs(pdf_pages_dir, exist_ok=True)
    images_dir = os.path.join(pdf_output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    text_dir = os.path.join(pdf_output_dir, 'text')
    os.makedirs(text_dir, exist_ok=True)
    cleaned_text_dir = os.path.join(text_dir, 'cleaned')
    os.makedirs(cleaned_text_dir, exist_ok=True)
    preprocessed_images_dir = os.path.join(pdf_output_dir, 'preprocessed_images')
    os.makedirs(preprocessed_images_dir, exist_ok=True)
    preprocessed_text_dir = os.path.join(pdf_output_dir, 'preprocessed_text')
    os.makedirs(preprocessed_text_dir, exist_ok=True)
    cleaned_preprocessed_text_dir = os.path.join(preprocessed_text_dir, 'cleaned')
    os.makedirs(cleaned_preprocessed_text_dir, exist_ok=True)
    

    pdf_reader = PyPDF2.PdfReader(main_pdf_path)
    num_pages = len(pdf_reader.pages)
    logging.info(f"Processing {pdf_name} with {num_pages} pages")

    for page_num in range(num_pages):
        
            # Split PDF into individual pages
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])
            filename = f"{pdf_name}_page_{page_num + 1}"
            basename_pdf= f"{filename}.pdf"
            basename_png= f"{filename}.png"
            preprocessed_basename_png = f"preprocessed_{basename_png}"
            basename_txt= f"{filename}.txt"
            cleaned_basename_txt = f"cleaned_{basename_txt}"
            preprocessed_basename_txt = f"preprocessed_{basename_txt}"
            preprocessed_cleaned_basename_txt = f"preprocessed_cleaned_{basename_txt}"
            page_path = os.path.join(pdf_pages_dir, basename_pdf)
            with open(page_path, 'wb') as f:
                pdf_writer.write(f)

            # Convert PDF page to image
            images = convert_from_path(page_path)
            if images:
                # Save the image
                img_path = os.path.join(images_dir, basename_png)
                images[0].save(img_path, 'PNG')

                # Extract text directly from the image
                text = convert_image_to_text(img_path)
                txt_path = os.path.join(text_dir, basename_txt)
                write_to_file(file_path=txt_path, contents=text)

                # Clean the extracted text
                cleaned_text = clean_text(text)
                cleaned_text_path = os.path.join(cleaned_text_dir, cleaned_basename_txt)
                write_to_file(file_path=cleaned_text_path, contents=cleaned_text)

                # Preprocess the image
                
                preprocessed_img_path = os.path.join(preprocessed_images_dir, preprocessed_basename_png)
                preprocess_image(img_path, preprocessed_img_path)

                # Extract text from the preprocessed image
                preprocessed_text = convert_image_to_text(preprocessed_img_path)
                
                preprocessed_txt_path = os.path.join(preprocessed_text_dir, preprocessed_basename_txt)
                write_to_file(file_path=preprocessed_txt_path, contents=preprocessed_text)

                # Clean the preprocessed text
                preprocessed_cleaned_text = clean_text(preprocessed_text)
                
                preprocessed_cleaned_txt_path = os.path.join(cleaned_preprocessed_text_dir, preprocessed_cleaned_basename_txt)
                write_to_file(file_path=preprocessed_cleaned_txt_path, contents=preprocessed_cleaned_text)
                    
                logging.info(f"Processed page {page_num + 1} of {pdf_name}")
