import re

def str_to_list(pages_as_str):
    if not pages_as_str:
        return []
    
    rv = []
    pages = pages_as_str.replace(' ', '').split(sep=',')
    
    for page in pages:
        if '-' in page:
            tmp = page.split('-')
            for num in range(int(tmp[0]), int(tmp[1]) + 1):
                rv.append(num)
        else:
            rv.append(int(page))
    
    return rv

def letters_exists(string):
    if re.search('[a-zA-Z]', string) is None:
        return False
    return True
