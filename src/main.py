import os 
import sys
import shutil
from utils import generate_page

def clean_public():
    if not os.path.exists('docs'):
        print('docs folder is missing')
        return 
    shutil.rmtree('docs')

def copyFiles(src, dest):
    for item in os.listdir(src):
        if os.path.isfile(os.path.join(src,item)):
            print(f'src : {os.path.join(src,item)}  dest: {dest}')
            shutil.copy(os.path.join(src,item), dest)
        else:
            os.mkdir(os.path.join(dest, item))
            copyFiles(os.path.join(src,item), os.path.join(dest,item))

def treeGenerate(src, template, dest, basepath):

    for item in os.listdir(src):
        if os.path.isdir(os.path.join(src, item)):
            os.mkdir(os.path.join(dest, item))
            treeGenerate(os.path.join(src, item), template, os.path.join(dest, item), basepath)
        else:
            generate_page(os.path.join(src, item), template, os.path.join(dest, item.replace('md', 'html') ), basepath)

def main():

    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'

    clean_public()
    os.mkdir('docs')
    copyFiles('static', 'docs')
    treeGenerate('content', 'template.html', 'docs', basepath)

if __name__ == '__main__':
    main()
