import io
import streamlit as st
from PyPDF2 import PdfFileReader
from merger import PdfMerger
from utils import str_to_list, letters_exists

st.set_page_config(page_title='PDF Merger',
                   page_icon='https://cdn4.iconfinder.com/data/icons/CS5/256/ACP_PDF%202_file_document.png')
st.title('PDF Merger')


main_file = st.file_uploader("Upload Main File",type=['pdf'])
second_file = st.file_uploader("Upload 2nd file File",type=['pdf'])
file_name = st.text_input(label='File Name:', value='Merged')

if main_file and second_file:
    pdf1 = PdfFileReader(main_file, strict=False)
    pdf2 = PdfFileReader(second_file, strict=False)
    
    st.warning('### Don\'t change those settings to merge the files one after the other!')
    
    start_merge_after_page = st.number_input(label='Merge the 2nd file after page:', step=1,
                                             value=pdf1.getNumPages(),
                                             min_value=1,
                                             max_value=pdf1.getNumPages())
    
    merge_from_page = st.number_input(label='The 2nd file starting at page:', step=1,
                                      value=1,
                                      min_value=1,
                                      max_value=pdf2.getNumPages())
    
    merge_to_page = st.number_input(label='The 2nd file ending at page:', step=1,
                                    value=pdf2.getNumPages(),
                                    min_value=int(merge_from_page),
                                    max_value=pdf2.getNumPages())
    
    skip_pages_on_main_file = st.text_input(label='Enter the pages you want to skip them from the main file:',
                                            key='skipped_main_file',
                                            help='Usage: Contain only numbers seperated by comma like: 1, 3, 5 ' \
                                                'or range like: 5-9, 11-14. If None, don\'t skip at all.')
    
    skip_pages_on_second_file = st.text_input(label='Enter the pages you want to skip them from the 2nd file:',
                                              key='skipped_2nd_file',
                                              help='Usage: Contain only numbers seperated by comma like: 1, 3, 5 ' \
                                                'or range like: 5-9, 11-14 If None, don\'t skip at all.')
    
    keep_writing_after_merge = st.checkbox(label='Keep writing the rest of pages from main file after merged 2nd file?',
                                           value=True)
    
    
    is_finished = st.button(label='Finish')

    if is_finished:
        if not letters_exists(skip_pages_on_main_file) and \
            not letters_exists(skip_pages_on_second_file):
            
            main_file_skip = str_to_list(st.session_state.skipped_main_file)
            second_file_skip = str_to_list(st.session_state.skipped_2nd_file)
            
            merger_obj = PdfMerger(pdf1, pdf2, start_merge_after_page, main_file_skip, second_file_skip,
                                   merge_from_page, merge_to_page, keep_writing_after_merge)

            mereged_pdf = merger_obj.merge()
            tmp = io.BytesIO()
            mereged_pdf.write(tmp)
            
            st.download_button('Download', tmp.getvalue(), mime='application/pdf', file_name=f'{file_name}.pdf')
        else:
            st.error('Values CAN NOT contain any letter!')
    