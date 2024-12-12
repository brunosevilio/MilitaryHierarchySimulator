import random
from simplekml import Kml
import pandas as pd
import ast
import math


class Unidade:
    """Classe base para representar uma unidade hierárquica."""
    def __init__(self, nome, nivel, id_unico, lat=None, lon=None, imagem=None):
        self.nome = nome
        self.nivel = nivel
        self.id_unico = id_unico
        self.lat = lat
        self.lon = lon
        self.imagem = imagem  # Link para imagem
        self.subordinados = []

    def adicionar_subordinado(self, unidade):
        """Adiciona uma unidade subordinada."""
        self.subordinados.append(unidade)

    def gerar_coordenadas(self, lat_base, lon_base, total_subordinados, raio):
        """Gera coordenadas para subordinados dispostos em círculo."""
        if total_subordinados > 0:
            coordenadas = gerar_coordenadas_circulo((lat_base, lon_base), total_subordinados, raio)
            for i, unidade in enumerate(self.subordinados):
                unidade.lat, unidade.lon = coordenadas[i]


class Forca(Unidade):
    """Representa uma força (nível superior)."""
    def __init__(self, nome, id_unico):
        super().__init__(nome, "Força", id_unico)


class Exercito(Unidade):
    """Representa um exército."""
    def __init__(self, nome, id_unico, coord=None, imagem=None):
        super().__init__(nome, "Exército", id_unico, imagem=imagem)
        if coord:
            self.lat = coord.get('lat')
            self.lon = coord.get('lon')


class Divisao(Unidade):
    """Representa uma divisão."""
    def __init__(self, nome, id_unico, imagem=None):
        super().__init__(nome, "Divisão", id_unico, imagem=imagem)


class Brigada(Unidade):
    """Representa uma brigada."""
    def __init__(self, nome, id_unico, imagem=None):
        super().__init__(nome, "Brigada", id_unico, imagem=imagem)


class Regimento(Unidade):
    """Representa um regimento."""
    def __init__(self, nome, id_unico, imagem=None):
        super().__init__(nome, "Regimento", id_unico, imagem=imagem)


def gerar_coordenadas_circulo(base_coord, total, raio):
    """
    Gera coordenadas para posicionar os subordinados em círculo ao redor de uma coordenada base.
    """
    lat_base, lon_base = base_coord
    angulo_incremento = 360 / total  # Divide o círculo em partes iguais

    coordenadas = []
    for i in range(total):
        angulo = math.radians(i * angulo_incremento)  # Converte o ângulo para radianos
        lat = lat_base + raio * math.sin(angulo)
        lon = lon_base + raio * math.cos(angulo)
        coordenadas.append((lat, lon))

    return coordenadas


def processar_hierarquia(df_ativas, cidades_df):
    """
    Processa os DataFrames para construir a hierarquia usando classes.
    
    Parâmetros:
        df_ativas (pd.DataFrame): DataFrame contendo as unidades hierárquicas.
        cidades_df (pd.DataFrame): DataFrame contendo as cidades e suas coordenadas.
        
    Retorna:
        dict: Dicionário de forças processadas.
    """
    forcas = {}

    # Função para buscar coordenadas de uma cidade
    def buscar_coordenadas(cidade_nome):
        if pd.notna(cidade_nome):
            cidade_row = cidades_df[cidades_df['Nome'] == cidade_nome]
            if not cidade_row.empty:
                return {
                    'lat': cidade_row.iloc[0]['Latitude'],
                    'lon': cidade_row.iloc[0]['Longitude']
                }
        return None

    for _, row in df_ativas.iterrows():
        forca_nome = row['Force']
        exercito_nome = row['Exercito']
        divisao_nome = row['Divizao']
        brigada_nome = row['Brigada']

        # Busca coordenadas de cada nível
        coords_ex = buscar_coordenadas(row.get('Cidade'))  # Cidade do Exército
        coords_div = buscar_coordenadas(row.get('Cidade_Div'))  # Cidade da Divisão
        coords_brig = buscar_coordenadas(row.get('Cidade_Brig'))  # Cidade da Brigada

        print(f"[DEBUGC] Exército '{exercito_nome}' - Cidade: {row.get('Cidade')}, Coordenadas: {coords_ex}")
        print(f"[DEBUGC] Divisão '{divisao_nome}' - Cidade: {row.get('Cidade_Div')}, Coordenadas: {coords_div}")
        print(f"[DEBUGC] Brigada '{brigada_nome}' - Cidade: {row.get('Cidade_Brig')}, Coordenadas: {coords_brig}")

        ex_imagem = row.get('Exe_PNG')
        div_imagem = row.get('Div_PNG')
        bri_imagem = row.get('Bri_PNG')
        reg_imagem = row.get('Reg_PNG')

        regimentos = [row[col] for col in df_ativas.columns if col.startswith('Regimento_') and pd.notna(row[col])]

        # Adiciona a força se não existir
        if forca_nome not in forcas:
            forcas[forca_nome] = Forca(forca_nome, id_unico=len(forcas) + 1)

        # Adiciona o exército
        exercito = next((e for e in forcas[forca_nome].subordinados if e.nome == exercito_nome), None)
        if not exercito:
            exercito = Exercito(exercito_nome, id_unico=len(forcas[forca_nome].subordinados) + 1, coord=coords_ex, imagem=ex_imagem)
            forcas[forca_nome].adicionar_subordinado(exercito)

        # Adiciona a divisão
        # Adiciona a divisão
        divisao = next((d for d in exercito.subordinados if d.nome == divisao_nome), None)
        if not divisao:
            divisao = Divisao(divisao_nome, id_unico=len(exercito.subordinados) + 1, imagem=div_imagem)
            
            # Priorize as coordenadas da cidade da divisão, se disponíveis
            if coords_div:
                divisao.lat, divisao.lon = coords_div['lat'], coords_div['lon']
            else:
                divisao.lat, divisao.lon = exercito.lat, exercito.lon  # Caso contrário, herda do exército
            
            exercito.adicionar_subordinado(divisao)
            print(f"[DEBUGB] Divisão '{divisao.nome}' - Coordenadas finais atribuídas: ({divisao.lat}, {divisao.lon})")

        # Adiciona a brigada
        brigada = next((b for b in divisao.subordinados if b.nome == brigada_nome), None)
        if not brigada:
            brigada = Brigada(brigada_nome, id_unico=len(divisao.subordinados) + 1, imagem=bri_imagem)
            
            # Priorize as coordenadas da cidade da brigada, se disponíveis
            if coords_brig:
                brigada.lat, brigada.lon = coords_brig['lat'], coords_brig['lon']
            else:
                brigada.lat, brigada.lon = divisao.lat, divisao.lon  # Caso contrário, herda da divisão
            
            divisao.adicionar_subordinado(brigada)
            print(f"[DEBUGB] Brigada '{brigada.nome}' - Coordenadas finais atribuídas: ({brigada.lat}, {brigada.lon})")



        # Adiciona os regimentos
        for regimento_nome in regimentos:
            regimento = Regimento(regimento_nome, id_unico=len(brigada.subordinados) + 1, imagem=reg_imagem)
            regimento.lat, regimento.lon = brigada.lat, brigada.lon  # Regimentos herdam da brigada
            brigada.adicionar_subordinado(regimento)

    return forcas






def gerar_kml_com_camadas(forcas, niveis, output_file):
    """
    Gera um único KML contendo camadas (folders) para cada nível especificado.

    Parâmetros:
        forcas (dict): Dicionário de forças processadas.
        niveis (list): Lista de níveis para os quais gerar camadas.
        output_file (str): Nome do arquivo KML de saída.
    """
    kml = Kml()

    def adicionar_unidades_por_nivel(unidade, nivel, folder, hierarquia_superior=None):
        """
        Adiciona as unidades de um determinado nível ao KML, incluindo informações de unidades superiores e subordinadas.
        
        Parâmetros:
            unidade (Unidade): Unidade atual sendo processada.
            nivel (str): Nível atual sendo processado.
            folder (Folder): Pasta do KML onde as unidades serão adicionadas.
            hierarquia_superior (list): Lista de nomes das unidades superiores.
        """
        # Inicializa a hierarquia superior se ainda não existir
        if hierarquia_superior is None:
            hierarquia_superior = []

        if unidade.nivel == nivel and unidade.lat is not None and unidade.lon is not None:
            # Constrói a hierarquia de unidades superiores
            unidade_superior = " > ".join(hierarquia_superior) if hierarquia_superior else "Nenhuma"
            subordinados = [sub.nome for sub in unidade.subordinados]

            # Cria o ponto KML para a unidade
            print(f"[DEBUGA] Plotando unidade {unidade.nome} - Coordenadas: ({unidade.lat}, {unidade.lon})")

            ponto = folder.newpoint(
                name=f"{unidade.nome} (ID: {unidade.id_unico})",
                coords=[(unidade.lon, unidade.lat)]
            )

            # Cria a descrição
            description = (
                f"Unidade: {unidade.nome}\n"
                f"Nível: {unidade.nivel}\n"
                f"ID: {unidade.id_unico}\n"
                f"Latitude: {unidade.lat}\n"
                f"Longitude: {unidade.lon}\n"
                f"Unidades Superiores: {unidade_superior}\n"
            )

            if subordinados:
                description += "Unidades Subordinadas:\n" + "\n".join(subordinados) + "\n"

            if unidade.imagem:
                description += f"<br><img src='{unidade.imagem}' alt='{unidade.nome}' width='200'/>"
                ponto.style.iconstyle.icon.href = unidade.imagem
                ponto.style.iconstyle.scale = 1.0

            ponto.description = description

        # Adiciona unidades subordinadas recursivamente, passando a hierarquia superior atualizada
        for subordinado in unidade.subordinados:
            adicionar_unidades_por_nivel(subordinado, nivel, folder, hierarquia_superior + [unidade.nome])

    # Cria uma camada (folder) para cada nível
    for nivel in niveis:
        folder = kml.newfolder(name=f"Nível: {nivel}")
        for forca in forcas.values():
            adicionar_unidades_por_nivel(forca, nivel, folder)

    # Salva o arquivo KML
    kml.save(output_file)
    print(f"KML '{output_file}' gerado com camadas para os níveis especificados.")






def gerar_coordenadas_todos_niveis(forcas, raio_inicial=0.01):
    """
    Gera as coordenadas para todas as unidades em todos os níveis hierárquicos.

    Parâmetros:
        forcas (dict): Dicionário de forças processadas.
        raio_inicial (float): Raio inicial para as unidades superiores.
    """
    for forca in forcas.values():
        # Garante coordenadas padrão para a força
        if forca.lat is None or forca.lon is None:
            forca.lat, forca.lon = 0.0, 0.0

        # Processa os exércitos
        for exercito in forca.subordinados:
            if exercito.lat is None or exercito.lon is None:
                exercito.lat, exercito.lon = forca.lat, forca.lon  # Herda da força
            exercito.gerar_coordenadas(exercito.lat, exercito.lon, len(exercito.subordinados), raio_inicial)

            # Processa as divisões
            for divisao in exercito.subordinados:
                if divisao.lat is None or divisao.lon is None:
                    divisao.lat, divisao.lon = exercito.lat, exercito.lon  # Herda do exército
                divisao.gerar_coordenadas(divisao.lat, divisao.lon, len(divisao.subordinados), raio_inicial / 2)

                # Processa as brigadas
                for brigada in divisao.subordinados:
                    if brigada.lat is None or brigada.lon is None:
                        brigada.lat, brigada.lon = divisao.lat, divisao.lon  # Herda da divisão
                    brigada.gerar_coordenadas(brigada.lat, brigada.lon, len(brigada.subordinados), raio_inicial / 3)

                    # Processa os regimentos
                    for regimento in brigada.subordinados:
                        if regimento.lat is None or regimento.lon is None:
                            regimento.lat, regimento.lon = brigada.lat, brigada.lon  # Herda da brigada
                        regimento.gerar_coordenadas(regimento.lat, regimento.lon, len(regimento.subordinados), raio_inicial / 4)




# Carregar os DataFrames
df_ativas = pd.read_excel('military_sistem/Data_Military_Units.ods', sheet_name='Ativas')
cidades_df = pd.read_excel('citizen_generator/Filtered_Pop_Municipio.ods', sheet_name='Main')

# Corrigir o formato das coordenadas no DataFrame de cidades
cidades_df['Latitude'] = cidades_df['Latitude'].apply(lambda x: float(str(x).replace(',', '.')))
cidades_df['Longitude'] = cidades_df['Longitude'].apply(lambda x: float(str(x).replace(',', '.')))

# Processar a hierarquia com a nova coluna 'Cidade'
forcas = processar_hierarquia(df_ativas, cidades_df)

# Gerar as coordenadas para todos os níveis hierárquicos
gerar_coordenadas_todos_niveis(forcas)

# Níveis para o KML
niveis = ["Exército", "Divisão", "Brigada", "Regimento"]

# Gerar um único KML com camadas separadas por nível
gerar_kml_com_camadas(forcas, niveis, output_file="unidades.kml")

# Verificar as primeiras linhas de ambos os DataFrames
print("[DEBUG] Primeiras linhas do DataFrame df_ativas:")
print(df_ativas.head())

print("[DEBUG] Primeiras linhas do DataFrame cidades_df:")
print(cidades_df.head())
# Teste direto da função buscar_coordenadas
