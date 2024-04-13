import streamlit as st
import pandas as pd
import uuid
import ahp_gauss
from functions_app import DealWithDf

# Inicializando algumas listas para coletar alternativas e critérios
rows_collection_alt = []
rows_collection_cri = []

# Inicializando alguns estatos utilizados no processo de 
if "alternativas" not in st.session_state:
    st.session_state["alternativas"] = []

if "criterios" not in st.session_state:
    st.session_state["criterios"] = []

if 'alternativas_concluidas' not in st.session_state:
    st.session_state.alternativas_concluidas = False

if 'criterios_concluidos' not in st.session_state:
    st.session_state.criterios_concluidos = False

if f"matriz_decisao" not in st.session_state:
    st.session_state["matriz_decisao"] = False

# Concentrando a classe que coordena o acionamento de botões
class Button:
    def __init__(self) -> None:
        pass

    def click_button_alternativas_concluidas(self):
        st.session_state.alternativas_concluidas = True

    def click_button_criterios_concluidos(self):
        st.session_state.criterios_concluidos = True

    def click_button_matriz_decisao(self):
        st.session_state["matriz_decisao"] = True

# Classe que coordena o processo de inserção de dados pelo tomador de decisão
class CollectInfos:
    def __init__(self) -> None:
        pass

    def add_row(self, type):
        """
        Função que adiciona uma linha para que o usuário possa informar mais um valor

        Args:
            type (str): indica a etapa ao qual deseja-se inserir linhas (alternativas, critérios, etc.)
        
        Return:
            None
        """
        element_id = uuid.uuid4()
        st.session_state[type].append(str(element_id))

    def remove_row(self, row_id, type):
        """
        Função que remove uma linha

        Args:
            row_id (str, int): indica o id utilizado para a linha que deseja-se excluir
            type (str): indica a etapa ao qual deseja-se inserir linhas (alternativas, critérios, etc.)
        
        Return:
            None
        """
        st.session_state[type].remove(str(row_id))

    def generate_row(self, row_id, type):
        """
        Função que coordena a aparição/exclusão de uma linha e capta a informação fornecida pelo usuário

        Args:
            row_id (str, int): indica o id utilizado para a linha trabalhada
            type (str): indica a etapa ao qual deseja-se inserir linhas (alternativas, critérios, etc.)
        
        Return:
            (dict): dicionário contendo as informações coletadas
        """
        if type == "alternativas":
            row_container = st.empty()
            row_columns = row_container.columns((3,1))
            row_name = row_columns[0].text_input("Alternativa", key=f"txt_{row_id}")
            row_columns[1].button("🗑️", key=f"del_{row_id}", on_click=self.remove_row, args=[row_id, type])
            return {"name": row_name}
        
        if type == "criterios":
            row_container = st.empty()
            row_columns = row_container.columns((3, 3, 1))
            row_name = row_columns[0].text_input("Criterios", key=f"txt_{row_id}")
            row_charac = row_columns[1].selectbox("Característica", ("Quanto maior, melhor", "Quanto maior, pior", "Não Aplicável"), key=f"carac_{row_id}")
            row_columns[2].button("🗑️", key=f"del_{row_id}", on_click=self.remove_row, args=[row_id, type])
            return {"name": row_name, "caracteristica": row_charac}

# Inicialização das classes importantes a serem utilizadas
botoes = Button()
coordena_coleta = CollectInfos()
df_opps = DealWithDf()

# Construção da visualização inicial do usuário. Uma tela informando o propósito, modelo, origem, criador e
# qual a lógica de construção e limitações do algoritmo
with st.container():
    st.title("Modelo de apoio à tomada de decisão multicritérios")
    st.subheader("O método AHP - Gaussiano")
    menu = st.columns([3,1])
    with menu[0]:
        texto1 = """    Com artigo seminal publicado em 2021 pelo professor [Marcos dos Santos](https://www.linkedin.com/in/profmarcosdossantos/) e
            seu grupo de pesquisa, o modelo busca ser uma alternativa frente a algumas limitações do método clássico AHP do professor
            [Thomas Saaty](https://pt.wikipedia.org/wiki/Thomas_Saaty). Com este método, o tomador de decisão não possui o desgaste cognitivo
            presente no método AHP, em que há a necessidade de ponderar as relações de paridade dos critérios envolvidos. Com isso,
            o vetor prioridade dos critérios é obtido a partir da própria matriz de decisão, pois torna-se o resultado do
            vetor de coeficientes de variação normalizados, obtido a partir da matriz transposta da matriz de decisão normalizada. Tal método implica
            em número ilimitado de critérios, mas resume-se a critérios cardinais (quantitativos). Outra característica é que a avaliação do grau de relevância
            dos critérios baseia-se em conceitos estatísticos, tornando a opinião do decisor menos impactante no processo.
            """
        st.write(f'{texto1}')
    with menu[1]:
        st.image("marcos_dos_santos.jpg",
                  use_column_width=True)
    
    st.subheader("Abordagem do produto")
    texto2 = """    Este produto busca trazer de maneira simples e prática a possibilidade de aplicação do
             método AHP - Gaussiano. Para tal, precisamos conhecer os passos a serem seguidos e as características
             do modelo."""
    st.write(f'<div style="text-align: justify">{texto2}</div>', unsafe_allow_html=True)
    st.image("fluxo.jpg")
    
    texto3 = """Com isso, após definirmos quais as alternativas temos, precisamos pontuar quais os critérios
             adotados na tomada de decisão e sua característica
             em relação ao negócio (a variação deste critério para mais ou para menos é prejudicial ou benéfica para
             sua tomada de decisão?). Em seguida, há a definição da matriz de decisão, no qual são estabelecidos quais
             os valores em relação a cada alternativa. Com isso, o método é capaz de retornar o que é estatisticamente
             melhor para o tomador de decisão."""
    st.write(f'<div style="text-align: justify">{texto3}</div>', unsafe_allow_html=True)
   
# Estrutura dedicada a receber as alternativas de solução do modelo
with st.container():
    st.title("Adição de alternativas")
    for row in st.session_state["alternativas"]:
        row_data = coordena_coleta.generate_row(row, "alternativas")
        rows_collection_alt.append(row_data)

    menu = st.columns(2)

    with menu[0]:
        # Botão que adiciona uma linha para receber mais uma alternativa
        st.button("Add Alternativa", on_click=coordena_coleta.add_row,  args=["alternativas"])
    with menu[1]:
        # Botão que indica que o processo foi finalizado
        st.button("Alternativas - Concluído", on_click=botoes.click_button_alternativas_concluidas)
    # Apresentação das alternativas coletadas
    if len(rows_collection_alt) > 0:
        st.subheader("Dados coletados - Alternativas")
        display = st.columns(1)
        data_alternativas = pd.DataFrame(rows_collection_alt)
        data_alternativas.rename(columns={"name": "alternativas"}, inplace=True)
        display[0].dataframe(data=data_alternativas, use_container_width=True)

# Estrutura dedicada ao recebimento dos critérios
with st.container():
    if st.session_state.alternativas_concluidas:
        st.title("Adição de critérios")

        for row in st.session_state["criterios"]:
            row_data = coordena_coleta.generate_row(row, "criterios")
            rows_collection_cri.append(row_data)

        menu = st.columns(2)

        with menu[0]:
            # Botão que indica que queremos adicionar mais um critério para escolha
            st.button("Add Critério", on_click=coordena_coleta.add_row,  args=["criterios"])
        with menu[1]:
            # Botão que indica que o processo de inserção de critérios foi finalizado
            st.button("Critério - Concluído", on_click=botoes.click_button_criterios_concluidos)
        # Apresentação dos dados coletados
        if len(rows_collection_cri) > 0:
            st.subheader("Dados coletados - Critérios")
            display = st.columns(1)
            data_criterios = pd.DataFrame(rows_collection_cri)
            data_criterios.rename(columns={"name": "criterios"}, inplace=True)
            data_criterios["caracteristica"] = data_criterios["caracteristica"].apply(lambda x: -1 if x == "Quanto maior, pior" else 1)
            display[0].dataframe(data=data_criterios, use_container_width=True)

# Estrutura dedicada a construir a matriz de decisão
with st.container():
    if st.session_state["criterios_concluidos"]:
        data_criterios["tipo"] = "quantitativo"
        df_decisao = df_opps.create_decision_table(data_alternativas, data_criterios, False)

        st.subheader("Dados coletados - Matriz de Decisão")
        display = st.columns(1)
        display[0].dataframe(data=df_decisao, use_container_width=True)
        matriz_decisao = df_decisao.values
        menu_final = st.columns(1)
        with menu_final[0]:
            # Botão que indica a finalização da matriz de decisão
            st.button("Matriz de Decisão Finalizada", on_click=botoes.click_button_matriz_decisao, key=uuid.uuid4())

# Estrutura dedicada a execução do algoritmo e apresentação de resultados
with st.container():
    if st.session_state["matriz_decisao"]:
        lista_referencia = list(data_criterios["caracteristica"])
        process = ahp_gauss.AHP_GAUSS(decision_matrix = matriz_decisao, monotomic_reference_list = lista_referencia)
        result = process.run_process()
        df_results = data_alternativas.copy()
        df_results["resultados"] = result.flatten()
        max_results = df_results["resultados"].max()
        min_results = df_results["resultados"].min()
        st.subheader("Resultados - Verde (melhor escolha), Amarelo (valores intermediários), Vermelho (pior escolha)")
        display = st.columns(1)
        display[0].dataframe(df_results.style.apply(lambda x: df_opps.color_coding(row = x, max = max_results, min = min_results), axis=1))
