from PyPDF2 import PdfFileReader, PdfFileWriter


class PdfMerger:
    def __init__(self, main_file, second_file, start_merge_after_page=None, skip_pages_on_main_file=[],
        skip_pages_on_second_file=[], merge_from_page=None, merge_to_page=None, keep_writing_after_merge=True):
        self.main_file = main_file
        self.second_file = second_file
        self.start_merge_after_page = start_merge_after_page
        self.merge_from_page = merge_from_page
        self.merge_to_page = merge_to_page
        self.keep_writing_after_merge = keep_writing_after_merge
        self.skip_pages_on_main_file = skip_pages_on_main_file
        self.skip_pages_on_second_file = skip_pages_on_second_file
    
    def merge(self):
        merged_file = PdfFileWriter()

        self.start_merge_after_page = self.main_file.getNumPages() - 1 if self.start_merge_after_page is None else self.start_merge_after_page - 1
        self.merge_from_page = 0 if self.merge_from_page is None else self.merge_from_page - 1# - 1 --->>> maybe do minus 1
        self.merge_to_page = self.second_file.getNumPages() - 1 if self.merge_to_page is None else self.merge_to_page

        for i in range(self.main_file.getNumPages()):
            if i + 1 not in self.skip_pages_on_main_file:
                merged_file.addPage(self.main_file.getPage(i))
            
            if i == self.start_merge_after_page:
                for j in range(self.merge_from_page, self.merge_to_page):
                    if j + 1 not in self.skip_pages_on_second_file:
                        merged_file.addPage(self.second_file.getPage(j))
                
                if not self.keep_writing_after_merge:
                    break
        
        return merged_file
