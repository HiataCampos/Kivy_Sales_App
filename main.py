from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests
from bannervenda import BannerVenda
import os
from functools import partial

GUI = Builder.load_file("main.kv")


class MainApp(App):
    id_usuario = 1

    def build(self):
        return GUI

    def on_start(self):

        arquivos = os.listdir("icones/fotos_perfil")
        pagina_fotoperfil = self.root.ids['fotoperfilpage']
        lista_fotos = pagina_fotoperfil.ids['lista_fotos_perfil']
        for foto in arquivos:
            imagem = ImageButton(source=f'icones/fotos_perfil/{foto}',
                                 on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)
        #carrega informações do usuario
        self.carregar_infos_usuario()

    def carregar_infos_usuario(self):
        #Pegar informações do usuario
        requisicao = requests.get(f"https://appkivy-a225c-default-rtdb.firebaseio.com/{self.id_usuario}.json")
        requisicao_dic = requisicao.json()

        #Preencher foto de perfil
        avatar = requisicao_dic['avatar']
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        #Preencher Lista de Vendas
        vendas = requisicao_dic['vendas'][1:]
        pagina_homepage = self.root.ids['homepage']
        lista_vendas = pagina_homepage.ids["lista_vendas"]
        for venda in vendas:
            print(venda)
            banner = BannerVenda(
                cliente=venda['cliente'], data_venda=venda['data'],
                foto_cliente=venda['foto_cliente'], foto_produto=venda['foto_produto'],
                preco=venda['preco'], produto=venda['produto'],
                quantidade=venda['quantidade'], unidade=venda['unidade'])

            lista_vendas.add_widget(banner)


    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela

    def mudar_foto_perfil(self, foto, *args):
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{foto}"

        """
            Para atualizar informações no Firebase precisamos passar como texto conforme
            o exemplo abaixo. Utilizando {{}}, colchetes duplos dom o f string.
            Colocar todas os valores entre apas duplas. Garantindo que o valor das váriaves
            fiquem corretas.
        """

        info = f'{{"avatar": "{foto}"}}'
        requisicao = requests.patch(f'https://appkivy-a225c-default-rtdb.firebaseio.com/{self.id_usuario}.json',
                                    data=info)

        self.mudar_tela("ajustespage")

MainApp().run()
