# fileName : plugins/dm/callBack/pdfFormatter.py
# copyright ©️ 2021 nabilanavab

# import os
import fitz

#--------------->
#--------> LOCAL VARIABLES
#------------------->

# IG NO Need 🥱
pgNoError="""__For Some Reason A4 FORMATTING Supports for pdfs with less than 5 Pages__"

Total Pages: {} ⭐"""

# NB:
#    A4 paper size in pixels with a resolution of 72 PPI is 595 x 842 px.
#    Screens and monitors usually use 72 PPI
#    
#    In a resolution of 300 PPI A4 is 2480 x 3508 px.
#    For printing you often use 200-300 PPI

#--------------->
#--------> PDF FORMATTER
#------------------->

async def formatterPDF(message, message_id):
    try:
        input_file=f"{message_id}/inPut.pdf"
        output_file=f"{message_id}/outPut.pdf"
        
        # OPEN INPUT PDF
        r=fitz.Rect(0,0,0,0)
        with fitz.open(input_file) as inPDF:
            # OPENING AN OUTPUT PDF OBJECT
            with fitz.open() as outPDF:
                nOfPages=inPDF.pageCount
                if nOfPages>5:
                    await message.edit(pgNoError.format(nOfPages))
                    return False
                # ITERATE THROUGH PAGE NUMBERS
                for _ in range(nOfPages):
                    outPDF.new_page(pno=-1, width=595, height=842)
                    # WIDTH AND HEIGH OF PAGE 
                    page=inPDF[_]
                    pix=page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    # SAVE IMAGE AS NEW FILE
                    with open(unFormated,'wb'):
                        pix.save(unFormated)
                    with Image.open(unFormated) as img:
                        imgWidth, imgHeight=img.size
                        if imgWidth==imgHeight:
                            neWidth=595
                            newHeight=neWidth*imgHeight/imgWidth
                            newImage=img.resize((neWidth, int(newHeight)))
                            y0=(842-newHeight)/2; x0=(595-neWidth)/2
                            x1=x0+newHeight; y1=y0+neWidth
                            r=fitz.Rect(x0, y0, x1, y1)
                        elif imgWidth > imgHeight:
                            neWidth=595
                            newHeight=(neWidth*imgHeight)/imgWidth
                            newImage=img.resize((neWidth, int(newHeight)))
                            x0=0; y0=(842-newHeight)/2
                            x1=595; y1=y0+newHeight
                            r=fitz.Rect(x0, y0, x1, y1)
                        else:
                            newHeight=842
                            neWidth=(newHeight*imgWidth)/imgHeight
                            newImage=img.resize((int(neWidth), newHeight))
                            x0=(595-neWidth)/2; y0=0
                            x1=x0+neWidth; y1=842
                            r=fitz.Rect(x0, y0, x1, y1)
                        newImage.save(unFormated)
                    load=outPDF[_]
                    load.insert_image(
                        rect=r, filename=unFormated
                    )
                    os.remove(unFormated)
                outPDF.save(output_file)
        return "__a4 formatted pdf__"
    except Exception as e:
        print("FormatToA4: " , e)
        return False

#       ______                                                
#      |      |   _________    __    ___                      
#      |      |  |         |  |  |  |   |                     
#      |  A4  |  |    B    |  |B`|  |___|                     
#      |      |  |_________|  |__|    B``                     
#      |______|                                @ nabilanavab  
#                                                             
#   ° 1st resize image B (large side with rt. A4 sheet)       
#   ° height & width must be in same ratio(pillow)            
#   ° get values for B(x⁰, y⁰, x¹, y¹) on A4                  
#   ° Insert B to A4 (here pymuPdf) fitz                      
#                                                             
#                                                                                  Telegram: @nabilanavab
