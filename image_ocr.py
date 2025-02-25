from PIL import Image
import pytesseract
import os
import cv2
import numpy as np

relative_utvonal = '~/Images/image.jpg'
absolute_utvonal = os.path.abspath(relative_utvonal)

def simple_denoise_ocr(image_path, denoise_strength=260, debug=False):
    try:
        # Load image and convert to OpenCV grayscale
        image = Image.open(image_path)
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)  # Direct grayscale conversion

        # Apply Non-Local Means Denoising (preserves edges better than Gaussian)
        denoised = cv2.fastNlMeansDenoising(
            gray, 
            h=denoise_strength,      # Adjust based on noise level (higher = stronger denoising)
            templateWindowSize=7, 
            searchWindowSize=21
        )

        # Ensure black text on white background (critical for Tesseract)
        if np.mean(denoised) < 127:
            denoised = cv2.bitwise_not(denoised)

        # Save denoised image for inspection
        if debug:
            cv2.imwrite("debug_denoised.png", denoised)

        # Directly pass the denoised grayscale image to Tesseract
        text = pytesseract.image_to_string(
            Image.fromarray(denoised), 
            config='--psm 6'  # Treat image as a single text block
        )

        return text.strip()

    except Exception as e:
        return f"Error: {e}"

result = simple_denoise_ocr(absolute_utvonal, denoise_strength=12, debug=True)
print("Extracted Text:\n", result)
