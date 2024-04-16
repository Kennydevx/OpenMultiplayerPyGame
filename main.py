# main.py

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from database import authenticate_user, get_player_names, check_player_status, update_player_status, create_account, create_character
from map_script import main as render_map
from viewport_screen import ViewportScreen
from kivy.uix.image import Image
from kivy.uix.label import Label
import os


# Carrega os arquivos kv
Builder.load_file('kv/login.kv')
Builder.load_file('kv/create_account.kv')
Builder.load_file('kv/viewport.kv')  # Carrega o conteúdo do arquivo viewport.kv


class LoginScreen(Screen):
    def go_to_create_account(self):
        self.manager.current = 'create_account'
        
    def login(self):
        print("Método login chamado")
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        print(f"Valor de username: {username}")
        print(f"Valor de password: {password}")
        if username and password:  # Verifica se os campos de usuário e senha não estão vazios
            account_id = authenticate_user(username, password)
            if account_id:
                player_names = get_player_names(account_id)
                print("Nomes de jogadores obtidos:", player_names)
                # Verifica se o Spinner existe antes de atualizar os valores
                if 'character_spinner' in self.ids:
                    self.update_character_list(player_names)
                else:
                    print("Spinner de personagens não encontrado.")
                    self.add_widget(Label(text='Erro: Spinner de personagens não encontrado.', color=(1, 0, 0, 1)))
            else:
                print("Credenciais inválidas.")
                self.add_widget(Label(text='Credenciais inválidas. Tente novamente.', color=(1, 0, 0, 1)))
        else:
            print("Campos de usuário e/ou senha vazios.")
            self.add_widget(Label(text='Erro: Campos de usuário e/ou senha vazios.', color=(1, 0, 0, 1)))

    def update_character_list(self, player_names):
        print("Método update_character_list chamado")
        # Verifica se o Spinner existe antes de atualizar os valores
        if 'character_spinner' in self.ids:
            spinner = self.ids.character_spinner
            spinner.values = [str(name[0]) for name in player_names]
            print("Valores do Spinner atualizados:", spinner.values)
        else:
            print("Spinner de personagens não encontrado.")
            self.add_widget(Label(text='Erro: Spinner de personagens não encontrado.', color=(1, 0, 0, 1)))

    def select_character(self, character_name):
        account_id = authenticate_user(self.ids.username_input.text, self.ids.password_input.text)
        if account_id:
            character_status = check_player_status(account_id, character_name)
            if character_status == 0:
                update_player_status(account_id, character_name, 1)  # Altera para online
                self.manager.current = 'viewport'  # Muda para a tela do viewport
                viewport_screen = self.manager.get_screen('viewport')  # Obtém a instância da tela do viewport
                if viewport_screen:
                    print("Tela do viewport encontrada.")
                    viewport_screen.show_loading_message()  # Exibe uma mensagem de carregamento na viewport
                else:
                    print("Erro: Tela do viewport não encontrada.")
                tmx_url = "http://192.168.189.175:3000/api/get_map_tmx"  # URL do arquivo TMX
                tileset_dir = os.path.join(os.getcwd(), "tilesets")  # Diretório onde os arquivos TSX serão salvos
                map_image_path = render_map(tmx_url, tileset_dir)  # Renderiza o mapa e obtém o caminho da imagem
                print("Caminho da imagem do mapa renderizado:", map_image_path)  # Adiciona print para verificar o caminho da imagem
                if viewport_screen:
                    viewport_screen.show_map(map_image_path)  # Exibe o mapa renderizado no viewport
                else:
                    print("Erro: Tela do viewport não encontrada.")
            else:
                self.add_widget(Label(text='Personagem online. Por favor, escolha outro.', color=(1, 0, 0, 1)))
        else:
            self.add_widget(Label(text='Erro ao autenticar. Tente novamente.', color=(1, 0, 0, 1)))
    

class CreateAccountScreen(Screen):
    def create_account_and_character(self):
        new_username = self.ids.new_username_input.text
        new_password = self.ids.new_password_input.text
        new_character_name = self.ids.new_character_input.text

        # Verifica se os campos de usuário, senha e nome do personagem estão vazios
        if not new_username or not new_password or not new_character_name:
            print("Campos de usuário, senha ou nome do personagem vazios.")
            self.add_widget(Label(text='Erro: Campos de usuário, senha ou nome do personagem vazios.', color=(1, 0, 0, 1)))
            return

        print("Novo nome do personagem:", new_character_name)  # Adicionando instrução de impressão

        account_id = create_account(new_username, new_password)  # Obtendo o ID da conta criada

        if account_id:
            if create_character(account_id, new_character_name):
                self.manager.current = 'login'  # Retorna à tela de login após criar a conta
            else:
                self.add_widget(Label(text='Erro ao criar personagem.', color=(1, 0, 0, 1)))
        else:
            self.add_widget(Label(text='Erro ao criar conta.', color=(1, 0, 0, 1)))

class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        
        # Adicionando as telas ao gerenciador de telas
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(CreateAccountScreen(name='create_account'))
        self.screen_manager.add_widget(ViewportScreen(name='viewport'))  # Adiciona a tela do viewport

        return self.screen_manager

if __name__ == '__main__':
    MyApp().run()
