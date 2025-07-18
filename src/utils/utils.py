import os
def ler_markdown(nome_arquivo):
    caminho_arquivo = os.path.join(os.path.dirname(__file__), '../assets/texts', nome_arquivo)
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        return f.read()