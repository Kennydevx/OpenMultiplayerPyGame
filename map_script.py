# map_script.py

import os
import requests
import xml.etree.ElementTree as ET
import pygame
from kivy.logger import Logger

class MapRenderer:
    def __init__(self, tmx_url, tileset_dir):
        self.tmx_url = tmx_url
        self.tmx_file_path = os.path.join(os.getcwd(), "map.tmx")
        self.tileset_dir = tileset_dir
        self.map_image_path = None

    def download_file(self, url, destination):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(destination, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                Logger.error("Erro ao baixar o arquivo.")
                return False
        except Exception as e:
            Logger.error("Erro ao baixar o arquivo: {}".format(e))
            return False

    def render_map(self):
        try:
            # Baixa o arquivo TMX
            self.download_file(self.tmx_url, self.tmx_file_path)

            # Carrega o arquivo TMX
            tree = ET.parse(self.tmx_file_path)
            root = tree.getroot()

            # Itera sobre os elementos 'tileset' no arquivo TMX
            for tileset in root.iter('tileset'):
                # Obtém o nome do arquivo TSX
                tsx_filename = tileset.attrib['source']
                tsx_url = f"http://192.168.189.175:3000/api/get_tileset?filename={tsx_filename}"
                tsx_file_path = os.path.join(self.tileset_dir, tsx_filename)

                # Baixa o arquivo TSX se ainda não existir
                if not os.path.exists(tsx_file_path):
                    self.download_file(tsx_url, tsx_file_path)

            # Criando um caminho para a imagem do mapa
            map_image_path = os.path.join(self.tileset_dir, "map.png")

            # Configurações do Pygame
            pygame.init()

            # Define as dimensões do mapa
            width = int(root.attrib['width']) * int(root.attrib['tilewidth'])
            height = int(root.attrib['height']) * int(root.attrib['tileheight'])

            # Criando uma superfície para renderizar o mapa
            map_surface = pygame.Surface((width, height))

            # Itera sobre as camadas e renderiza os tiles
            for layer in root.findall('layer'):
                data = layer.find('data')
                tiles = data.text.strip().split(',')
                for idx, tile in enumerate(tiles):
                    gid = int(tile)
                    if gid != 0:
                        tileset_index = 0
                        for tileset in root.findall('tileset'):
                            firstgid = int(tileset.attrib['firstgid'])
                            if gid >= firstgid:
                                tileset_index = int(tileset.attrib['firstgid'])
                                break
                        tile_image = pygame.image.load(f"tilesets/{tsx_filename[:-4]}/{gid - tileset_index}.png")
                        x = (idx % int(root.attrib['width'])) * int(root.attrib['tilewidth'])
                        y = (idx // int(root.attrib['width'])) * int(root.attrib['tileheight'])
                        map_surface.blit(tile_image, (x, y))

            # Salvando a superfície como uma imagem
            pygame.image.save(map_surface, map_image_path)

            # Retornando o caminho da imagem do mapa renderizado
            self.map_image_path = map_image_path

        except Exception as e:
            Logger.error("Erro ao renderizar o mapa: {}".format(e))

    def get_map_image_path(self):
        if self.map_image_path is None:
            self.render_map()
        return self.map_image_path

def main(tmx_url, tileset_dir):
    renderer = MapRenderer(tmx_url, tileset_dir)
    renderer.render_map()
    return renderer.get_map_image_path()
