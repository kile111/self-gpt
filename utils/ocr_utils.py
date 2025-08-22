import easyocr

def ocr_image_easyocr(file):
    image_bytes = file.read()
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=False)
    result = reader.readtext(image_bytes, detail=0)
    return "\n".join(result)