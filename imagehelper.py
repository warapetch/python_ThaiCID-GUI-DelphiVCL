"""
    pillow==10.2.0
    pip install pillow
    
    from :: https://stackoverflow.com/questions/7050448/write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard
"""

from io import BytesIO
import win32clipboard
from PIL import Image as PILImage

def saveImageFileToClipboard(filepath):
    
    image = PILImage.open(filepath)

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()
    
    
def saveImageDataToClipboard(image : PILImage):
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()
    
    
    
def convertJpgToPng(InputJpgFileName,OutputPngFileName):
    imgJpg = PILImage.open(InputJpgFileName)
    imgJpg.save(OutputPngFileName)    
    
    return True