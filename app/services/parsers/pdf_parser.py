import fitz
from domain.file_entities import FileResult, Picture, Sentence
from domain.interfaces.file_parser import FileParser

class PdfParser(FileParser):
    def parse_file(self,filename: str) -> FileResult:
    
        sentences: list[Sentence] = []
        images: list[Picture] = []
        
        
        doc = fitz.open("docs/" + filename)
        for page in doc:
            page.get_text().split(".\n")
            
            for text in page.get_text().split(".\n"):
                sentences.append(Sentence(sentence=text, page_number=page.number))
            
            image_list = page.get_images()
            for image_index, img in enumerate(image_list, start=1): # enumerate the image list
                xref = img[0] # get the XREF of the image
                pix = fitz.Pixmap(doc, xref) # create a Pixmap

                if pix.n - pix.alpha > 3: # CMYK: convert to RGB first
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                    
                pix.save("page_%s-image_%s.png" % (page.number, image_index)) # save the image as png
                    
                images.append(Picture(picture=pix, page_number=page.number))

        return FileResult(file_name=filename, sentences=sentences, images=images)
