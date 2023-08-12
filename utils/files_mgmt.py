import os, sys
from zipfile import ZipFile


current_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_dir)

res_dir = os.path.abspath(os.path.join(root_dir, 'res'))
out_dir = os.path.abspath(os.path.join(root_dir, 'out'))

def load_words():
    words_file = os.path.abspath(os.path.join(res_dir, 'words.zip'))
    with ZipFile(words_file, 'r') as zip:
        raw_words = zip.read('words.txt')
        words = set(raw_words.split())
        
    words_alpha_file = os.path.abspath(os.path.join(res_dir, 'words_alpha.zip'))
    with ZipFile(words_alpha_file, 'r') as zip:
        raw_words_alpha = zip.read('words_alpha.txt')
        words_alpha = set(raw_words_alpha.split())
        
    words.update(words_alpha)    
    
    encoding = "utf-8"
    words_list = list()
    for word in list(words):
        words_list.append(word.decode(encoding))
        
    return words_list


def get_file_by_suffix(suffix_name, dir_name=None, inclusive_keyword=None, exclusive_keyword=None):
    if dir_name:
        target_dir = os.path.abspath(os.path.join(root_dir, dir_name))
    else:
        target_dir = root_dir
        
    if type(suffix_name) is not str:
        suffix_name = str(suffix_name)
        
    paths_hash = dict()
    
    if inclusive_keyword:
        for path, sub_dirs, files in os.walk(target_dir):
            for file in files:
                if((file.endswith('.' + suffix_name) or 
                    file.endswith('.' + suffix_name.lower()) or 
                    file.endswith('.' + suffix_name.title()) or 
                    file.endswith('.' + suffix_name.upper()))) and (inclusive_keyword in file):
                    paths_hash[file] = os.path.join(path, file)
    
    elif exclusive_keyword:
        for path, sub_dirs, files in os.walk(target_dir):
            for file in files:
                if((file.endswith('.' + suffix_name) or 
                    file.endswith('.' + suffix_name.lower()) or 
                    file.endswith('.' + suffix_name.title()) or 
                    file.endswith('.' + suffix_name.upper()))) and (exclusive_keyword not in file):
                    paths_hash[file] = os.path.join(path, file)
                    
    else:
        for path, sub_dirs, files in os.walk(target_dir):
            for file in files:
                if(file.endswith('.' + suffix_name) or 
                    file.endswith('.' + suffix_name.lower()) or 
                    file.endswith('.' + suffix_name.title()) or 
                    file.endswith('.' + suffix_name.upper())):
                    paths_hash[file] = os.path.join(path, file)
                
    return paths_hash


if __name__ == '__main__':
    print(load_words())