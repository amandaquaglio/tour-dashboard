import tabs.content.visao_geral.eventos_marcantes as eventos_marcantes
def get_content():
    return eventos_marcantes.get_content_events(eventos_data, '2020', 'Resiliência e Reinvenção: O Turismo Renasce Após a Tempestade')



eventos_data = [
    {
        "ano": "2020 (Colapso)",
        "titulo": "Pandemia de COVID-19",
        "descricao": "A pandemia de COVID-19 teve um impacto devastador no turismo global, com o fechamento de fronteiras, restrições de viagens, cancelamento de voos e medidas de distanciamento social. O turismo internacional no Brasil sofreu uma queda acentuada, atingindo os níveis mais baixos da série histórica.",
        "imagem": "assets/images/2020_covid_19.jpg",
    },
    {
        "ano": "2021 (Recuperação lenta)",
        "titulo": "Vacinação",
        "descricao": "O início da vacinação contra a COVID-19 em alguns países gerou um certo otimismo e permitiu a retomada gradual das viagens internacionais.",
        "imagem": "assets/images/2021_vacinacao.jpg",
    },
    {
        "ano": "2021-2022 (Recuperação lenta)",
        "titulo": "Flexibilização das regras de entrada no país",
        "descricao": "Em meio à pandemia do COVID-19, à medida em que os casos graves e números de mortes por COVID-19 diminuía, a Anvisa começou a flexibilizar algumas exigências de entrada ao país. Em 2022, a vacinação deixou de ser obrigatória, e um teste negativo do COVID-19 era suficiente para autorizar a entrada no país.",
        "imagem": "assets/images/2022_flexibilização.jpeg",
    },
    {
        "ano": "2021 (Recuperação lenta)",
        "titulo": "Selo Turismo Responsável, Limpo e Seguro",
        "descricao": "Para incentivar o turismo e trazer mais confiança aos viajantes, o Ministério do Turismo criou o Selo Turismo Responsável, Limpo e Seguro. Este selo era concedido através de um programa que estabelecia boas práticas de higienização para cada segmento do setor. O selo era um incentivo para que os consumidores se sentissem seguros ao viajar e frequentarem locais que cumprissem protocolos específicos para a prevenção da Covid-19, posicionando o Brasil como um destino protegido e responsável.  ",
        "imagem": "assets/images/2021-turismo-responsavel.jpeg",
    },
    {
        "ano": "2021 (Recuperação lenta)",
        "titulo": "Variantes do Coronavírus",
        "descricao": "O surgimento de novas variantes do coronavírus, como a Delta e a Ômicron, gerou novas ondas de infecção e afetou a confiança dos viajantes, retardando a recuperação do turismo internacional.",
        "imagem": "assets/images/2021_variantes_corona.jpg",
    },
    {
        "ano": "2022 (Retomada Gradual)",
        "titulo": "Guerra na Ucrânia",
        "descricao": "A guerra na Ucrânia gerou incerteza econômica e aumentou os preços da energia, afetando os custos de transporte e as viagens internacionais.",
        "imagem": "assets/images/2022-guerra-ucrania.jpeg",
    },
    {
        "ano": "2023 (Retomada Gradual e Desafios Persistentes)",
        "titulo": "Fim das Restrições",
        "descricao": "Na metade do ano de 2023, a Anvisa decretou o fim das medidas de prevenção ao Covid para entrada de viajantes no Brasil, como apresentação de vacinação ou testes de COVID-19. Isto ocorreu após o anúncio do fim da emergência sanitária de importância internacional anunciada pela Organização Mundial da Saúde (OMS).",
        "imagem": "assets/images/2022_fim_restricoes.jpg",
    },
    {
        "ano": "2022-2024 (Retomada Gradual)",
        "titulo": "Inflação em muitos países",
        "descricao": "A alta da inflação em muitos países reduziu o poder de compra dos consumidores e afetou os gastos com turismo.",
        "imagem": "assets/images/2022_inflacao.png",
    },
     {
        "ano": "2022-2024 (Retomada Gradual)",
        "titulo": "Aumento da demanda",
        "descricao": "A demanda por viagens aumentou significativamente, impulsionada pela vontade de viajar após dois anos de restrições, em 2022, e seguiu crescendo em 2024, mas em um ritmo mais lento do que o esperado, devido aos desafios econômicos e geopolíticos.",
        "imagem": "assets/images/2022_aumento_demanda.png",
    },
]