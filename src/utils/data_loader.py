import pandas as pd

def load_data():
    """Carrega e trata os dados do arquivo CSV."""
    try:
        df = pd.read_csv('src/data/turismo_brasil_1989_2024_tratado.csv', encoding='utf-8')
    except FileNotFoundError:
        print("Erro: Arquivo 'src/data/turismo_brasil_1989_2024_tratado.csv' não encontrado.")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

    # Renomear colunas para facilitar o uso
    df = df.rename(columns={
        'continente': 'continente',
        'cod_continente': 'cod_continente',
        'pais': 'pais',
        'cod_pais': 'cod_pais',
        'uf': 'uf',
        'cod_uf': 'cod_uf',
        'cod_via_acesso': 'cod_via_acesso',
        'ano': 'ano',
        'mes': 'mes',
        'cod_mes': 'cod_mes',
        'chegadas': 'chegadas',
        'via_acesso': 'via_acesso',
        'mes_num': 'mes_num'
    })

    # Converter colunas para tipos apropriados
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce').fillna(0).astype(int)
    df['mes_num'] = pd.to_numeric(df['mes_num'], errors='coerce').fillna(0).astype(int)
    df['chegadas'] = pd.to_numeric(df['chegadas'], errors='coerce').fillna(0).astype(int)
    df['cod_continente'] = pd.to_numeric(df['cod_continente'], errors='coerce').fillna(0).astype(int)
    df['cod_pais'] = pd.to_numeric(df['cod_pais'], errors='coerce').fillna(0).astype(int)
    df['cod_uf'] = pd.to_numeric(df['cod_uf'], errors='coerce').fillna(0).astype(int)
    df['cod_mes'] = pd.to_numeric(df['cod_mes'], errors='coerce').fillna(0).astype(int)
    df['cod_via_acesso'] = pd.to_numeric(df['cod_via_acesso'], errors='coerce').fillna(0).astype(int)

    # Converter a coluna 'mes' para minúsculas para consistência
    df['mes'] = df['mes'].str.lower()

    # Remover linhas onde 'pais' é nulo
    df = df.dropna(subset=['pais'])

    # Remover linhas onde 'chegadas' é nulo
    df = df.dropna(subset=['chegadas'])  

    # Criar dict continentes com lista de países
    continentes_dict = df.groupby('continente')['pais'].apply(lambda x: x.unique().tolist()).to_dict()

    # Criar dict paises com o continente
    pais_continente_dict = df.set_index('pais')['continente'].to_dict()
   
   
    # Agrupar por país e ano e somar as chegadas
    chegadas_por_pais = df.groupby(['ano', 'pais'])['chegadas'].sum().reset_index()

    # Encontrar os países que estiveram no top N em algum ano
    def top_n_por_ano(df_ano):
        return df_ano.nlargest(5, 'chegadas')

    top_paises_por_ano = chegadas_por_pais.groupby('ano').apply(top_n_por_ano).reset_index(drop=True)
    paises_unicos = top_paises_por_ano['pais'].unique().tolist()

    # Criar um DataFrame com todos os países e anos
    anos = chegadas_por_pais['ano'].unique()

    todos_os_dados = pd.DataFrame([(ano, pais) for ano in anos for pais in paises_unicos], columns=['ano', 'pais'])

    # Mesclar com os dados existentes para preencher valores ausentes com 0
    df_completo = pd.merge(todos_os_dados, chegadas_por_pais, on=['ano', 'pais'], how='left').fillna(0)

    def zerar_fora_do_top_n(df_ano, top_n):
        top_n_paises = df_ano.nlargest(top_n, 'chegadas')['pais'].tolist()
        df_ano['chegadas'] = df_ano['chegadas'].where(df_ano['pais'].isin(top_n_paises), 0)
        return df_ano

    df_zerado = df_completo.groupby('ano', group_keys=False).apply(zerar_fora_do_top_n, top_n=5)

    df_ordenado = df_zerado.sort_values(by=['ano', 'chegadas'], ascending=[True, False])
    print(df_ordenado[df_ordenado['ano']==2024])

    return df, continentes_dict, pais_continente_dict