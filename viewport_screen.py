# viewport_screen.py

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import Image


class ViewportScreen(Screen):
    def show_map(self, map_image_path):
        # Limpa qualquer widget existente na tela do viewport
        self.clear_widgets()

        # Adiciona o Image com o mapa renderizado diretamente ao viewport
        map_image = Image(source=map_image_path, allow_stretch=True, keep_ratio=False)

        # Definindo a posição e o tamanho do mapa
        map_image.size_hint = (None, None)  # Desativando o ajuste automático de tamanho
        map_image.size = (1024, 1024)  # Definindo o tamanho do mapa
        map_image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Centralizando o mapa na tela

        self.add_widget(map_image)

        print("Imagem do mapa carregada:", map_image.source)  # Verifica o caminho da imagem
        print("Tamanho da imagem do mapa:", map_image.texture_size)  # Verifica o tamanho da imagem


    def show_loading_message(self):
        # Limpa qualquer widget existente na tela do viewport
        self.clear_widgets()

        # Adiciona uma mensagem de carregamento
        loading_label = Label(text='Carregando...', font_size=24)
        self.add_widget(loading_label)
