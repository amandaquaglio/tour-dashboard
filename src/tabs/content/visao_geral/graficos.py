import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import json
import numpy as np



def aplicar_filtro(df, selected_decada, anos_selecionados=None, meses_selecionados=None, ufs_selecionadas=None, paises_selecionados=None, vias_selecionadas=None, continentes_selecionados=None):
    df['decada'] = (df['ano'] // 10) * 10
    df_decada = df[df['decada'] == selected_decada]
    df_filtrado = df_decada.copy()
    if anos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['ano'].isin(anos_selecionados)]
    if meses_selecionados:
        df_filtrado = df_filtrado[df_filtrado['mes'].isin(meses_selecionados)]
    if ufs_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['uf'].isin(ufs_selecionadas)]
    if paises_selecionados:
        df_filtrado = df_filtrado[df_filtrado['pais'].isin(paises_selecionados)]
    if vias_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['via_acesso'].isin(vias_selecionadas)]
    if continentes_selecionados:
        df_filtrado = df_filtrado[df_filtrado['continente'] == continentes_selecionados]
    return df_filtrado

def gerar_grafico_linha_chegadas(df):
    """
    Gera um gráfico de linha interativo das chegadas de turistas por ano,
    com marcadores, hover personalizado e média móvel.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados de chegadas, com as colunas 'ano' e 'chegadas'.

    Returns:
        plotly.graph_objects.Figure: Objeto Figure do Plotly contendo o gráfico.
    """

    chegadas_por_ano = df.groupby('ano')['chegadas'].sum().reset_index()

    # Criar o gráfico de linha com marcadores e linhas
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chegadas_por_ano['ano'],
        y=chegadas_por_ano['chegadas'],
        mode='markers+lines',
        name='Chegadas',  # Nome para a legenda
        hovertemplate='Ano: %{x}<br>Chegadas: %{y}<extra></extra>'  # Formato do texto ao passar o mouse
    ))

    # Adicionar a média móvel (janela de 5 anos)
    chegadas_por_ano['media_movel'] = chegadas_por_ano['chegadas'].rolling(window=5, center=True).mean()
    fig.add_trace(go.Scatter(
        x=chegadas_por_ano['ano'],
        y=chegadas_por_ano['media_movel'],
        mode='lines',
        name='Média Móvel (5 anos)',  # Nome para a legenda
        line=dict(color='rgba(0,0,0,0.5)') # Cor da linha da média móvel
    ))

    # Personalizar o layout do gráfico
    fig.update_layout(
        title='Chegadas de Turistas por ano no Brasil',
        xaxis_title='Ano',
        yaxis_title='Chegadas',
        hovermode='x unified',  # Exibe o hover de todos os traces no mesmo ano
        legend=dict(
            orientation="h",  # 'h' for horizontal
            yanchor="bottom",
            y=-0.5,  # Position below the x-axis
            xanchor="center",
            x=0.5
        )
    )

    return fig


def gerar_grafico_barras_chegadas_por_ano_decada(df, selected_decada, anos_selecionados=None, meses_selecionados=None, ufs_selecionadas=None, paises_selecionados=None, vias_selecionadas=None, continentes_selecionados=None):
    """
    Gera um gráfico de barras mostrando as chegadas por ano na década selecionada.

    Args:
        df: DataFrame com os dados.
        selected_decada: Década selecionada para filtrar os dados.
    """

    df_filtrado = aplicar_filtro(df, selected_decada=selected_decada, 
                                 anos_selecionados=anos_selecionados, 
                                 meses_selecionados=meses_selecionados, 
                                 ufs_selecionadas=ufs_selecionadas,
                                 paises_selecionados=paises_selecionados,
                                 vias_selecionadas=vias_selecionadas,
                                 continentes_selecionados=continentes_selecionados)

    # Agrupar por ano e década, somando as chegadas
    chegadas_por_ano = df_filtrado.groupby(['ano'])['chegadas'].sum().reset_index()
     # Criar lista de todos os anos da década
    anos_da_decada = list(range(int(selected_decada), int(selected_decada) + 10))

    # Criar um DataFrame com todos os anos da década e mesclar com os dados
    df_anos = pd.DataFrame({'ano': anos_da_decada})
    chegadas_por_ano = pd.merge(df_anos, chegadas_por_ano, on='ano', how='left').fillna(0)

    # Plotar o gráfico de barras
    fig = px.bar(chegadas_por_ano, x='ano', y='chegadas',
                 title=f'Chegadas por Ano na Década de {selected_decada}',
                 labels={'ano': 'Ano', 'chegadas': 'Número de Chegadas'},
                color_discrete_sequence=['#1f77b4'], text_auto=True,)

    # Adicionar tooltips informativos
    fig.update_traces(
        hovertemplate="<b>Ano:</b> %{x}<br><b>Chegadas:</b> %{y:,}"
    )
     # Ajustar o layout do gráfico
    fig.update_layout(
        xaxis={'categoryorder': 'array', 'categoryarray': anos_da_decada, 'tickmode': 'linear'},
        yaxis_title = 'Chegadas (Milhões)',
        xaxis_title = 'Ano'
    )

    return fig

def gerar_grafico_linha_chegadas_por_decada(df, selected_decada, anos_selecionados=None, meses_selecionados=None, ufs_selecionadas=None, paises_selecionados=None, vias_selecionadas=None, continentes_selecionados=None):
    """
    Gera um gráfico de linha mostrando a evolução do turismo por década.

    Args:
        df: DataFrame com os dados.

    Returns:
        Figura do Plotly Express com o gráfico de linha.
    """

    df_filtrado = aplicar_filtro(df, selected_decada=selected_decada, 
                                 anos_selecionados=anos_selecionados, 
                                 meses_selecionados=meses_selecionados, 
                                 ufs_selecionadas=ufs_selecionadas,
                                 paises_selecionados=paises_selecionados,
                                 vias_selecionadas=vias_selecionadas,
                                 continentes_selecionados=continentes_selecionados)

    # Agrupar por década e somar as chegadas
    chegadas_por_decada = df_filtrado.groupby('decada')['chegadas'].sum().reset_index()

    # Plotar o gráfico de linha
    fig = px.line(chegadas_por_decada, x='decada', y='chegadas',
                  title='Evolução do Turismo no Brasil por Década',
                  labels={'decada': 'Década', 'chegadas': 'Número de Chegadas'},
                  markers=True)

    # Adicionar tooltips informativos
    fig.update_traces(
        hovertemplate="<b>Década:</b> %{x}<br><b>Chegadas:</b> %{y:,}"
    )

    return fig


def gerar_grafico_paises(df, top_n=5):
    """
    Gera um gráfico de barras ANIMADO mostrando os top N países com mais chegadas por ano,
    exibindo todos os países que já estiveram no top N em algum momento no eixo Y.

    Args:
        df: DataFrame com os dados.
        top_n: Número de países a serem exibidos em cada barra (top N de cada ano).

    Returns:
        Figura do Plotly Express com o gráfico de barras.
    """

    # Agrupar por país e ano e somar as chegadas
    chegadas_por_pais = df.groupby(['ano', 'pais'])['chegadas'].sum().reset_index()

    # Encontrar os países que estiveram no top N em algum ano
    def top_n_por_ano(df_ano):
        return df_ano.nlargest(top_n, 'chegadas')

    top_paises_por_ano = chegadas_por_pais.groupby('ano').apply(top_n_por_ano).reset_index(drop=True)
    paises_unicos = top_paises_por_ano['pais'].unique().tolist()
    
    total_chegadas_por_pais = df[df['pais'].isin(paises_unicos)].groupby('pais')['chegadas'].sum().sort_values(ascending=True)
    paises_unicos = total_chegadas_por_pais.index.tolist()

    # Criar um DataFrame com todos os países e anos
    anos = chegadas_por_pais['ano'].unique()
    todos_os_dados = pd.DataFrame([(ano, pais) for ano in anos for pais in paises_unicos], columns=['ano', 'pais'])

    # Mesclar com os dados existentes para preencher valores ausentes com 0
    df_completo = pd.merge(todos_os_dados, chegadas_por_pais, on=['ano', 'pais'], how='left').fillna(0)

    def zerar_fora_do_top_n(df_ano, top_n):
        top_n_paises = df_ano.nlargest(top_n, 'chegadas')['pais'].tolist()
        df_ano['chegadas'] = df_ano['chegadas'].where(df_ano['pais'].isin(top_n_paises), 0)
        return df_ano

    df_zerado = df_completo.groupby('ano', group_keys=False).apply(zerar_fora_do_top_n, top_n=top_n)

    # Ordenar os dados para a animação
    df_ordenado = df_zerado.sort_values(by=['ano', 'chegadas'], ascending=[True, False])
    max_chegadas = df_ordenado['chegadas'].max()

    
    # Criar category_orders explicitamente
    category_orders = {"pais": paises_unicos}

    # Plotar o gráfico de barras
    fig = px.bar(df_ordenado, x='chegadas', y='pais', color='pais', animation_frame="ano", animation_group="pais",
                 title=f"Top {top_n} Países que Amam o Brasil",
                 labels={'pais': 'País', 'chegadas': 'Número de Chegadas'}, text_auto=True,
                 category_orders=category_orders)

    # Adicionar tooltips informativos
    fig.update_traces(
        hovertemplate="<b>País:</b> %{y}<br><b>Chegadas:</b> %{x:,}"
    )

    # Atualizar o layout para forçar a exibição de todas as categorias
    fig.update_layout(
        xaxis=dict(range=[0, max_chegadas]),
        yaxis=dict(
            categoryorder='array',
            categoryarray=category_orders['pais']  # Usar os mesmos países para a ordem
        ),
        showlegend=False
    )

    # Opcional: Personalizar a velocidade da animação
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000

    return fig

def gerar_grafico_paises_por_decada(df, selected_decada, anos_selecionados=None, meses_selecionados=None, ufs_selecionadas=None, paises_selecionados=None, vias_selecionadas=None, continentes_selecionados=None, top_n=10):
    """
    Gera um gráfico de barras mostrando os top N países com mais chegadas na década selecionada.

    Args:
        df: DataFrame com os dados.
        selected_decada: Década selecionada.
        top_n: Número de países a serem exibidos.

    Returns:
        Figura do Plotly Express com o gráfico de barras.
    """
    df_filtrado = aplicar_filtro(df, selected_decada=selected_decada, 
                                 anos_selecionados=anos_selecionados, 
                                 meses_selecionados=meses_selecionados, 
                                 ufs_selecionadas=ufs_selecionadas,
                                 paises_selecionados=paises_selecionados,
                                 vias_selecionadas=vias_selecionadas,
                                 continentes_selecionados=continentes_selecionados)

    # Agrupar por país e somar as chegadas
    chegadas_por_pais = df_filtrado.groupby('pais')['chegadas'].sum().nlargest(top_n).reset_index()

    # Plotar o gráfico de barras
    fig = px.bar(chegadas_por_pais, x='chegadas', y='pais', orientation='h',
                 title=f'Top {top_n} Países com Mais Chegadas de Turistas na Década de {selected_decada}',
                 labels={'pais': 'País', 'chegadas': 'Número de Chegadas'},text_auto=True,
                 color_discrete_sequence=['#2ca02c'],

                 )  # Escolher uma cor mais agradável

    # Adicionar tooltips informativos
    fig.update_traces(
        hovertemplate="<b>País:</b> %{y}<br><b>Chegadas:</b> %{x:,.0f}"  # Adicionar formatação ao número de chegadas
    )

    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        xaxis_title = 'Número de Chegadas (Milhões)'
    )

    return fig

def gerar_mapa_calor_uf_por_decada(df, selected_decada, anos_selecionados=None, meses_selecionados=None, ufs_selecionadas=None, paises_selecionados=None, vias_selecionadas=None, continentes_selecionados=None):
    """
    Gera um mapa de calor do Brasil mostrando as chegadas por UF na década selecionada.

    Args:
        df: DataFrame com os dados.
        selected_decada: Década selecionada.

    Returns:
        Figura do Plotly Express com o mapa de calor.
    """

    # Carregue o arquivo GeoJSON com as geometrias das UFs
    try:
        with open("src/br_states.json", "r") as f:
            geojson_brasil = json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo 'br_states.json' não encontrado.")
        return px.scatter(title="Arquivo GeoJSON não encontrado")


    df_filtrado = aplicar_filtro(df, selected_decada=selected_decada, 
                                 anos_selecionados=anos_selecionados, 
                                 meses_selecionados=meses_selecionados, 
                                 ufs_selecionadas=ufs_selecionadas,
                                 paises_selecionados=paises_selecionados,
                                 vias_selecionadas=vias_selecionadas,
                                 continentes_selecionados=continentes_selecionados)

    chegadas_por_uf = df_filtrado.groupby('uf')['chegadas'].sum().reset_index()

    # Adicionar informações detalhadas para os tooltips
    chegadas_por_uf['tooltip_text'] = chegadas_por_uf.apply(
        lambda row: f"UF: {row['uf']}<br>Chegadas: {row['chegadas']:,}", axis=1)

    # Criar o mapa de calor
    fig = px.choropleth_mapbox(chegadas_por_uf, geojson=geojson_brasil, locations='uf',
                               featureidkey='properties.Estado',
                               color='chegadas',
                               color_continuous_scale="YlGnBu",  # Paleta de cores mais agradável
                               mapbox_style="carto-positron", zoom=3, center={"lat": -15, "lon": -50},
                               title=f'Chegadas por UF na Década de {selected_decada}',
                               hover_data={'uf': False, 'chegadas': False, 'tooltip_text': True})
    
    def format_ticks(value):
        if value >= 1000000:
            return f"{value / 1000000:.0f}M"
        elif value >= 1000:
            return f"{value / 1000:.0f}K"
        else:
            return f"{value:.0f}"
    
    cmin = chegadas_por_uf['chegadas'].min()
    cmax = chegadas_por_uf['chegadas'].max()

    # Gerar os ticks (valores) da escala
    tickvals = np.linspace(cmin, cmax, num=6)

    # Formatar os ticks
    ticktext = [format_ticks(v) for v in tickvals]
    
    # Atualizar o layout para melhorar a legenda e o tooltip
    fig.update_layout(
        width=800,       
        height=600,
        margin=dict(l=20, r=20, t=50, b=50),  # Ajustar as margens
        coloraxis_colorbar=dict(
            title="Chegadas",
            tickvals=tickvals,
            ticktext=ticktext
        )
    )

    fig.update_traces(
        hovertemplate="%{customdata[0]}"  # Usar o tooltip personalizado
    )
    
    fig.update_traces(customdata=chegadas_por_uf[['tooltip_text']].values.tolist())

    return fig


def gerar_serie_temporal_pais_chegadas(df, selected_decada, paises_selecionados=None, anos_selecionados=None, meses_selecionados=None, ufs_selecionadas=None, vias_selecionadas=None, continentes_selecionados=None, top_n=10):
    """
    Gera um gráfico de linha das chegadas de um país específico ao longo dos anos.

    Args:
        df: DataFrame com os dados.
        selected_decada: Década selecionada.
        paises_selecionados: Lista de países selecionados (opcional).
        anos_selecionados: Lista de anos selecionados (opcional).
        meses_selecionados: Lista de meses selecionados (opcional).
        ufs_selecionadas: Lista de UFs selecionadas (opcional).
        top_n: O número máximo de países para exibir.

    Returns:
        Figura do Plotly Express com o gráfico de linha.
    """

    df_filtrado = aplicar_filtro(df, selected_decada=selected_decada, 
                                 paises_selecionados=paises_selecionados,
                                 anos_selecionados=anos_selecionados, 
                                 meses_selecionados=meses_selecionados, 
                                 ufs_selecionadas=ufs_selecionadas,
                                 vias_selecionadas=vias_selecionadas,
                                 continentes_selecionados=continentes_selecionados)
    
    if not paises_selecionados:
        top_paises = df_filtrado.groupby('pais')['chegadas'].sum().nlargest(top_n).index.tolist()
        df_filtrado = df_filtrado[df_filtrado['pais'].isin(top_paises)]

    # Agrupar por ano e somar as chegadas
    chegadas_por_ano = df_filtrado.groupby(['ano', 'pais'])['chegadas'].sum().reset_index()


    fig = px.line(chegadas_por_ano, x='ano', y='chegadas', color='pais',
                  title=f'Chegadas de turistas ao longo dos anos',
                  labels={'ano': 'Ano', 'chegadas': 'Número de Chegadas'})

    # Adicionar tooltips informativos
    fig.update_traces(
        mode="markers+lines",
        hovertemplate="<b>Ano:</b> %{x}<br><b>Chegadas:</b> %{y:,}"
    )

    fig.update_layout(legend=dict(
            orientation="h",  # 'h' for horizontal
            yanchor="bottom",
            y=-0.5,  # Position below the x-axis
            xanchor="center",
            x=0.5
        ))

    return fig

def gerar_grafico_vias_acesso_por_decada(df, selected_decada, anos_selecionados=None, meses_selecionados=None, ufs_selecionadas=None, paises_selecionados=None, vias_selecionadas=None, continentes_selecionados=None):
    """
    Gera um gráfico de linhas mostrando a distribuição das chegadas por via de acesso ao longo dos anos na década selecionada.

    Args:
        df: DataFrame com os dados.
        selected_decada: Década selecionada.
        anos_selecionados: Lista de anos selecionados (opcional).
        meses_selecionados: Lista de meses selecionados (opcional).
        ufs_selecionadas: Lista de UFs selecionadas (opcional).

    Returns:
        Figura do Plotly Express com o gráfico de linhas.
    """

    df_filtrado = aplicar_filtro(df, selected_decada=selected_decada, 
                                 anos_selecionados=anos_selecionados, 
                                 meses_selecionados=meses_selecionados, 
                                 ufs_selecionadas=ufs_selecionadas,
                                 paises_selecionados=paises_selecionados,
                                 vias_selecionadas=vias_selecionadas,
                                 continentes_selecionados=continentes_selecionados)
    

    # Agrupar por via de acesso e somar as chegadas
    chegadas_por_ano = df_filtrado.groupby(['via_acesso','ano'])['chegadas'].sum().reset_index()

    # Filtrar vias de acesso com poucas chegadas (exemplo: remover vias com menos de 1000 chegadas)
    chegadas_por_ano = chegadas_por_ano[chegadas_por_ano['chegadas'] > 1000]

    # Plotar o gráfico de linhas
    fig = px.line(chegadas_por_ano, x='ano', y='chegadas',color='via_acesso',
                 title=f'Chegadas de Turistas por Via de Acesso na Década de {selected_decada}',
                 labels={'ano': 'Ano', 'chegadas': 'Número de Chegadas', 'via_acesso': 'Via de Acesso'})

    # Adicionar tooltips informativos
    fig.update_traces(
        mode="markers+lines",
        hovertemplate="<b>Ano:</b> %{x}<br><b>Via de Acesso:</b> %{data.name}<br><b>Chegadas:</b> %{y:,}"
    )


    fig.update_layout(
        yaxis_title = 'Número de Chegadas',
        legend=dict(
            orientation="h",  # 'h' for horizontal
            yanchor="bottom",
            y=-0.5,  # Position below the x-axis
            xanchor="center",
            x=0.5
        )
    )
    
    return fig