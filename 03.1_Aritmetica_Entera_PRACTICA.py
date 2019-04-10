# -*- coding: utf-8 -*-
"""
@author: martinez
"""

import math
import random




#%%
"""
Dado un mensaje y su alfabeto con sus frecuencias dar el código 
que representa el mensaje utilizando precisión infinita (reescalado)

El intervalo de trabajo será: [0,R), R=2**k, k menor entero tal que R>4T

T: suma total de frecuencias

"""


def IntegerArithmeticCode(mensaje,alfabeto,frecuencias):
    m = int(math.ceil(math.log(4*sum(frecuencias))/math.log(2)))
    l = 0
    u = 2**m-1
    cum_count = [0]*(len(alfabeto)+1)
    count = 0
    scale = 0
    for i in range(len(alfabeto)):
        count += frecuencias[i]
        cum_count[i+1] = count
    #we put here the masks
    b = 2**(m-1) #this mask is for checking if the MSB of two words equals
    b2 = 2**(m-2) #and this for checking the second one
    b3 = 2**m-1
    transmission = "" #string containing the coded message

    for c in mensaje:
        i = alfabeto.index(c)
        uax = l+math.floor(((u-l+1)*cum_count[i+1])/count)-1
        l = l+math.floor(((u-l+1)*cum_count[i])/count)
        u = uax
        c1 = (u & b) == (l & b)
        c2 = ((u & b2) != (l & b2)) and ((l & b2) == b2)
        while(c1 | c2):
            if(c1):
                tbit = ''
                if(u & b == 0):
                    tbit = '0'
                else:
                    tbit = '1'
                u = ((u << 1) | 1) & b3
                l = (l << 1) & b3
                transmission += tbit
                while(scale > 0):
                    scale -= 1
                    transmission += '1' if (tbit == '0') else '0' #we send complementary
            c1 = (u & b) == (l & b)
            c2 = ((u & b2) != (l & b2)) and ((l & b2) == b2)
            if not c1 and c2:
                scale += 1
                u = b^(u<<1|1) & b3
                l = b^(l<<1) & b3
            #here we update the conditions
            c1 = (u & b) == (l & b)
            c2 = ((u & b2) != (l & b2)) and ((l & b2) == b2)
        transmission += '0'+'1'*scale+'0'*(m-1)
    return transmission
    
    
#%%
            
            
"""
Dada la representación binaria del número que representa un mensaje, la
longitud del mensaje y el alfabeto con sus frecuencias 
dar el mensaje original
"""
           
def IntegerArithmeticDecode(codigo, tamanyo_mensaje, alfabeto, frecuencias):
    m = int(math.ceil(math.log(4*sum(frecuencias))/math.log(2)))
    l = 0
    u = (2**m)-1
    cum_count = [0]*(len(alfabeto)+1)
    count = 0
    message = ""
    #we put here the masks
    b = 2**(m-1) #this mask is for checking if the MSB of two words equals
    b2 = 2**(m-2) #and this for checking the second one
    b3 = (2**m)-1  #to control max size
    tagoffset = 0
    tag = int(codigo[0:m], 2)
    for i in range(len(alfabeto)):
        count += frecuencias[i]
        cum_count[i+1] = count
    while len(message) < tamanyo_mensaje:
        val = math.floor(((tag -l + 1)*count-1) / (u -l + 1))
        i = 0
        while val >= cum_count[i]:
            i += 1
        message += alfabeto[i-1]
        lax = l + math.floor(((u -l + 1) * cum_count[i-1]) / count)
        u = l + math.floor(((u -l + 1) * cum_count[i]) / count) -1
        l = lax
        c1 = (u & b) == (l & b)
        c2 = ((u & b2) != (l & b2)) and ((l & b2) == b2)
        while c1 | c2:
            if c1:
                tagoffset += 1
                tag = int(codigo[tagoffset : tagoffset+m], 2)
                u = ((u << 1)|1) & b3
                l = (l << 1) & b3
            else:
                if c2:
                    tagoffset += 1
                    tag = int(codigo[tagoffset : tagoffset+m], 2)
                    u = b^((u<<1) & b3)|1
                    l = b^(l<<1) & b3
                    tag = b^tag
            #here we update the conditions
            c1 = (u & b) == (l & b)
            c2 = ((u & b2) != (l & b2)) and ((l & b2) == b2)
    return message

#%%
'''
Definir una función que codifique un mensaje utilizando codificación aritmética con precisión infinita
obtenido a partir de las frecuencias de los caracteres del mensaje.

Definir otra función que decodifique los mensajes codificados con la función 
anterior.
'''

def TransformarMovida(mensaje):
    dick = {}
    for c in mensaje:
        if c in dick: dick[c] += 1
        else: dick[c] = 1
    dicks = sorted(dick, key = lambda k: int(dick[k]))
    alfa = dicks
    freqs = [dick[c] for c in alfa]
    return alfa, freqs

def EncodeArithmetic(mensaje_a_codificar):
    alfa, freqs = TransformarMovida(mensaje_a_codificar)
    print(alfa)
    print(freqs)
    mensaje_codificado = IntegerArithmeticCode(mensaje_a_codificar,alfa,freqs)
    return mensaje_codificado,alfa,freqs
    
def DecodeArithmetic(mensaje_codificado,tamanyo_mensaje,alfabeto,frecuencias):

    return IntegerArithmeticDecode(mensaje_codificado,tamanyo_mensaje,alfabeto,frecuencias)
        
#%%
'''
Ejemplo (!El mismo mensaje se puede codificar con varios códigos¡)

'''

lista_C=['010001110110000000001000000111111000000100010000000000001100000010001111001100001000000',
         '01000111011000000000100000011111100000010001000000000000110000001000111100110000100000000']
alfabeto=['a','b','c','d']
frecuencias=[1,10,20,300]
mensaje='dddcabccacabadac'
tamanyo_mensaje=len(mensaje)  
code = IntegerArithmeticCode(mensaje, alfabeto, frecuencias)

for C in lista_C:
    mensaje_recuperado=DecodeArithmetic(C,tamanyo_mensaje,alfabeto,frecuencias)
    print(mensaje==mensaje_recuperado)



#%%

'''
Ejemplo

'''

mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos.'

mensaje_codificado,alfabeto,frecuencias=EncodeArithmetic(mensaje)
mensaje_recuperado=DecodeArithmetic(mensaje_codificado,len(mensaje),alfabeto,frecuencias)

ratio_compresion=8*len(mensaje)/len(mensaje_codificado)
print(ratio_compresion)

if (mensaje==mensaje_recuperado):
        print('!!!!!!!!!!!!!!  IGUALES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
        
