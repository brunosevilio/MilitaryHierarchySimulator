import pandas as pd

# Carregar o arquivo .ods e a Sheet especificada
filename = 'military_sistem/Dados_M_OSM.ods'
df = pd.read_excel(filename, sheet_name='Unidades')

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

# Aplicar a função ao DataFrame
df["Regimento_Total_Unidades_Quinto"] = df.apply(calcular_total_nivel_quinto, axis=1)

# Exibir o DataFrame atualizado com a nova coluna
print(df[["Nome_Oitava", "Regimento_Total_Unidades_Quinto"]])

# Salvar o resultado em um novo arquivo (opcional)
df.to_excel("Unidades_Com_Totais_Quinto.xlsx", index=False)
