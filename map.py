import requests
from PIL import Image, ImageDraw
from io import BytesIO

# Função para fazer a requisição e obter os dados JSON
def obter_dados(url):
    response = requests.get(url)
    return response.json()

# Função para carregar as imagens dos tiles, NPCs e itens utilizáveis
def carregar_imagens():
    imagens = {}

    tipos = ['escadas', 'paredes', 'npcs', 'usaveis', 'monstros']
    for tipo in tipos:
        for elemento in data[tipo]:
            nome = elemento['nome']
            if nome not in imagens:
                imagens[nome] = Image.open(f"{tipo}/{nome}.png")

    return imagens

# Função para criar o mapa
def criar_mapa(imagens):
    mapa = Image.new('RGBA', (100 * 64, 100 * 64), (255, 255, 255, 0))
    draw = ImageDraw.Draw(mapa)

    for tipo in data:
        for elemento in data[tipo]:
            nome = elemento['nome']
            imagem = imagens[nome]
            x = elemento['posicao']['x'] * 64
            y = elemento['posicao']['y'] * 64
            mapa.paste(imagem, (x, y), imagem)

    return mapa

# URL da API
url = "http://192.168.15.6:3000/api/acessar_link"

# Obter os dados da API
data = obter_dados(url)

# Carregar as imagens dos tiles, NPCs e itens utilizáveis
imagens = carregar_imagens()

# Criar o mapa
mapa = criar_mapa(imagens)

# Salvar o mapa
mapa.save('mapa.png')
