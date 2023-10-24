def nftd(content:str):
    new_content = content\
    .replace('_','\_')\
    .replace('*','\*')\
    .replace('~','\~')\
    .replace('|','\|')\
    .replace('>','\>')\
    .replace('`','\`')\
    .replace('#','\#')\
    .replace('-','\-')\
    .replace('[','\[')\
    .replace(']','\]')\
    .replace('(','\(')\
    .replace(')','\)')
    return new_content
