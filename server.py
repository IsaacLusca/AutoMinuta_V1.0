from waitress import serve
import socket
import os

from autoMinuta.wsgi import application

if __name__ == '__main__':

    nome_pc = socket.gethostname()
    ip_local = socket.gethostbyname(nome_pc)
    print("Para testar no seu PC, acesse: http://localhost:8000")
    print(f"Para testar em outro PC com o nome, acesse: http://{nome_pc}:8000")
    print(f"Para testar em outro PC, acesse: http://{ip_local}:8000")
    # para acessar pelo nome do pc

    serve(application, host='0.0.0.0', port=8000)
