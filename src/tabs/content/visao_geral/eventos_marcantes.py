from dash import html, dcc
import dash_bootstrap_components as dbc
import utils.utils as utils

def get_content_events(eventos, decada, titulo_decada):
    """
    Gera o conteúdo da linha do tempo com base nos dados dos eventos,
    incluindo imagens e alternando a posição das imagens.
    """
    num_colunas = 3  # Define o número de colunas (pode ser 2 ou 3)
    eventos_por_coluna = [eventos[i::num_colunas] for i in range(num_colunas)]

    # Cria as colunas com os eventos
    colunas = []
    for coluna_eventos in eventos_por_coluna:
        eventos_html = []
        for evento in coluna_eventos:
            eventos_html.append(
                dbc.Card(
                    dbc.CardBody([
                        html.Img(src=evento["imagem"], className="img-fluid rounded", style={'marginBottom': '10px'}),
                        html.H6(evento["ano"] + " - " + evento["titulo"], className="card-title"),
                        html.P(evento["descricao"], className="card-text")
                    ]),
                    className="mb-4 event-card"  # Adiciona um espaçamento abaixo de cada card
                )
            )
        colunas.append(dbc.Col(eventos_html, md=4))  # Ajusta para md=6 para duas colunas, md=4 para três

    return html.Div([
        html.H4(f"{decada}: {titulo_decada}", className="text-center mb-3"),
        html.Br(),
        html.H5(f"Resumo"),
        
        html.Div(dcc.Markdown(utils.ler_markdown(f"decada_{decada}.md")), style={
            "backgroundColor": "#f0f0f0", 
            "padding": "15px",  
            "borderRadius": "5px", 
            "marginBottom": "15px"
        }),
        html.H5(f"Fatos Relevantes que podem ter impactado o Turismo da Década de {decada}", className="text-center mb-4"),
        dbc.Row(colunas)  # Linha para as colunas
    ], className="container mt-4")
