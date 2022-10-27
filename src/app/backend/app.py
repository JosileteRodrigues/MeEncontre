from flask import Flask, request, Response
from flask_migrate import Migrate
from models import db
from models import User
import os
import sqlite3
from apikey import ME_ENCONTRE_GOOGLE_API_KEY
import requests
from flask_cors import CORS, cross_origin#conjunto de opções para permitir requisições

# Iniciar app
app = Flask(__name__)
CORS(app)#especifica qual aplicativo o cors vai usar que é app

cors = CORS(app, resources={r"/*": {"origins": "*"}})#inicia o cors novamente com os recursos do cors. pega tds as url da api(listar, cadastrar e a raiz) e add ao origins que é o cabeçalho da requisição e dizendo que qlq site pode usar essa api

#Configuracoes do banco de dados no app
basedir = os.path.abspath(os.path.dirname(__file__))
print(os.path.join(basedir, 'database.sqlite3'))
app.config['CORS_HEADERS'] = 'Allow-Origin'#especifica de qual onde vai vir a requisição, especifica qual cabeçalho o cors vai usar que significa permitir origen
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite3')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['AUTOCRUD_METADATA_ENABLED'] = True
#Conectar ao banco de dados ou cria caso ainda nao exista
con = sqlite3.connect('./database.sqlite3')
db.init_app(app)
migrate = Migrate(app, db)


def add_to_db(new_user:dict):
    """Adiciona o novo usuario no banco de dados

    Args:
        new_user (dict): json com os dados do usuario

    Returns:
        Response: resposta com o status
    """    
    try:
        #verifica se o tipo esta correto
        if type(new_user['email']) != type(str()) or type(new_user['senha']) != type(str()):
            return Response('o campo "email" e "senha" devem ser string', status=400)
        
        email = new_user['email']
        senha = new_user['senha']
        #cria um novo objeto usuario para adicionar no db
        new_user = User(email=email, password=senha)
        #adiconar novo usuario ao banco de dados
        db.session.add(new_user)
        db.session.commit()
        return Response('Novo usuario adicionado com sucesso', status=200)
    except:
        return Response('Erro inesperado ao adicionar novo usuario', status=500)


def buscar_item_no_mapa(item:dict):
    """Buscar item no mapa a partir da API do google

    Args:
        item (dict): item para buscar

    Returns:
        Response: se tiver algum erro
        or
        List: lista com jsons com os dados dos lugares
    """
    try:
        if type(item['estado']) != type(str()) or type(item['cidade']) != type(str())or type(item['item']) != type(str()):
                return Response('o campo "estado","cidade" e "item" devem ser string', status=400)
        text_input = item['item'] + ' ' + item['cidade'] + ' ' + item['estado']
        #Substitui os espaços para a url
        text_input = text_input.replace(' ', '%20')
        print(text_input)
        #Formata a url pra fazer a requisicao
        url = rf"https://maps.googleapis.com/maps/api/place/textsearch/json?query={text_input}&key={ME_ENCONTRE_GOOGLE_API_KEY}"
        print(url)
        #fazer a requisicao
        payload={}
        headers = {}
        req = requests.get(url=url, headers=headers, data=payload)
        #Envia o campo results da requisicao para ser formatada
        return format_places(req.json()['results'])
    except:
        return Response('Erro inesperado ao buscar item no mapa', status=500)


def format_places(places:list):
    """_summary_

    Args:
        places (list): lista de lugares

    Returns:
        Response: se tiver algum erro
        or
        List: lista com jsons com os dados dos lugares
    """    
    try:
        places_list = []
        for pla in places:
            places_list.append(
                {'nome': pla['name'],
                'endereco': pla['formatted_address'],
                'rating': pla['rating']
                }
            )
        
        return places_list
    except:
        return Response('Erro inesperado ao adicionar os lugares na lista', status=500)


@app.route('/', methods=['GET'])
@cross_origin()#ao iniciar a rota, permite puxar as informações do origin importado e alterar oq for necessario nas respostas de requisição, para as origens já estarem permitidas
def index():
    if request.method == 'GET':
        return 'funcionando'


@app.route('/cadastrar', methods=['POST'])
@cross_origin()#ao iniciar a rota, permite puxar as informações do origin importado e alterar oq for necessario nas respostas de requisição, para as origens já estarem permitidas
def cadastrar_usuario():
    return add_to_db(request.get_json())


@app.route('/listar', methods=['POST'])
@cross_origin()#ao iniciar a rota, permite puxar as informações do origin importado e alterar oq for necessario nas respostas de requisição, para as origens já estarem permitidas
def listar_itens():
    return buscar_item_no_mapa(request.get_json())

    
if __name__ == '__main__':
    #db.create_all()
    app.run(host='0.0.0.0', port=5000)#usar o endereço que estiver disponivel

