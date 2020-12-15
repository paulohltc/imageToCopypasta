import cv2
import argparse
import math
import os

IMGS_PATH = 'images/'

parser = argparse.ArgumentParser(description='High,low threshold value of intensity gradient and grayscale (0 or 255) for special character')
parser.add_argument('-ht', '--hthreshold', required = True, type = int, help ='High threshold')
parser.add_argument('-lt', '--lthreshold', required = True, type = int, help ='Low threshold')
parser.add_argument('-g', '--gray', type = int, default = 0, help = 'Grayscale, 0 or 255')
args =  vars(parser.parse_args())


def show(img):
    cv2.imshow('i',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def writeTxt(copypasta):
    f = open('output.txt','w',encoding = 'utf-8')
    f.write(copypasta)
    f.close()

# os valores de char do caractere com 2x4 tinha como base o caractere 10240 e trabalhava com os 8 bits e tinha essa posição diferenciada de bits
#  0**3
#  1**4
#  2**5
#  6**7
bits = {
    (0,0):0, (1,0):3,
    (0,1):1, (1,1):4,
    (0,2):2, (1,2):5,
    (0,3):6, (1,3):7,
}

def toText(roi): # transforma regiao de interesse de tamanho 2x4 no caractere
    soma = 0
    start = 10240
    for linha in range(4):
        for coluna in range(2):
            if roi[linha][coluna] == args['gray']:
                exp = bits[(coluna,linha)]
                soma += int(math.pow(2,exp))
    return chr(start+soma)


def edgedToCopyPasta(edged): # iterar todas as regioes 2x4 da imagem com silhueta, transformando e juntando em uma unica string
    ans = ''
    linhas,colunas= edged.shape
    for i in range(0,linhas,4):
        for j in range(0,colunas,2):
            roi = edged[i:i+4,j:j+2]
            ans += toText(roi)
        ans+='\n'    
    return ans

def main():
    files = os.listdir(IMGS_PATH)
    copypastas = ''
    for filename in files:
        img = cv2.imread(os.path.join(IMGS_PATH,filename))
        width,height, _ = img.shape
        # O limite de caracteres por linha na twitch/ meet é perto de 29, e estamos dobrando para garantir que será um multiplo de 2 na hora
        # do recorte da região de interesse
        x = 2*29 
        y = math.ceil(width*2*29.0/height) # Esticar na mesma proporção
        y = y - y % 4 # Garantindo que a quantidade de pixeis comprimento seja multiplo de 4
        img = cv2.resize(img,(x,y))
        
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17) # tirar pertubação
        edged = cv2.Canny(gray, args['hthreshold']  , args['lthreshold'])
        copypasta = edgedToCopyPasta(edged)
        copypastas += copypasta+'\n'
        #show(edged)
    
    writeTxt(copypastas)

if __name__ == "__main__":
    main()
    

