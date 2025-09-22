import os
import pymupdf
from PIL import Image
import io

data_dir = "./pdfs/orginals"
output_dir = "./pdfs/optimized"

def main() -> None:
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(data_dir):
        print(filename)
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(data_dir, filename)
            src = pymupdf.open(pdf_path)
            num_pages = src.page_count
            page_ind = 1
            image_files = []
            for src_page in src:
                imageList = src_page.get_images(full=True)
                if imageList:
                    for idx, img in enumerate(imageList, start=1):
                        try:
                            data = src.extract_image(img[0])
                            image_bytes = data.get('image')
                            with Image.open(io.BytesIO(image_bytes)) as image:
                                # First and last page in color, others in grayscale
                                quality = 4
                                if page_ind == 1 or page_ind == num_pages:
                                    image = image.convert("RGB")
                                    quitality = 5
                                else:
                                    image = image.convert("L")
                                image_file = os.path.join(
                                    output_dir,
                                    f'page_img_{page_ind}-{idx}_{os.path.splitext(filename)[0]}.jpg'
                                )
                                image.save(image_file, format="JPEG", optimize=True, quality=quality)
                                image_files.append(image_file)
                        except Exception as e:
                            print(f"Error extracting image: {e}")
                page_ind += 1
            src.close()
            # Create optimized PDF from images
            output_pdf = os.path.join(output_dir, f"{filename}")
            images_to_pdf_pymupdf(image_files, output_pdf)
            for image_file in image_files:
                os.remove(image_file)

def images_to_pdf_pymupdf(images, output_pdf):
    doc = pymupdf.open()
    for img_path in images:
        with Image.open(img_path) as img:
            width, height = img.size
        page = doc.new_page(width=width, height=height)
        page.insert_image(page.rect, filename=img_path)
    doc.save(output_pdf)

if __name__ == "__main__":
    main()
