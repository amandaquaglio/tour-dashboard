from dash import html, dcc
import dash_bootstrap_components as dbc
import tabs.content.visao_geral.eventos_marcantes_90 as eventos_marcantes_90
import tabs.content.visao_geral.eventos_marcantes_2000 as eventos_marcantes_2000
import tabs.content.visao_geral.eventos_marcantes_2010 as eventos_marcantes_2010
import tabs.content.visao_geral.eventos_marcantes_2020 as eventos_marcantes_2020
import utils.utils as utils


def layout(df, app):
    """Layout da aba 'Evolução do Turismo por Década'."""
    min_decada = 1990 // 10 * 10
    max_decada = 2020

    anos_options = [{'label': str(ano), 'value': ano} for ano in sorted(df['ano'].unique())]

    # Crie a lista de meses ordenados
    meses_options = [{'label': mes, 'value': mes} for mes in [
        "janeiro", "fevereiro", "março", "abril",
        "maio", "junho", "julho", "agosto",
        "setembro", "outubro", "novembro", "dezembro"
    ]]
    
    continentes_options = [{'label': continente, 'value': continente} for continente in sorted(df['continente'].unique())]

    pais_options = [{'label': pais, 'value': pais} for pais in sorted(df['pais'].unique())]
    

    ufs_options = [{'label': uf, 'value': uf} for uf in sorted(df['uf'].unique())]

    vias_options = [{'label': via, 'value': via} for via in sorted(df['via_acesso'].unique())]


    return html.Div([
        html.Br(),
        html.H3("Um mergulho em cada década do Turismo no Brasil"),
        html.Br(),
        dcc.Markdown(utils.ler_markdown("evolucao_decadas_intro.md")),
        html.Br(),
        html.H4("Selecione a década"),
        dbc.Row([
            dbc.Col(dcc.Slider(
                id='decada-slider',
                min=min_decada,
                max=max_decada,
                step=10,
                marks={i: f'{i}' for i in range(min_decada, max_decada + 10, 10)},
                value=1990,
                ),md=8)  # Largura do Slider
        ]),
        html.Br(),
        html.Button("Mostrar/Ocultar Filtros", id="mostrar-filtros", n_clicks=0),
        html.Div(id="filtros-container", children=[ 
            html.Br(),
            html.H4("Filtros"),
            html.Div("Selecione os filtros abaixo para otimizar suas análises"),
            dbc.Row([
                dbc.Col(dcc.Dropdown(
                id='ano-dropdown',
                options=anos_options,
                multi=True,
                placeholder="Selecione os Anos"
                )),
                dbc.Col(dcc.Dropdown(
                id='mes-dropdown',
                options=meses_options,
                multi=True,
                placeholder="Selecione os Meses"
                )),
                dbc.Col(dcc.Dropdown(
                id='continente-dropdown',
                options=continentes_options,
                multi=False,
                placeholder="Selecione os Continentes"
                )),
                dbc.Col(dcc.Dropdown(
                id='pais-dropdown',
                options=pais_options,
                multi=True,
                placeholder="Selecione os Países"
                )),
                dbc.Col(dcc.Dropdown(
                id='uf-dropdown',
                options=ufs_options,
                multi=True,
                placeholder="Selecione as UFs"
                )),
                dbc.Col(dcc.Dropdown(
                id='via-acesso-dropdown',
                options=vias_options,
                multi=True,
                placeholder="Selecione as Vias de acesso"
                ))
            ]),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='chegadas-decada-graph'), width="90%"),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(id="mapa-calor-uf-decada", style={'width': '100%'}), md=6),
            dbc.Col(dcc.Graph(id="grafico-paises-decada", style={'width': '100%'}), md=6),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(id="grafico-vias-decada", style={'width': '96%'}), md=6),
            dbc.Col(dcc.Graph(id="grafico-pais-time-series", style={'width': '100%'}), md=6),
        ]),
        html.Div(id='decada-content', children=[  # Div para conter o conteúdo das décadas
            html.Div(id='1990s', style={'display': 'none'}, children=[  # Ocultar inicialmente
                eventos_marcantes_90.get_content()
            ]),
             html.Div(id='2000s', style={'display': 'none'}, children=[  # Ocultar inicialmente
                eventos_marcantes_2000.get_content()
            ]),
            html.Div(id='2010s', style={'display': 'none'}, children=[  # Ocultar inicialmente
                eventos_marcantes_2010.get_content()
            ]),
            html.Div(id='2020s', style={'display': 'none'}, children=[  # Ocultar inicialmente
                eventos_marcantes_2020.get_content()

            ]),
        ]),
    ])