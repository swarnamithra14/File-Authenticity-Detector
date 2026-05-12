from PIL import Image
from PyPDF2 import PdfReader


def extract_metadata(file_path, file_type):
    metadata = {}

    try:
        # 📸 IMAGE METADATA
        if file_type in ["PNG", "JPG"]:
            img = Image.open(file_path)

            metadata["Type"] = "Image"
            metadata["Format"] = img.format
            metadata["Size"] = f"{img.width} x {img.height}"
            metadata["Mode"] = img.mode

        # 📄 PDF METADATA
        elif file_type == "PDF":
            reader = PdfReader(file_path)
            info = reader.metadata

            metadata["Type"] = "PDF"

            if info:
                metadata["Author"] = str(info.author)
                metadata["Creator"] = str(info.creator)
                metadata["Title"] = str(info.title)

        else:
            metadata["Type"] = "Unknown / Not Supported"

    except Exception:
        metadata["Warning"] = "Invalid or corrupted file format (possible spoofing detected)"

    return metadata