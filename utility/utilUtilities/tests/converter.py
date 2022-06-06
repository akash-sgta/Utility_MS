# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================
# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from email.policy import default
from django.test import TestCase

# from docx2pdf import convert
import aspose.words as aw
import os
from pathlib import Path

# =========================================================================================
#                                       CONSTANT
# =========================================================================================
BASE_DIR = Path(__file__).resolve().parent

# =========================================================================================
#                                       CODE
# =========================================================================================
class Converter(object):
    QUALITY = 100

    def __init__(self) -> None:
        super(Converter, self).__init__()

    @staticmethod
    def genFileName(path: str, final_ext: str) -> str:
        final_ext = final_ext.lower()
        path = path.split("/")
        file_name = path[-1].split(".")
        if len(file_name) > 1:
            file_name = (".").join(file_name[:-1])
        file_name = f"{file_name}.{final_ext}"
        path[-1] = file_name
        return ("/").join(path)

    @staticmethod
    def wordToPdf(path: str, img_compression=0) -> bool:
        try:
            # convert(input_path=path)
            doc = aw.Document(os.path.join(BASE_DIR, path))
            save_options = aw.saving.PdfSaveOptions()
            save_options.compliance = aw.saving.PdfCompliance.PDF17
            save_options.image_compression[0] = (
                aw.saving.PdfImageCompression.JPEG,
            )
            save_options.jpeg_quality = Converter.QUALITY - img_compression
            doc.save(
                os.path.join(path, Converter.genFileName(path, "PDF")),
                save_options,
            )
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return False
        else:
            return True


if __name__ == "__main__":
    path = input("PATH : ")
    comp = int(input("COMPRESSION % : "))
    print(Converter.wordToPdf(path=path, img_compression=comp))
