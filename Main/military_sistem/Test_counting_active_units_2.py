import pandas as pd

# Carregar os DataFrames
filename = "Dados_M_OSM.ods"
df_unidades = pd.read_excel(filename, sheet_name="Unidades")
df_sheet4 = pd.read_excel(filename, sheet_name="Sheet4")

# Função para calcular o total de unidades no nível quinto
def calcular_total_nivel_quinto(row):
    # Quantidade base
    qtd_base = row["Qtd_Base"]
    
    # Multiplicadores até o nível quinto
    multiplicador_segunda = row["Multiplicador_Segunda"]
    multiplicador_terceira = row["Multiplicador_Terceira"]
    multiplicador_quarta = row["Multiplicador_Quarta"]
    multiplicador_quinta = row["Multiplicador_Quinta"]
    
    # Calcular o total de unidades no nível quinto
    total_quinto = (qtd_base *
                    multiplicador_segunda *
                    multiplicador_terceira *
                    multiplicador_quarta *
                    multiplicador_quinta)
    return total_quinto

# Calcular e adicionar a coluna `Regimento_Total_Unidades_Quinto` no DataFrame Unidades
df_unidades["Regimento_Total_Unidades_Quinto"] = df_unidades.apply(calcular_total_nivel_quinto, axis=1)

# Criar um dicionário para mapear Tipo ao total de unidades no nível quinto
regimento_to_total_quinto = df_unidades.set_index("Tipo")["Regimento_Total_Unidades_Quinto"].to_dict()

# Inicializar a nova coluna `Total_Brigada` com valor zero
df_sheet4["Total_Brigada"] = 0

# Iterar sobre as linhas do DataFrame Sheet4 para calcular `Total_Brigada`
for index, row in df_sheet4.iterrows():
    total_soldados_brigada = 0
    
    # Iterar sobre as colunas Regimento_n
    for col in [col for col in df_sheet4.columns if col.startswith("Regimento_")]:
        regimento = row[col]  # Nome do regimento na linha atual
        if pd.notna(regimento) and regimento in regimento_to_total_quinto:  # Verificar se o regimento é válido
            total_soldados_brigada += regimento_to_total_quinto[regimento]  # Somar o total de soldados no nível quinto
    
    # Atualizar o total de soldados na Brigada
    df_sheet4.at[index, "Total_Brigada"] = total_soldados_brigada

# Salvar os resultados
df_unidades.to_excel("Unidades_Com_Totais_Quinto.ods", index=False)
df_sheet4.to_excel("Contagem_Brigada.ods", index=False)

# Exibir os resultados
print("Unidades com Regimento_Total_Unidades_Quinto:")
print(df_unidades[["Tipo", "Regimento_Total_Unidades_Quinto"]].head())

print("\nSheet4 com Total_Brigada:")
print(df_sheet4[["Brigada", "Total_Brigada"]].head())
