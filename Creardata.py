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
        
    final_authors='\tauthor={'
    
    for i,name in enumerate(Autor_encontrado):
        if i == 0:
            final_authors+=name
        else:
            final_authors+=' and '+name

    encontrado = False
    for l in biblines:
        CMS = l.find('CMS')
        if CMS != -1 and encontrado == False:
            encontrado = True
            final_authors += ' and CMS Collaboration' 

    final_authors+='},\n'
    
    #print(final_authors)

    # Escribimos nueva bibliografica
    #output = open("Final/"+f.name, "w")
    with codecs.open("Final/"+f.name, "w", "utf-8") as output:
    
        Doi = False
        for l in biblines:
            doi_lines = l.find('doi = ')
            if doi_lines != -1:
                Doi = l
                Doi = Doi.replace('doi = {',"")
                Doi = Doi.replace('},',"")
                # Quitamos espacios en blanco
                Doi = Doi.strip()
              #  print(Doi)
        
       
        for l in biblines:
            author_lines = l.find('author')
            file_lines = l.find('file')
            abstract_lines = l.find('abstract')
            
            
            # Quitamos file lines
            if file_lines != -1 or abstract_lines != -1:
                continue

            if author_lines != -1:
                output.write(final_authors) # Cambiamos lista de autores
                output.write('\tpages = {1-10},\n')
                if Doi != False:
                    output.write('\turl = {https://doi.org/'+Doi+'},\n')
            
                  
            else:
                output.write(l)                   
                 

        
    
    #output1 = open("Temp/"+f.name, "w")
    with codecs.open("Temp/"+f.name, "w", "utf-8") as output1:
    
        for i, name in enumerate(Autor_noencontrado):
            output1.write(name+'\n')
    
    #output1.close()

# Ahora creamos el archivo final
Files1 = []

for f in glob.glob('Final/Data/*.bib'):
    file = open(f, 'r', encoding='utf-8')
    Files1.append(file)


with codecs.open("Final/DataFinal.bib", "w", "utf-8") as output1:

    
    for f in Files1:

        biblines = f.readlines()

        for l in biblines:
            output1.write(l)

        