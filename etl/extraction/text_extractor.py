import os
import pymupdf

if __name__ != "__main__":
    from etl.extraction.form_input import form_input_boundary
else:
    from extraction.form_input import form_input_boundary   

def retrieve_input_strings(pdf) -> dict:
    
    form_input_boundary_temp = form_input_boundary.copy()
    form_input_data = dict(zip(form_input_boundary_temp.copy().keys(), ['']*21))
    
    pdf_temp = pdf
    
    X1_COOD_TOLERANCE_FROM_LEFT = 139
    
    # get specific word, draw rectangle border
    try:        
        # filter most none input words from pdf extracted words
        words = pdf[0].get_text_words()
        words = [word_info for word_info in words if word_info[0] > X1_COOD_TOLERANCE_FROM_LEFT and
                                            ':' not in word_info[4]]
        
        # 
        def draw_word_boundary(page, rect_boundary, color, width) : \
            page.draw_rect(pymupdf.Rect(rect_boundary), color=color, width=width)
        
        for word_info in words:   
            
            word_boundary = word_info[:4]
            word = word_info[4]
            
            # check every input boundary if intersects word boundary
            for input_name, input_boundary in form_input_boundary_temp.items():
                
                input_rect = pymupdf.Rect(input_boundary)
                
                # concat word to corresponding form_input_data item
                if input_rect.intersects(word_boundary):
                    if form_input_data[input_name] != '':
                        form_input_data[input_name] += ' '
                    
                    form_input_data[input_name] += word
                        
                    draw_word_boundary(pdf_temp[0], word_boundary, (0,0,0), 3)
                    break
                        
        # draw boxes for input boundaries
        for _, boundary in form_input_boundary.items():
            draw_word_boundary(pdf_temp[0], boundary, (1,0,0), 1)

    except Exception as e:
        print(f"Error: {e}")
    
    
    return form_input_data

def save_altered_pdf() -> None:
    try:
            if os.path.exists('others\test_report_highlight\temp.pdf'):
                os.remove('others\test_report_highlight\temp.pdf')
                
            pdf_temp.save('others/temp.pdf')
            
    except Exception as e:
        print(f"Error: {e}")
    
if __name__ == "__main__":
    pdf = pymupdf.open(r"others\test_reports_batch\template-1.pdf")
    pdf_temp = pdf
    
    form_input_data = retrieve_input_strings(pdf_temp)
    print(form_input_data)
    
    print("\nDone")
    
    save_altered_pdf()