import pandas as pd
import numpy as np
import random


class AgePopulationProcessor:
    def __init__(self, age_population_file):
        self.age_population_file = age_population_file
        self.age_percentages = None

    def calculate_age_population_percentage(self, sheet_name="Age_Pop"):
        """Calcula a porcentagem da população por faixa etária."""
        print("\n--- Step 1: Calculando porcentagem da população por faixa etária ---")
        data = pd.read_excel(self.age_population_file, sheet_name=sheet_name, engine='odf')
        print("Colunas encontradas no arquivo:", data.columns.tolist())

        if 'Pop' not in data.columns:
            raise KeyError("A coluna 'Pop' não foi encontrada no arquivo. Verifique o nome correto da coluna.")

        total_population = data['Pop'].sum()
        data['Percentage'] = (data['Pop'] / total_population) * 100
        self.age_percentages = data[['Age', 'Pop', 'Percentage']]
        return self.age_percentages


class MunicipalityProcessor:
    def __init__(self, municipality_file):
        self.municipality_file = municipality_file
        self.municipalities = None

    def load_population_data_by_municipality(self, sheet_name="Main"):
        """Carrega dados populacionais por município."""
        print("\n--- Step 2: Carregando dados populacionais por município ---")
        data = pd.read_excel(self.municipality_file, sheet_name=sheet_name, engine='odf')
        data['Pop_div100'] = data['Pop_div100'].astype(int)
        self.municipalities = data
        return self.municipalities


class PopulationProcessor:
    def __init__(self, municipalities, age_percentages):
        self.municipalities = municipalities
        self.age_percentages = age_percentages
        self.population = None

    def calculate_population_by_age(self):
        """Calcula a população por faixa etária para cada município."""
        print("\n--- Step 4: Calculando população por faixa etária para cada município ---")
        self.age_percentages['Percentage'] /= 100  # Converte para fração

        merged_data = self.municipalities[['Nome', 'Pop_div100']].merge(self.age_percentages, how='cross')
        merged_data['Numero_Pessoas'] = (merged_data['Pop_div100'] * merged_data['Percentage']).astype(int)
        merged_data['Numero_Pessoas'] = [int(i/1000) for i in merged_data['Numero_Pessoas']] ################       REdução do volume de dados

        self.population = merged_data[['Nome', 'Age', 'Numero_Pessoas']].rename(
            columns={'Nome': 'Municipio', 'Age': 'Idade'}
        )
        print("População por faixa etária para cada município calculada com sucesso.")
        return self.population


class NameGenerator:
    def __init__(self, name_file):
        self.name_file = name_file
        self.names_df = pd.read_excel(name_file, sheet_name="Names")
        self.first_names = self.names_df['First_Name'].dropna().astype(str).tolist()
        self.surnames = self.names_df['Surname'].dropna().astype(str).tolist()

    def generate_name(self, num_names=10):
        """Gera nomes aleatórios para uma população."""
        names = []
        for _ in range(num_names):
            first_name = random.choice(self.first_names)
            num_surnames = random.randint(1, 3)
            selected_surnames = random.sample(self.surnames, num_surnames)
            full_name = f"{first_name} {' '.join(selected_surnames)}"
            names.append(full_name)
        return names

    def generate_names_for_population(self, population_data):
        """Gera nomes para a população."""
        print("\n--- Step 5: Gerando nomes para a população ---")
        population_data = population_data[population_data['Numero_Pessoas'] > 0]  # Filtra para números positivos
        expanded_population = []

        for _, row in population_data.iterrows():
            municipio = row['Municipio']
            idade = row['Idade']
            numero_pessoas = row['Numero_Pessoas']

            print(f"Processando município {municipio}, Idade {idade}")
            nomes = self.generate_name(num_names=numero_pessoas)
            expanded_population.extend(
                {'Municipio': municipio, 'Idade': idade, 'Nome': nome} for nome in nomes
            )

        print("Nomes gerados para a população com sucesso.")
        return pd.DataFrame(expanded_population)


class AttributeAssigner:
    def __init__(self, attribute_file):
        self.attribute_file = attribute_file

    def generate_attributes(self, population_data):
        """Gera e adiciona atributos para cada linha do DataFrame."""
        print("\n--- Step 8: Gerando e adicionando atributos para cada linha da população ---")
        sheet_names = ["Atributo_Int", "Atributo_Ath", "Atributo_Cha"]

        for sheet in sheet_names:
            data = pd.read_excel(self.attribute_file, sheet_name=sheet)
            data['Percentage'] = data['Percentage'].str.replace('%', '', regex=False).str.replace(',', '.').astype(float) / 100
            data['Cumulative'] = data['Percentage'].cumsum()

            population_data[sheet] = None
            for idx in population_data.index:
                rand_num = np.random.rand()
                for _, row in data.iterrows():
                    if rand_num <= row['Cumulative']:
                        random_value = random.randint(row['Start'], row['End'])
                        population_data.at[idx, sheet] = f"{random_value} ({row['Description']})"
                        break

        print("Atributos adicionados com sucesso.")
        return population_data


class IdentityGenerator:
    @staticmethod
    def generate_identity_number(row):
        """Gera um número de identidade fictício."""
        name_parts = row['Nome'].split()
        initials = ''.join(part[0].upper() for part in name_parts)
        initials_numbers = ''.join(str(ord(char) - ord('A')) for char in initials)
        state_id = str(row['ID_State'])
        random_digits = f"{random.randint(0, 9)}{random.randint(0, 9)}"
        city_id = str(row['ID_City'])
        age = row['Idade']
        return f"{initials_numbers}.{state_id}{random_digits}.{city_id}-{age}"


# --- Script Principal ---
if __name__ == "__main__":
    # Etapa 1: Processamento da população por faixa etária
    age_processor = AgePopulationProcessor('Data_Pop_Age_Name.ods')
    age_percentages = age_processor.calculate_age_population_percentage()

    # Etapa 2: Processamento de municípios
    municipality_processor = MunicipalityProcessor('Filtered_Pop_Municipio.ods')
    municipalities = municipality_processor.load_population_data_by_municipality()

    # Etapa 3: Processamento da população
    population_processor = PopulationProcessor(municipalities, age_percentages)
    population_by_age = population_processor.calculate_population_by_age()

    # Etapa 4: Geração de nomes
    name_generator = NameGenerator('Data_Pop_Age_Name.ods')
    population_with_names = name_generator.generate_names_for_population(population_by_age)

    # Etapa 5: Atribuição de atributos
    attribute_assigner = AttributeAssigner("Atributos.ods")
    population_with_attributes = attribute_assigner.generate_attributes(population_with_names)

    #population_with_attributes.to_excel('population_data.ods')

    # Etapa 6: Exibir resultado final
    print("\n--- População com nomes e atributos ---")
    print(population_with_attributes.head())
    print(len(population_with_attributes))
