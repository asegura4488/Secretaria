import glob
import os
from os import path
import codecs

if not path.exists('Final'):
    os.mkdir('Final')
if not path.exists('Final/Data'):
    os.mkdir('Final/Data')

if not path.exists('Temp'):
    os.mkdir('Temp')
if not path.exists('Temp/Data'):
    os.mkdir('Temp/Data')

if not path.exists('Config/Profesores.txt'):
    print('Sin archivo de configuracion')
    exit(1)

if not path.exists('Config/Diccionario.txt'):
    print('Sin archivo del diccionario')
    exit(1)

with open('Config/Profesores.txt','r', encoding='utf-8') as fprofe:
    Lista_Profesores = [linea.rstrip() for linea in fprofe]

with open('Config/Diccionario.txt','r', encoding='utf-8') as fdict:
    Dict_Profesores = [linea.rstrip() for linea in fdict]

if len(Lista_Profesores) != len(Dict_Profesores):
    print('Diccionario imcompleto')
    exit(1)

Dict1 = dict(zip(Lista_Profesores,Dict_Profesores))

def CheckAuthor(author, biblines):
        
    NRef = 0
            
    for l in biblines:
        isinfile = l.find(author)
                
        if isinfile != -1:
            NRef = 1
               
    return NRef

Files = []

for f in glob.glob('Data/*.bib'):
    file = open(f, 'r', encoding='utf-8')
    Files.append(file)
    
#Files[0].name    
    
for f in Files:
    
    #print('Creando:', f.name)
    
    biblines = f.readlines()
    
    Autor_encontrado = []
    Autor_noencontrado = []
    
    for author in Lista_Profesores:
        NRef = CheckAuthor(author,biblines)
    
        if NRef == 1:
            Autor_encontrado.append(Dict1[author])
        else:
            Autor_noencontrado.append(Dict1[author])
        
    final_authors='\t author={'
    
    for i,name in enumerate(Autor_encontrado):
        if i == 0:
            final_authors+=name
        else:
            final_authors+=', '+name
        
    final_authors+='},\n'
    
    #print(final_authors)

    # Escribimos nueva bibliografica
    #output = open("Final/"+f.name, "w")
    with codecs.open("Final/"+f.name, "w", "utf-8") as output:
    
        for l in biblines:
            author_lines = l.find('author')
            if author_lines != -1:
                output.write(final_authors) # Cambiamos lista de autores
            else:
                output.write(l)
        
    #output.close()
    
    #output1 = open("Temp/"+f.name, "w")
    with codecs.open("Temp/"+f.name, "w", "utf-8") as output1:
    
        for i, name in enumerate(Autor_noencontrado):
            output1.write(name+'\n')
    
    #output1.close()
