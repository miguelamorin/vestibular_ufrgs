import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(page_title="Dashboard Vestibular", layout="wide", page_icon="🎓")

# Cores personalizadas para consistência nos gráficos
COLOR_MAP = {'F': '#ff9999', 'M': '#66b3ff'}

# --- DICIONÁRIO DE ÁREAS DE CONHECIMENTO ---
dicionario_curso_area = {
    'Administração - Bacharelado - Noturno': 'Economia, Gestão e Negócios',
    'Odontologia - Bacharelado - Diurno': 'Saúde',
    'Geologia - Bacharelado': 'Biológicas, Naturais e Agrárias',
    'Relações Públicas - Bacharelado': 'Comunicação e Informação',
    'Estatística - Bacharelado': 'Exatas e Tecnologia',
    'Letras - Licenciatura': 'Humanas e Sociais',
    'Medicina Veterinária - Bacharelado': 'Saúde',
    'Engenharia Física - Bacharelado': 'Engenharias e Arquitetura',
    'Ciência da Computação - Bacharelado': 'Exatas e Tecnologia',
    'Pedagogia - Licenciatura - Matutino': 'Humanas e Sociais',
    'Farmácia - Bacharelado': 'Saúde',
    'História da Arte - Bacharelado - Noturno': 'Artes',
    'Música': 'Artes',
    'Pedagogia - Licenciatura - Noturno - Campus Litoral Norte': 'Humanas e Sociais',
    'Administração Pública e Social - Bacharelado - Noturno': 'Economia, Gestão e Negócios',
    'Ciências Jurídicas e Sociais - Direito - Bacharelado - Diurno': 'Humanas e Sociais',
    'Engenharia Cartográfica e de Agrimensura - Bacharelado - Noturno': 'Engenharias e Arquitetura',
    'Filosofia - Licenciatura - Noturno': 'Humanas e Sociais',
    'Ciências Sociais - Noturno': 'Humanas e Sociais',
    'História - Diurno': 'Humanas e Sociais',
    'Engenharia Civil - Bacharelado': 'Engenharias e Arquitetura',
    'Saúde Coletiva - Bacharelado - Noturno': 'Saúde',
    'Educação Física': 'Saúde',
    'Letras - Bacharelado': 'Humanas e Sociais',
    'Ciências Biológicas - Biologia Marinha - Bacharelado - Campus Litoral Norte': 'Biológicas, Naturais e Agrárias',
    'Física - Bacharelado': 'Exatas e Tecnologia',
    'Artes Visuais - Bacharelado': 'Artes',
    'Fonoaudiologia - Bacharelado': 'Saúde',
    'Relações Internacionais - Bacharelado': 'Humanas e Sociais',
    'Jornalismo - Bacharelado': 'Comunicação e Informação',
    'Ciências Jurídicas e Sociais - Direito - Bacharelado - Noturno': 'Humanas e Sociais',
    'Engenharia de Minas - Bacharelado': 'Engenharias e Arquitetura',
    'Engenharia Química - Bacharelado': 'Engenharias e Arquitetura',
    'Arquitetura e Urbanismo - Bacharelado': 'Engenharias e Arquitetura',
    'Ciências Econômicas - Bacharelado - Diurno': 'Economia, Gestão e Negócios',
    'Engenharia de Alimentos - Bacharelado': 'Engenharias e Arquitetura',
    'Ciências Biológicas - Bacharelado': 'Biológicas, Naturais e Agrárias',
    'Biblioteconomia - Bacharelado': 'Comunicação e Informação',
    'Letras - Bacharelado: Formação Tradutor e Intérprete de Libras': 'Humanas e Sociais',
    'Engenharia de Produção - Bacharelado': 'Engenharias e Arquitetura',
    'Dança - Licenciatura': 'Artes',
    'Artes Visuais - Licenciatura': 'Artes',
    'Ciências Sociais - Diurno': 'Humanas e Sociais',
    'Engenharia Elétrica - Bacharelado': 'Engenharias e Arquitetura',
    'Engenharia de Materiais - Bacharelado': 'Engenharias e Arquitetura',
    'Nutrição - Bacharelado': 'Saúde',
    'Ciências Biológicas - Licenciatura': 'Biológicas, Naturais e Agrárias',
    'Fisioterapia - Bacharelado': 'Saúde',
    'Matemática - Licenciatura - Diurno': 'Exatas e Tecnologia',
    'Teatro - Bacharelado': 'Artes',
    'Ciências Contábeis - Bacharelado - Noturno': 'Economia, Gestão e Negócios',
    'Zootecnia - Bacharelado': 'Biológicas, Naturais e Agrárias',
    'Engenharia Mecânica - Bacharelado': 'Engenharias e Arquitetura',
    'Medicina - Bacharelado': 'Saúde',
    'Serviço Social - Bacharelado - Noturno': 'Humanas e Sociais',
    'Arquivologia - Bacharelado - Noturno': 'Comunicação e Informação',
    'Ciências Econômicas - Bacharelado - Noturno': 'Economia, Gestão e Negócios',
    'Design de Produto - Bacharelado': 'Artes',
    'Psicologia - Bacharelado - Noturno': 'Saúde',
    'Ciências Atuariais - Bacharelado - Noturno': 'Economia, Gestão e Negócios',
    'Design Visual - Bacharelado': 'Artes',
    'Odontologia - Bacharelado - Noturno': 'Saúde',
    'Agronomia - Bacharelado': 'Biológicas, Naturais e Agrárias',
    'Biomedicina - Bacharelado': 'Saúde',
    'Engenharia Ambiental - Bacharelado': 'Engenharias e Arquitetura',
    'Teatro - Licenciatura': 'Artes',
    'Pedagogia - Licenciatura - Noturno': 'Humanas e Sociais',
    'Química Industrial - Bacharelado - Noturno': 'Biológicas, Naturais e Agrárias',
    'Administração - Bacharelado - Diurno': 'Economia, Gestão e Negócios',
    'Enfermagem - Bacharelado': 'Saúde',
    'Biotecnologia - Bacharelado': 'Biológicas, Naturais e Agrárias',
    'Geografia - Noturno': 'Humanas e Sociais',
    'Física - Bacharelado: Astrofísica': 'Exatas e Tecnologia',
    'Psicologia - Bacharelado - Diurno': 'Saúde',
    'Matemática - Bacharelado': 'Exatas e Tecnologia',
    'Química Industrial - Bacharelado - Integral': 'Biológicas, Naturais e Agrárias',
    'Geografia - Diurno': 'Humanas e Sociais',
    'História - Noturno': 'Humanas e Sociais',
    'Publicidade e Propaganda - Bacharelado': 'Comunicação e Informação',
    'Filosofia - Bacharelado - Diurno': 'Humanas e Sociais',
    'Matemática - Licenciatura - Noturno': 'Exatas e Tecnologia',
    'Engenharia de Computação - Bacharelado': 'Engenharias e Arquitetura',
    'Engenharia de Gestão de Energia - Bacharelado - Campus Litoral Norte': 'Engenharias e Arquitetura',
    'Engenharia Hídrica - Bacharelado': 'Engenharias e Arquitetura',
    'Políticas Públicas - Bacharelado - Noturno': 'Humanas e Sociais',
    'Museologia - Bacharelado': 'Comunicação e Informação',
    'Engenharia de Energia - Bacharelado': 'Engenharias e Arquitetura',
    'Engenharia de Controle e Automação - Bacharelado': 'Engenharias e Arquitetura',
    'Engenharia Metalúrgica - Bacharelado': 'Engenharias e Arquitetura',
    'Física - Licenciatura - Noturno': 'Exatas e Tecnologia',
    'Química - Licenciatura - Noturno': 'Biológicas, Naturais e Agrárias',
    'Geografia - Licenciatura - Noturno - Campus Litoral Norte': 'Humanas e Sociais',
    'Química - Bacharelado': 'Biológicas, Naturais e Agrárias',
    'Física - Licenciatura - Diurno': 'Exatas e Tecnologia',
    'Gestão Pública e Desenvolvimento Regional - Bacharelado - Noturno - Campus Litoral Norte': 'Economia, Gestão e Negócios',
    'Engenharia de Serviços - Bacharelado - Campus Litoral Norte': 'Economia, Gestão e Negócios',
    'Educação do Campo - Ciências da Natureza - Licenciatura - Campus Litoral Norte': 'Biológicas, Naturais e Agrárias',
    'Interdisciplinar em Ciência e Tecnologia - Bacharelado - Campus Litoral Norte': 'Exatas e Tecnologia'
}

# --- CARREGAMENTO E PROCESSAMENTO OTIMIZADO DE DADOS ---
@st.cache_data
def load_data():
    # 1. Carregar CSV
    df = pd.read_csv("dados_vestibular.csv")
    
    # 2. Limpeza: Remover duplicatas baseadas no número de Inscrição
    df = df.drop_duplicates(subset=['Inscrição'], keep='first')
    
    # 3. Mapeamento de Área (Processamento Pesado 1)
    df['Area'] = df['Curso'].map(dicionario_curso_area).fillna('Outra / Não Classificado')
    
    # 4. Processamento de Cotas (Processamento Pesado 2)
    # Convertemos para string e maiúsculo uma vez só para otimizar
    vaga_series = df['Vaga'].astype(str).str.upper()
    
    # Lógica de Renda
    df['Cota_Renda'] = vaga_series.apply(
        lambda x: 'Baixa Renda' if 'LB' in x else ('Independente' if 'LI' in x else 'Ampla/Outros')
    )
    
    # Lógica de Raça e Grupo
    def define_raca_row(val):
        if 'AC' in val: return 'Ampla Concorrência'
        if 'PPI' in val: return 'PPI (Preto/Pardo/Indígena)'
        if 'Q' in val: return 'Quilombola'
        if 'PCD' in val: return 'PCD (Não PPI)' 
        return 'Escola Pública (Sem Raça/PCD declarados)'
    
    df['Cota_Raca'] = vaga_series.apply(define_raca_row)
    
    return df

# Executa a carga de dados
df = load_data()

# --- FUNÇÃO DE FILTRO INTELIGENTE (UX) ---
def multiselect_com_todos(label, options, key):
    """Cria um multiselect onde 'Todos' é exclusivo."""
    # Garante que 'Todos' esteja na lista
    options_with_all = ["Todos"] + sorted([opt for opt in options if opt != "Todos"])
    
    # Inicializa sessão
    if key not in st.session_state:
        st.session_state[key] = ["Todos"]
    
    # Lógica de exclusividade
    def on_change():
        selected = st.session_state[key]
        if "Todos" in selected and len(selected) > 1:
            if selected[0] == "Todos": # Se 'Todos' estava antes, remove 'Todos'
                st.session_state[key] = selected[1:]
            else: # Se 'Todos' foi clicado por último, remove o resto
                st.session_state[key] = ["Todos"]
        elif not selected:
            st.session_state[key] = ["Todos"]

    selection = st.sidebar.multiselect(label, options=options_with_all, key=key, on_change=on_change)
    # Retorna todas as opções se 'Todos' estiver selecionado
    return options if "Todos" in selection else selection

# --- SIDEBAR (FILTROS) ---
st.sidebar.title("🔍 Filtros Avançados")
st.sidebar.markdown("Use as opções abaixo para filtrar a análise.")

filtros = {}

# 1. Filtro de Área (Hierarquia superior)
filtros['Area'] = multiselect_com_todos(
    "Selecione a Área de Conhecimento:", 
    df["Area"].dropna().unique(), 
    key="filtro_area"
)

# 2. Demais filtros
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

# --- APLICAÇÃO DOS FILTROS ---
# Criação do DataFrame Filtrado
df_filtered = df[
    (df["Area"].isin(filtros['Area'])) & 
    (df["Curso"].isin(filtros['Curso'])) & 
    (df["Turno"].isin(filtros['Turno'])) &
    (df["Semestre"].isin(filtros['Semestre'])) &
    (df["Grau"].isin(filtros['Grau']))
].copy()

# Remove dados sem gênero para não quebrar gráficos
df_filtered = df_filtered.dropna(subset=['Gênero'])

# --- CONSTRUÇÃO DO DASHBOARD ---
st.title("📊 Análise de Gênero - Vestibular")
st.markdown("---")

# KPIs Principais (Topo)
col1, col2, col3 = st.columns(3)
total_vagas = len(df_filtered)

if total_vagas > 0:
    pct_fem = (df_filtered[df_filtered['Gênero'] == 'F'].shape[0] / total_vagas * 100)
    pct_masc = (df_filtered[df_filtered['Gênero'] == 'M'].shape[0] / total_vagas * 100)
else:
    pct_fem = 0
    pct_masc = 0

col1.metric("👥 Total de Candidatos", total_vagas)
col2.metric("👩 Mulheres", f"{pct_fem:.1f}%")
col3.metric("👨 Homens", f"{pct_masc:.1f}%")

st.markdown("---")

# Verificação se o filtro retornou vazio
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# --- CRIAÇÃO DAS ABAS ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Visão Geral", "🎯 Performance & Cotas", "🌐 Socioeconômico", "💾 Base de Dados"])

# --- ABA 1: VISÃO GERAL ---
with tab1:
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("Proporção Global")
        fig_pie = px.pie(
            df_filtered, names='Gênero', 
            color='Gênero', color_discrete_map=COLOR_MAP, 
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_g2:
        # Lógica adaptável: Se muitas áreas selecionadas, mostra gráfico por Área. Senão, por Turno.
        if len(filtros['Area']) > 1 or len(filtros['Area']) == len(df['Area'].unique()):
             st.subheader("Gênero por Área de Conhecimento")
             df_area_g = df_filtered.groupby(['Area', 'Gênero']).size().reset_index(name='Contagem')
             fig_bar = px.bar(
                 df_area_g, x='Contagem', y='Area', color='Gênero', 
                 orientation='h', color_discrete_map=COLOR_MAP, barmode='group'
             )
             st.plotly_chart(fig_bar, use_container_width=True)
        else:
             st.subheader("Distribuição por Turno")
             df_turno = df_filtered.groupby(['Turno', 'Gênero']).size().reset_index(name='Contagem')
             fig_bar = px.bar(
                 df_turno, x='Turno', y='Contagem', color='Gênero', 
                 barmode='group', color_discrete_map=COLOR_MAP, text_auto=True
             )
             st.plotly_chart(fig_bar, use_container_width=True)
             st.subheader("Gênero por Tipo de Grau")

    df_grau = df_filtered.groupby(['Grau', 'Gênero']).size().reset_index(name='Contagem')

    fig_grau = px.bar(df_grau, x='Grau', y='Contagem', color='Gênero', barmode='group',
                      color_discrete_map=COLOR_MAP, text_auto=True)

    st.plotly_chart(fig_grau, use_container_width=True)

# --- ABA 2: PERFORMANCE E COTAS ---
with tab2:
    st.subheader("Análise de Classificação (Rank)")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        fig_box = px.box(
            df_filtered, x='Gênero', y='Rank', color='Gênero', 
            color_discrete_map=COLOR_MAP, points="outliers",
            title="Distribuição de Rank (Boxplot)"
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_p2:
        fig_hist = px.histogram(
            df_filtered, x="Rank", color="Gênero", 
            marginal="box", nbins=50, 
            color_discrete_map=COLOR_MAP, barmode="overlay",
            title="Histograma de Notas"
        )
        fig_hist.update_traces(opacity=0.75)
        st.plotly_chart(fig_hist, use_container_width=True)

    st.subheader("Principais Formas de Entrada")
    # Pega apenas o Top 10 códigos mais frequentes
    top_vagas = df_filtered['Vaga'].value_counts().head(10).index
    df_vaga_top = df_filtered[df_filtered['Vaga'].isin(top_vagas)]
    
    df_vaga_agrupada = df_vaga_top.groupby(['Vaga', 'Gênero']).size().reset_index(name='Contagem')
    df_vaga_agrupada = df_vaga_agrupada.sort_values(by='Contagem', ascending=False)
    
    fig_cod_vaga = px.bar(
        df_vaga_agrupada, x='Vaga', y='Contagem', color='Gênero', 
        barmode='group', color_discrete_map=COLOR_MAP, text_auto = True
    )
    st.plotly_chart(fig_cod_vaga, use_container_width=True)

# --- ABA 3: SOCIOECONÔMICO E INCLUSÃO ---
with tab3:
    st.subheader("🌐 Análise Socioeconômica e Racial")
    
    # 1. CÁLCULO DOS KPIs GERAIS
    # PPI + Quilombolas (Ações Afirmativas Raciais)
    qtd_ppi = df_filtered[df_filtered['Cota_Raca'].str.contains('PPI|Quilombola', regex=True)].shape[0]
    pct_ppi = (qtd_ppi / total_vagas * 100) if total_vagas > 0 else 0
    
    # Baixa Renda
    qtd_baixa_renda = df_filtered[df_filtered['Cota_Renda'] == 'Baixa Renda'].shape[0]
    pct_baixa_renda = (qtd_baixa_renda / total_vagas * 100) if total_vagas > 0 else 0

    # PCD (Calculando direto da coluna Vaga para garantir precisão)
    qtd_pcd = df_filtered[df_filtered['Vaga'].str.contains('PCD', na=False)].shape[0]
    pct_pcd = (qtd_pcd / total_vagas * 100) if total_vagas > 0 else 0

    # Escola Pública (Total de Cotistas)
    qtd_ep = df_filtered[df_filtered['Tipo_Vaga'] == 'Cota'].shape[0]
    pct_ep = (qtd_ep / total_vagas * 100) if total_vagas > 0 else 0

    # 2. EXIBIÇÃO DOS KPIs (4 Colunas)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(label="Total de Cotas", value=f"{qtd_ep} ({pct_ep:.1f}%)")
    kpi2.metric(label="PPI e Quilombolas", value=f"{qtd_ppi} ({pct_ppi:.1f}%)")
    kpi3.metric(label="Baixa Renda", value=f"{qtd_baixa_renda} ({pct_baixa_renda:.1f}%)")
    kpi4.metric(label="PCD", value=f"{qtd_pcd} ({pct_pcd:.1f}%)")

    st.markdown("---")

    # 3. GRÁFICOS DE RAÇA E RENDA (Apenas Cotistas)
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
            # Gráfico de Raça
            # Simplifica rótulo para caber no gráfico
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

    # 4. SEÇÃO DE ACESSIBILIDADE (PCD)
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
            # Gráfico 2: Modalidade
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

# --- ABA 4: DADOS E DOWNLOAD ---
with tab4:
    st.subheader("📋 Dados Detalhados")
    st.dataframe(df_filtered, use_container_width=True)
    
    # Botão de Download
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados Filtrados (CSV)",
        data=csv,
        file_name='vestibular_filtrado.csv',
        mime='text/csv',
    )