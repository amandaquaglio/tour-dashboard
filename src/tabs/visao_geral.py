from dash import html, dcc
import tabs.content.visao_geral.graficos as graficos
import utils.utils as utils

def layout(df):
    """Layout da aba 'Visão Geral'."""
    return html.Div([
        html.Br(),
        html.H3("Turismo no Brasil ao longo dos anos"),
        html.Br(),
        dcc.Markdown(utils.ler_markdown("visao_geral_grafico_por_ano.md")),
        dcc.Graph(id="grafico-linha-chegadas", figure=graficos.gerar_grafico_linha_chegadas(df)),
        dcc.Markdown(utils.ler_markdown("visao_geral_grafico_top_5.md")),
        dcc.Graph(id="grafico-paises-animado", figure=graficos.gerar_grafico_paises(df))
    ])  