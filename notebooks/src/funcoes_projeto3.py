import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import (
    levene,
    shapiro,
    wilcoxon
)
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

def carregar_notas_alunos():
    """
    Conecta ao banco de dados SQL Server e retorna um DataFrame
    com id_aluno, nota_diagnostico e nota_final.
    """

    # carrega variáveis de ambiente do arquivo .env
    load_dotenv(dotenv_path=".env")

    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER")

    connection_string = (
        f"mssql+pyodbc://@{server}/{database}"
        f"?driver={driver.replace(' ', '+')}&trusted_connection=yes"
    )

    # cria engine
    engine = create_engine(connection_string)

    # query
    query = """
    SELECT 
        a.id_aluno,
        SUM(CASE WHEN ts.descricao = 'Diagnostico' THEN f.acertou ELSE 0 END) AS nota_diagnostico,
        SUM(CASE WHEN ts.descricao = 'Final' THEN f.acertou ELSE 0 END) AS nota_final
    FROM Fato_Respostas f
    INNER JOIN Dim_Questoes q ON f.id_questao = q.id_questao
    INNER JOIN Dim_Simulados s ON q.id_simulado = s.id_simulado
    INNER JOIN Dim_Tipo_Simulado ts ON s.id_tipo = ts.id_tipo
    INNER JOIN Dim_Alunos a ON f.id_aluno = a.id_aluno
    WHERE ts.descricao IN ('Diagnostico', 'Final')
    GROUP BY a.id_aluno
    ORDER BY a.id_aluno;
    """

    # executa e retorna dataframe
    df = pd.read_sql(query, engine)
    return df



def teste_shapiro(series, nome_coluna):
    """Executa o teste de Shapiro-Wilk e retorna interpretação."""
    stat, p = shapiro(series)
    resultado = (
        f"Shapiro ({nome_coluna}): stat={stat:.3f}, p={p:.3f} - "
        + ("A distribuição segue aproximadamente normal."
           if p > 0.05 else
           "A distribuição **não segue** uma distribuição normal.")
    )
    return resultado


def teste_levene(series1, series2, nome1="Grupo 1", nome2="Grupo 2"):
    """Executa o teste de Levene para igualdade de variâncias."""
    stat, p = levene(series1, series2)
    resultado = (
        f"Levene ({nome1} vs {nome2}): stat={stat:.3f}, p={p:.3f} - "
        + ("As variâncias podem ser consideradas iguais."
           if p > 0.05 else
           "As variâncias são diferentes.")
    )
    return resultado



def teste_wilcoxon(series1, series2, nome1="Grupo 1", nome2="Grupo 2"):
    """Executa o teste de Wilcoxon para amostras pareadas."""
    stat, p = wilcoxon(series1, series2)
    resultado = (
        f"Wilcoxon ({nome1} vs {nome2}): stat={stat:.3f}, p={p:.3f} - "
        + ("Não rejeitamos H0: não há diferença significativa entre os grupos."
           if p > 0.05 else
           "Rejeitamos H0: há diferença significativa entre os grupos.")
    )
    return resultado