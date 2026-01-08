import streamlit as st

import pandas as pd

import plotly.express as px


# --- CONFIGURAÇÃO INICIAL ---

st.set_page_config(page_title="Dashboard Vestibular", layout="wide", page_icon="🎓")


# Cores personalizadas para consistência

COLOR_MAP = {'F': '#ff9999', 'M': '#66b3ff'}


# --- CARREGAMENTO DE DADOS ---

@st.cache_data

def load_data():

    df = pd.read_csv("dados_vestibular.csv")

    return df


df = load_data()


def processar_cotas(df):

    # 1. Identificar Baixa Renda (LB = L1/L2 usually Low Budget/Baixa Renda)

    # LI costuma ser Livre/Independente de renda

    df['Cota_Renda'] = df['Vaga'].apply(lambda x: 'Baixa Renda' if 'LB' in x else ('Independente' if 'LI' in x else 'Ampla/Outros'))

    

    # 2. Identificar Raça (PPI = Pretos, Pardos, Indígenas / Q = Quilombolas)

    def define_raca(vaga):
        vaga = str(vaga).upper() # Garante que tratamos string maiúscula
    
    # 1. Ampla Concorrência
        if 'AC' in vaga: 
            return 'Ampla Concorrência'
    
    # 2. Grupos Raciais Específicos
        if 'PPI' in vaga: 
            return 'PPI'
        if 'Q' in vaga: 
            return 'Quilombola'
    
    # 3. Tratamento explícito para PCD sem marcação racial
    # Se chegou aqui, não é PPI nem Q. Se tiver PCD, é cota de deficiência "pura"
        if 'PCD' in vaga:
            return 'PCD' 
        
    # 4. O que sobra é Cota Social/Escola Pública sem raça/deficiência definidas
        return 'Escola Pública'


    df['Cota_Raca'] = df['Vaga'].apply(define_raca)    

    # 3. Identificar PCD

    df['Cota_PCD'] = df['Vaga'].apply(lambda x: 'Sim' if 'PCD' in x else 'Não')


    return df


# Aplique logo após carregar

df = load_data()

df = processar_cotas(df)


# --- SIDEBAR (FILTROS) ---

st.sidebar.title("🔍 Filtros Avançados")

st.sidebar.markdown("Selecione as opções abaixo para filtrar os dados.")


# Função auxiliar para criar filtros com opção "Todos"

# --- FUNÇÃO AUXILIAR DE FILTRO INTELIGENTE ---
def multiselect_com_todos(label, options, key):
    """
    Cria um multiselect onde a opção 'Todos' é exclusiva.
    """
    # Garante que a opção "Todos" exista
    options_with_all = ["Todos"] + sorted([opt for opt in options if opt != "Todos"])
    
    # Inicializa o estado se não existir
    if key not in st.session_state:
        st.session_state[key] = ["Todos"]
    
    # Função de callback para gerenciar a lógica
    def on_change():
        selected = st.session_state[key]
        
        # Caso 1: Se "Todos" foi selecionado junto com outros itens
        if "Todos" in selected and len(selected) > 1:
            # Se "Todos" foi o primeiro item (já estava lá), e adicionaram outro -> Remove "Todos"
            if selected[0] == "Todos":
                st.session_state[key] = selected[1:]
            # Se "Todos" não era o primeiro (foi adicionado agora) -> Mantém só "Todos"
            else:
                st.session_state[key] = ["Todos"]
        
        # Caso 2: Se o usuário desmarcou tudo -> Volta para "Todos"
        elif not selected:
            st.session_state[key] = ["Todos"]

    # Cria o componente multiselect vinculado ao session_state e com callback
    selection = st.sidebar.multiselect(
        label,
        options=options_with_all,
        key=key,
        on_change=on_change
    )
    
    # Retorna todas as opções se "Todos" estiver selecionado, senão retorna a seleção
    return options if "Todos" in selection else selection

# --- APLICAÇÃO NOS SEUS FILTROS ---
# Substitua seu bloco de criação de filtros por este:

filtros = {}

# Note que cada chamada precisa de uma 'key' única (ex: 'filtro_curso')
filtros['Curso'] = multiselect_com_todos(
    "Selecione o(s) Curso(s):", 
    df["Curso"].dropna().unique(), 
    key="filtro_curso"
)

filtros['Turno'] = multiselect_com_todos(
    "Selecione o Turno:", 
    df["Turno"].dropna().unique(), 
    key="filtro_turno"
)

filtros['Semestre'] = multiselect_com_todos(
    "Selecione o Semestre:", 
    df["Semestre"].dropna().unique(), 
    key="filtro_semestre"
)

filtros['Grau'] = multiselect_com_todos(
    "Selecione o Grau:", 
    df["Grau"].dropna().unique(), 
    key="filtro_grau"
)

# O restante do código (df_filtered = ...) continua igual!

# Aplicação dos filtros de forma vetorizada

df_filtered = df[

    (df["Curso"].isin(filtros['Curso'])) & 

    (df["Turno"].isin(filtros['Turno'])) &

    (df["Semestre"].isin(filtros['Semestre'])) &

    (df["Grau"].isin(filtros['Grau']))

].copy() # .copy() evita warnings do pandas


# Limpeza de Gênero para gráficos

df_filtered = df_filtered.dropna(subset=['Gênero'])


# --- TÍTULO E KPIs ---

st.title("📊 Análise de Gênero - Vestibular")

st.markdown("---")


# KPIs

col1, col2, col3 = st.columns(3)

total_vagas = len(df_filtered)

pct_fem = (df_filtered[df_filtered['Gênero'] == 'F'].shape[0] / total_vagas * 100) if total_vagas > 0 else 0

pct_masc = (df_filtered[df_filtered['Gênero'] == 'M'].shape[0] / total_vagas * 100) if total_vagas > 0 else 0


col1.metric("👥 Total de Candidatos", total_vagas)

col2.metric("👩 Mulheres", f"{pct_fem:.1f}%")

col3.metric("👨 Homens", f"{pct_masc:.1f}%")

# Métrica extra: Melhor Rank encontrado


st.markdown("---")


if df_filtered.empty:

    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")

    st.stop() # Para a execução aqui se não tiver dados


# --- ORGANIZAÇÃO POR ABAS (Melhoria de UX) ---

tab1, tab2, tab3, tab4 = st.tabs(["📈 Visão Geral", "🎯 Performance & Cotas", "🌐 Socioeconômico", "💾 Base de Dados"])


# --- ABA 1: VISÃO GERAL ---

with tab1:

    col_g1, col_g2 = st.columns(2)

    

    with col_g1:

        st.subheader("Proporção Global")

        fig_pie = px.pie(df_filtered, names='Gênero', 

                         color='Gênero', color_discrete_map=COLOR_MAP,

                         hole=0.4) # Gráfico de Donut é mais moderno

        st.plotly_chart(fig_pie, use_container_width=True)


    with col_g2:

        st.subheader("Distribuição por Turno")

        df_turno = df_filtered.groupby(['Turno', 'Gênero']).size().reset_index(name='Contagem')

        fig_bar = px.bar(df_turno, x='Turno', y='Contagem', color='Gênero', barmode='group',

                         color_discrete_map=COLOR_MAP, text_auto=True)

        st.plotly_chart(fig_bar, use_container_width=True)


    st.subheader("Gênero por Tipo de Grau")

    df_grau = df_filtered.groupby(['Grau', 'Gênero']).size().reset_index(name='Contagem')

    fig_grau = px.bar(df_grau, x='Grau', y='Contagem', color='Gênero', barmode='group',

                      color_discrete_map=COLOR_MAP, text_auto=True)

    st.plotly_chart(fig_grau, use_container_width=True)


# --- ABA 2: PERFORMANCE E COTAS ---

with tab2:

    st.subheader("Análise de Classificação (Rank)")

    st.markdown("*Nota: Quanto menor o número do rank, melhor a colocação.*")

    

    col_p1, col_p2 = st.columns(2)

    

    with col_p1:

        # Boxplot

        fig_box = px.box(df_filtered, x='Gênero', y='Rank', color='Gênero',

                         color_discrete_map=COLOR_MAP,

                         points="outliers", 

                         title="Distribuição de Rank (Boxplot)")

        st.plotly_chart(fig_box, use_container_width=True)

        

    with col_p2:

        # Histograma (NOVO)

        fig_hist = px.histogram(df_filtered, x="Rank", color="Gênero", 

                                marginal="box", # Adiciona um mini boxplot em cima

                                nbins=50,

                                color_discrete_map=COLOR_MAP,

                                barmode="overlay", # Sobrepõe as cores com transparência

                                title="Histograma de Distribuição de Notas")

        fig_hist.update_traces(opacity=0.75)

        st.plotly_chart(fig_hist, use_container_width=True)


    st.markdown("---")

    st.subheader("Detalhamento por Modalidade de Vaga")

    

    # Gráfico Geral (Cota vs Ampla)

    df_tipo = df_filtered.groupby(['Tipo_Vaga', 'Gênero']).size().reset_index(name='Contagem')

    fig_tipo = px.bar(df_tipo, x='Contagem', y='Tipo_Vaga', color='Gênero', orientation='h',

                      color_discrete_map=COLOR_MAP, text_auto=False)

    st.plotly_chart(fig_tipo, use_container_width=True)

    

    # Gráfico Específico (Top 10) - CORRIGIDO

    st.subheader("Tipos Específicos de Formas de Entrada")

    # Pega apenas o Top 10 códigos mais frequentes no filtro atual

    top_vagas_codigos = df_filtered['Vaga'].value_counts().head(10).index

    df_vaga_top = df_filtered[df_filtered['Vaga'].isin(top_vagas_codigos)]

    

    df_vaga_agrupada = df_vaga_top.groupby(['Vaga', 'Gênero']).size().reset_index(name='Contagem')

    # Ordenar para ficar bonito no gráfico

    df_vaga_agrupada = df_vaga_agrupada.sort_values(by='Contagem', ascending=False)

    

    fig_cod_vaga = px.bar(df_vaga_agrupada, x='Vaga', y='Contagem', color='Gênero', 

                      barmode='group', color_discrete_map=COLOR_MAP, text_auto=True)

    st.plotly_chart(fig_cod_vaga, use_container_width=True)



# --- ABA 3: SOCIOECONÔMICO E INCLUSÃO ---
with tab3:
    st.subheader("🌐 Análise Socioeconômica e Racial")
    
    # 1. CÁLCULO DOS KPIs GERAIS
    total_filtrado = len(df_filtered)
    
    # PPI + Quilombolas (Ações Afirmativas Raciais)
    qtd_ppi = df_filtered[df_filtered['Cota_Raca'].str.contains('PPI|Quilombola', regex=True)].shape[0]
    pct_ppi = (qtd_ppi / total_filtrado * 100) if total_filtrado > 0 else 0
    
    # Baixa Renda
    qtd_baixa_renda = df_filtered[df_filtered['Cota_Renda'] == 'Baixa Renda'].shape[0]
    pct_baixa_renda = (qtd_baixa_renda / total_filtrado * 100) if total_filtrado > 0 else 0

    #PCD

    qtd_pcd = df_filtered[df_filtered['Cota_PCD'] == 'Sim'].shape[0]
    pct_pcd = (qtd_pcd / total_filtrado * 100) if total_filtrado > 0 else 0

    # Escola Pública (Total de Cotistas)
    qtd_ep = df_filtered[df_filtered['Tipo_Vaga'] == 'Cota'].shape[0]
    pct_ep = (qtd_ep / total_filtrado * 100) if total_filtrado > 0 else 0

    # 2. EXIBIÇÃO DOS KPIs (Layout Limpo sem Setas)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        label="Escola Pública (Total Cotas)", 
        value=f"{qtd_ep} ({pct_ep:.1f}%)"
    )
    
    kpi2.metric(
        label="PPI e Quilombolas", 
        value=f"{qtd_ppi} ({pct_ppi:.1f}%)"
    )
    
    kpi3.metric(
        label="Baixa Renda", 
        value=f"{qtd_baixa_renda} ({pct_baixa_renda:.1f}%)"
    )
    
    kpi4.metric(
        label="PCD", 
        value=f"{qtd_pcd} ({pct_pcd:.1f}%)"
    )

    st.markdown("---")

    # 3. GRÁFICOS DE RAÇA E RENDA
    df_cotistas = df_filtered[df_filtered['Tipo_Vaga'] == 'Cota'].copy()

    if not df_cotistas.empty:
        col_socio1, col_socio2 = st.columns(2)
        
        with col_socio1:
            # Gráfico de Renda
            fig_renda = px.histogram(
                df_cotistas, x="Cota_Renda", color="Gênero", 
                barmode="group", 
                title="Distribuição por Renda (Apenas Cotistas)",
                color_discrete_map=COLOR_MAP, text_auto=True
            )
            fig_renda.update_layout(xaxis_title=None)
            st.plotly_chart(fig_renda, use_container_width=True)

        with col_socio2:
            # Gráfico de Raça (com rótulo simplificado para visualização)
            df_cotistas['Cota_Raca_Simples'] = df_cotistas['Cota_Raca'].replace(
                'Escola Pública (Sem Raça/PCD declarados)', 'Não PPI (Apenas EP)'
            )
            
            fig_raca = px.histogram(
                df_cotistas, x="Cota_Raca_Simples", color="Gênero", 
                barmode="group", 
                title="Distribuição Racial (Apenas Cotistas)",
                color_discrete_map=COLOR_MAP, text_auto=True
            )
            fig_raca.update_layout(xaxis_title=None)
            st.plotly_chart(fig_raca, use_container_width=True)
    else:
        st.info("ℹ️ Nenhum aluno cotista encontrado com os filtros selecionados.")

    # 4. SEÇÃO DE ACESSIBILIDADE (PCD) - Integrada ao final
    st.markdown("---")
    st.subheader("♿ Acessibilidade e Inclusão (PCD)")

    # Filtra apenas candidatos PCD
    df_pcd = df_filtered[df_filtered['Vaga'].str.contains('PCD', na=False)].copy()

    if not df_pcd.empty:
        col_pcd1, col_pcd2 = st.columns(2)
        
        with col_pcd1:
            # Gráfico 1: Rosca de Gênero
            fig_pcd_pizza = px.pie(
                df_pcd, 
                names='Gênero', 
                title='Gênero entre Pessoas com Deficiência',
                color='Gênero', 
                color_discrete_map=COLOR_MAP,
                hole=0.4
            )
            st.plotly_chart(fig_pcd_pizza, use_container_width=True)

        with col_pcd2:
            # Gráfico 2: Modalidade (Renda vs Independente)
            df_pcd['Tipo_PCD'] = df_pcd['Vaga'].replace({
                'LI_PCD': 'PCD (Independente de Renda)', 
                'LB_PCD': 'PCD (Baixa Renda)'
            })
            
            fig_pcd_bar = px.histogram(
                df_pcd, 
                x="Tipo_PCD", 
                color="Gênero", 
                barmode="group",
                title="Modalidade de Cota PCD",
                color_discrete_map=COLOR_MAP, 
                text_auto=True
            )
            fig_pcd_bar.update_layout(xaxis_title=None)
            st.plotly_chart(fig_pcd_bar, use_container_width=True)
            
    else:
        st.write("Nenhum candidato PCD identificado neste recorte de dados.")
# --- ABA 4: DADOS BRUTOS---


with tab4:

    st.subheader("Dados Detalhados")

    st.dataframe(df_filtered, use_container_width=True)    

    # Botão de Download (NOVO)

    csv = df_filtered.to_csv(index=False).encode('utf-8')

    st.download_button(

        label="📥 Baixar Dados Filtrados (CSV)",

        data=csv,

        file_name='vestibular_filtrado.csv',

        mime='text/csv',

    )