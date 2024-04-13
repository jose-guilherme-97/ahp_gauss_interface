import streamlit as st
import pandas as pd

# Classe que apoia a montagem de dataframes e outras operações correlatas para compor
# os objetos necessários para execução do programa
class DealWithDf:
    def __init__(self) -> None:
        pass

    def create_decision_table(self, data_alternativas, data_criterios, flag, dict_quali = None):
        """
        Função que cria um dataframe tendo como valores a matriz de decisão fornecida pelo usuário

        Args:
            data_alternativas (dataframe pandas): df contendo as alternativas fornecidas
            data_criterios (dataframe pandas): df contendo os critérios fornecidos
            flag (bool): variável que indica se há presença de critérios qualitativos
            dict_quali (dict): dicionário que contém o de / para entre valores qualitativos e seus respectivos
            pesos calculados
        
        Returns:
            df (dataframe pandas): dataframe contendo como valor a matriz de decisão
        """
        if flag == True and dict_quali == None:
            raise ValueError("Quando flag é True (indicando que houve critérios qualitativos), dict_quali não pode ser None")
        
        index = list(data_alternativas["alternativas"])
        columns = list(data_criterios["criterios"])
        decision_matrix = pd.DataFrame(index = index, columns = columns)

        for i in range(len(index)):
            for j in range(len(columns)):
                tipo = data_criterios[data_criterios["criterios"] == columns[j]]["tipo"].values[0]
                if tipo == "quantitativo":
                    cell_value = st.number_input(f"Indique o valor quando a alternativa for {index[i]} e o critério {columns[j]}", key = f"{i}_{j}")
                if tipo == "qualitativo":
                    valores_possiveis = tuple(dict_quali[columns[j]].keys())
                    aux_value = st.selectbox(f"Indique o valor quando a alternativa for {index[i]} e o critério {columns[j]}"
                                            ,valores_possiveis
                                            , key = f"{i}_{j}")
                    cell_value = dict_quali[columns[j]][aux_value]
                decision_matrix.at[index[i], columns[j]] = cell_value
        return decision_matrix

    def color_coding(self, row, max, min):
        """
        Função que cria um mapeamento em um dataframe para definição de cores personalizadas baseando-se
        em uma coluna de resultados.

        Args:
            row (tuple): linha do dataframe percorrido
            max (float): valor máximo presente na coluna 'resultados'
            min(float): valor mínimo presente na coluna 'resultados'
        
        Returns:
            result (list): Lista contendo o mapeamento de cores a ser aplicado
        """
        if row.resultados == max:
            result = ['background-color:green'] * len(row) 
        elif row.resultados != min: 
            result = ['background-color:yellow'] * len(row) 
        else:
            result = ['background-color:red'] * len(row)
        return result