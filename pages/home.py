import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Home', title='DATASUS | Home')


layout = dbc.Container([
    # Titulo
    dbc.Row([
        dbc.Col(html.H2(['Sobre a Página']), 
                style={'padding':20})
    ]),

    dbc.Row([
            html.Ul([
                    html.Li("A página em questão tem como principal objetivo permitir que um amplo público, incluindo profissionais da área de saúde, pesquisadores, instituições e qualquer pessoa interessada em análises de dados de saúde pública, conduza investigações e análises estatísticas nas bases de dados públicas disponibilizadas pelo Sistema de Informação em Saúde do DataSUS, especificamente os sistemas SIM e SINAN."),
                    html.Li("Este projeto visa oferecer o suporte necessário para que os usuários da aplicação possam tomar decisões informadas com base em dados, tornando o processo de análise de informações mais simples e acessível. Nosso foco principal está em facilitar o avanço da pesquisa em saúde, simplificando a análise de dados complexos e extensos. Isso é feito com o objetivo de tornar os resultados acessíveis a todos, especialmente aos profissionais da saúde, para que possam aplicar facilmente essas informações em suas práticas e tomadas de decisão."),
                    html.Li("Para alcançar esses objetivos, a página oferece uma variedade de gráficos e visualizações que facilitam a interpretação dos dados, auxiliando na compreensão das análises realizadas. Além disso, as análises gráficas são acompanhadas de um resumo textual dos dados, com o objetivo de aprimorar a compreensão dos usuários."),
                    html.Li("As funcionalidades deste projeto incluem a apresentação de visualizações gráficas, a criação de modelos de séries temporais, a análise desses modelos e sua aplicação na previsão de observações futuras. Acreditamos que, ao disponibilizar essas análises detalhadas, os usuários poderão explorar e extrair informações significativas dos dados da saúde pública brasileira."),
                    html.Li("Importante destacar que esta página é parte integrante de um projeto acadêmico desenvolvido no âmbito da disciplina SME0808 - Séries Temporais e Aprendizado Dinâmico. Dúvidas e sugestões são bem-vindas e podem ser enviadas aos colaboradores do projeto, conforme indicado abaixo:")
                    ], style={'text-align': 'justify'}),
        ]),
    dbc.Row([        
            html.P(["Professor", html.Br(),
                    "Prof. Dr. Oilson Alberto Gonzatto Junior - Email: oilson.agjr@icmc.usp.br", html.Br(),
                    "Monitor de Graduação", html.Br(),
                    "Guilherme de Oliveira Cherobim - Email: guilherme.cherobim@usp.br", html.Br(),
                    "Equipe Discente", html.Br(),
                    "Alexandre Eduardo de Souza Jesus - Email: alexandre_souza@usp.br", html.Br(),
                    "Arthur Santorum Lorenzetto - Email: arts.lorenzetto@usp.br", html.Br(),
                    "Eduardo Zaffari Monteiro - Email: eduardozaffarimonteiro@usp.br", html.Br(),
                    "Gustavo Silva de Oliveira - Email:  gustavo.oliveira03@usp.br", html.Br(),
                    "Lucas Ivars Cadima Ciziks - Email: luciziks@usp.br", html.Br(),
                    "Paloma Botto de Medeiros Serrão - Email: palomabotto@usp.br", html.Br(),
                    "Pedro Henrique de Freitas Maçonetto - Email: pedromaconetto@usp.br"])
        ]),
])