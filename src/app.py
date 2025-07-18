import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import tabs.content.visao_geral.graficos as graficos
import utils.utils as utils

# Importar o conteúdo das abas
from tabs import evolucao_decada, visao_geral
from utils import data_loader  # Importe o módulo data_loader

# Carregar os dados
df, continentes_dict, pais_continente_dict = data_loader.load_data()

# https://dados.gov.br/dados/conjuntos-dados/estimativas-de-chegadas-de-turistas-internacionais-ao-brasil

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.H2("Turismo no Brasil: Uma Jornada Através das Décadas"),
    dbc.Row([
    dbc.Col(
        html.Video(
            autoPlay=True,
            loop=True,
            width="100%",
            height="100%",  # Ajustar altura do vídeo
            src="/assets/header_video.mp4"),
        className="same-height",
        width=5,
    ),
    dbc.Col([
        html.Br(),
        html.Div(
            dcc.Markdown(utils.ler_markdown("introducao.md")), 
            className="intro-text"
        ),
    ], className="same-height",        
    width=7,
    )
    ]),
    html.P([
                dcc.Markdown(utils.ler_markdown("rodape.md"),link_target="_blank"), 
                ]),
    html.Br(),
    dbc.Tabs([
        dbc.Tab(label="Visão Geral", tab_id="visao-geral"),
        dbc.Tab(label="Evolução do Turismo por Década", tab_id="evolucao-decada"),
    ], id="tabs", active_tab="visao-geral"),
    html.Div(id="content"),
])

@app.callback(
    [Output("content", "children"),
     Output("url", "href")],
    [Input("tabs", "active_tab")]
)
def update_content_and_url(active_tab):
    # Update content based on active tab
    if active_tab == "visao-geral":
        content = visao_geral.layout(df)
    elif active_tab == "evolucao-decada":
        content = evolucao_decada.layout(df, app)
    else:
        content = html.P("Erro: Aba não encontrada")

    # Update URL based on active tab
    url = f"/#{active_tab}"
    
    return content, url

# Callback to update the active tab based on the URL change
@app.callback(
    Output("tabs", "active_tab"),
    [Input("url", "href")]
)
def update_tab_based_on_url(href):
    if "#evolucao-decada" in href:
        return 'evolucao-decada'
    elif "#visao-geral" in href:
        return 'visao-geral'
    else:
        return dash.no_update

# # Callback para atualizar o conteúdo das abas
# @app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
# def atualizar_content(active_tab):
#     if active_tab == "visao-geral":
#         return visao_geral.layout(df)  # Passe o DataFrame como argumento
#     elif active_tab == "evolucao-decada":
#         return evolucao_decada.layout(df, app)  # Passe o DataFrame e o app
#     return html.P("Erro: Aba não encontrada")
    

@app.callback(
    Output("filtros-container", "style"),
    [Input("mostrar-filtros", "n_clicks")],
)
def toggle_filtros(n_clicks):
    """Mostra ou oculta os filtros com um clique no botão."""
    if n_clicks % 2 == 0:
        return {'display': 'none'}  # Oculta os filtros
    else:
        return {'display': 'block'} 
    
@app.callback(
    [Output('chegadas-decada-graph', 'figure'),
    Output('grafico-paises-decada', 'figure'),
    Output('mapa-calor-uf-decada', 'figure'),
    Output('grafico-vias-decada', 'figure'),
    Output('grafico-pais-time-series', 'figure'),
    Output('ano-dropdown', 'options'),
    Output('continente-dropdown', 'options'),
    Output('pais-dropdown', 'options'),
    ],
    [Input('decada-slider', 'value'),
     Input('ano-dropdown', 'value'),
     Input('mes-dropdown', 'value'),
     Input('uf-dropdown', 'value'),
     Input('pais-dropdown', 'value'),
     Input('via-acesso-dropdown', 'value'),
     Input('continente-dropdown', 'value')
    ]
)
def update_visao_geral_graficos(selected_decada, anos_selecionados, meses_selecionados, ufs_selecionadas, paises_selecionados, vias_selecionadas, continentes_selecionados):
    anos_na_decada = [ano for ano in df['ano'].unique() if selected_decada <= ano < selected_decada + 10]
    anos_options = [{'label': str(ano), 'value': ano} for ano in sorted(anos_na_decada)]
    continentes_options = df['continente'].unique()
    paises_options = df['pais'].unique()

    if continentes_selecionados and not paises_selecionados:
        paises_options = [
        {'label': pais, 'value': pais}
        for pais in sorted(continentes_dict[continentes_selecionados])
        ]
        
    if paises_selecionados and not continentes_selecionados:
       continentes_options = [
        {'label': pais_continente_dict[pais], 'value': pais_continente_dict[pais]}
        for pais in paises_selecionados if pais in pais_continente_dict
        ]

    return graficos.gerar_grafico_barras_chegadas_por_ano_decada(df, selected_decada=selected_decada, 
                                                                 anos_selecionados=anos_selecionados, 
                                                                 meses_selecionados=meses_selecionados, ufs_selecionadas=ufs_selecionadas, 
                                                                 paises_selecionados=paises_selecionados,
                                                                 vias_selecionadas=vias_selecionadas,
                                                                 continentes_selecionados=continentes_selecionados), \
        graficos.gerar_grafico_paises_por_decada(df, selected_decada=selected_decada, 
                                                                 anos_selecionados=anos_selecionados, 
                                                                 meses_selecionados=meses_selecionados, ufs_selecionadas=ufs_selecionadas, 
                                                                 paises_selecionados=paises_selecionados,
                                                                 vias_selecionadas=vias_selecionadas,
                                                                 continentes_selecionados=continentes_selecionados), \
        graficos.gerar_mapa_calor_uf_por_decada(df, selected_decada=selected_decada, 
                                                                 anos_selecionados=anos_selecionados, 
                                                                 meses_selecionados=meses_selecionados, ufs_selecionadas=ufs_selecionadas, 
                                                                 paises_selecionados=paises_selecionados,
                                                                 vias_selecionadas=vias_selecionadas,
                                                                 continentes_selecionados=continentes_selecionados), \
        graficos.gerar_grafico_vias_acesso_por_decada(df, selected_decada=selected_decada, 
                                                                 anos_selecionados=anos_selecionados, 
                                                                 meses_selecionados=meses_selecionados, ufs_selecionadas=ufs_selecionadas, 
                                                                 paises_selecionados=paises_selecionados,
                                                                 vias_selecionadas=vias_selecionadas,
                                                                 continentes_selecionados=continentes_selecionados), \
        graficos.gerar_serie_temporal_pais_chegadas(df, selected_decada=selected_decada, 
                                                                 anos_selecionados=anos_selecionados, 
                                                                 meses_selecionados=meses_selecionados, ufs_selecionadas=ufs_selecionadas, 
                                                                 paises_selecionados=paises_selecionados,
                                                                 vias_selecionadas=vias_selecionadas,
                                                                 continentes_selecionados=continentes_selecionados), \
        anos_options, continentes_options, paises_options

@app.callback(
    [Output(f'{decada}s', 'style') for decada in range(1990, 2030, 10)],
    [Input('decada-slider', 'value')]
)
def toggle_decada_content(selected_decada):
    """Mostra o conteúdo da década selecionada e oculta as outras."""
    styles = []
    for decada in range(1990, 2030, 10):
        if decada == selected_decada:
            styles.append({'display': 'block'})
        else:
            styles.append({'display': 'none'})
    return styles

if __name__ == "__main__":
    app.run(debug=True)

