import glob
import os
from os import path

if not path.exists('Final'):
    os.mkdir('Final')
if not path.exists('Final/Data'):
    os.mkdir('Final/Data')
    print('Creando directorio objetivo')

if not path.exists('Config/Profesores.txt'):
	print('Sin archivo de configuracion')
	exit(1)

if not path.exists('Config/Diccionario.txt'):
    print('Sin archivo del diccionario')
    exit(1)


with open('Config/Profesores.txt','r') as fprofe:
    Lista_Profesores = [linea.rstrip() for linea in fprofe]

with open('Config/Diccionario.txt','r') as fdict:
    Dict_Profesores = [linea.rstrip() for linea in fdict]

if len(Lista_Profesores) != len(Dict_Profesores):
    print('Diccionario imcompleto')
    exit(1)

Dict1 = dict(zip(Lista_Profesores,Dict_Profesores))

print(Dict1)

def CheckAuthor(author, biblines):
        
    NRef = 0
            
    for l in biblines:
        isinfile = l.find(author)
                
        if isinfile != -1:
            NRef = 1
               
    return NRef

# Funcion para cada archivo
Files = []
for f in glob.glob('Data/*.bib'):
    file = open(f, "r", encoding='utf-8')
    Files.append(file)
    
#Files[0].name    
    
for f in Files:
    
    print('Creando:', f.name)
    
    biblines = f.readlines()
    
    Autores_Andes = []
    
    output = open("Final/"+f.name, "w")
    
    for author in Lista_Profesores:
        
        NRef = CheckAuthor(author,biblines)
    
        if NRef == 1:
            Autores_Andes.append(Dict1[author])
        else:
            print('Articulo:', f.name, 'No Encontrado:',author)
    
    for i, name in enumerate(Autores_Andes):
        if i==0:
            output.write(name)
        else:
            output.write(', '+name)
        
    output.close()
    
    #print(Autores_Andes)