import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid
import pandas as pd
import numpy as np
import math
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from lifelines import KaplanMeierFitter, NelsonAalenFitter, WeibullFitter, CoxPHFitter
from lifelines.statistics import logrank_test, multivariate_logrank_test

import constant


@st.cache_data
def load_data():
    data = pd.read_csv(constant.data_path, sep=';', encoding='utf-8')
    data = data.rename(columns={'time': 'Time'})
    data = data.drop('Numero_paciente', axis=1)
    raw_data = data.copy()
    data = data.convert_dtypes()
    return data, raw_data

def reset_filters():
    st.session_state.select_sex = 'TOUT'
    st.session_state.select_anemia = 'TOUT'
    st.session_state.select_hipercalcemia = 'TOUT'
    st.session_state.select_ttomm1 = list(data['TtoMM1'].unique())
    st.session_state.select_ttomm2 = list(data['TtoMM2'].unique())
    check_country()
    check_erc()
    check_fish()
    check_age_range()
    check_myeloma()


def check_erc():
    st.session_state.select_erc = constant.list_erc

def check_fish():
    st.session_state.select_fish = constant.list_fish

def check_country():
    st.session_state.select_country = list(data['Country'].unique())

def check_hospital():
    st.session_state.select_hospital = list(data['Hospital'].unique())

def check_myeloma():
    st.session_state.select_myeloma = list(data['TypeMyeloma'].unique())

def check_age_range():
    st.session_state.select_age_range = list(data['Age_range'].unique())

def check_ttomm1():
    st.session_state.select_ttomm1 = list(data['TtoMM1'].unique())

def check_ttomm2():
    st.session_state.select_ttomm2 = list(data['TtoMM2'].unique())


st.set_page_config(layout="wide")

hide_streamlit_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

data, raw_data = load_data()
n = len(data)

#st.write(data.dtypes)

with st.sidebar:
    st.subheader('Selection des filtres')
    filters_text = st.container() 
    sex = st.selectbox('Genre', ('Tout', 'M', 'F'), key='select_sex')
    anemia = st.selectbox('Anémie', ('Tout', 'Oui', 'Non'), key='select_anemia')
    hipercalcemia = st.selectbox("Hypercalcémie", ('Tout', 'Oui', 'Non'), key='select_hipercalcemia')
    
    select, button = st.columns([8, 2])
    with select:
        erc = st.multiselect('ERC', constant.list_erc, constant.list_erc, key='select_erc')
    with button:
        st.write('')
        st.write('')
        st.button('Tout Cocher', on_click=check_erc, key='check_erc')

    select, button = st.columns([8, 2])
    with select:
        fish = st.multiselect('FISH', constant.list_fish, constant.list_fish, key='select_fish')
    with button:
        st.write('')
        st.write('')
        st.button('Tout Cocher', on_click=check_fish, key='check_fish')
    
    select, button = st.columns([8, 2])
    with select:
        country = st.multiselect('Pays', list(data['Country'].unique()), list(data['Country'].unique()), key='select_country')
    with button:
        st.write('')
        st.write('')
        st.button('Tout Cocher', on_click=check_country, key='check_country')
    
    select, button = st.columns([8, 2])
    with select:
        hospital = st.multiselect('Hôpital', list(data['Hospital'].unique()), list(data['Hospital'].unique()), key='select_hospital')
    with button:
        st.write('')
        st.write('')
        st.button('Tout Cocher', on_click=check_hospital, key='check_hospital')
    
    select, button = st.columns([8, 2])
    with select:
        age_range = st.multiselect("Tranche d'âge", list(data['Age_range'].unique()), list(data['Age_range'].unique()), key='select_age_range')
    with button:
        st.write('')
        st.write('')
        st.button('Tout Cocher', on_click=check_age_range, key='check_age_range')
    
    select, button = st.columns([8, 2])
    with select:
        myeloma = st.multiselect('Type de myélome', list(data['TypeMyeloma'].unique()), list(data['TypeMyeloma'].unique()), key='select_myeloma')
    with button:
        st.write('')
        st.write('')
        st.button('Tout Cocher', on_click=check_myeloma, key='check_myeloma')
    
    select, button = st.columns([8, 2])
    with select:
        ttomm1 = st.multiselect('Traitement du myélome multiple 1', list(data['TtoMM1'].unique()), list(data['TtoMM1'].unique()), key='select_ttomm1')
    with button:
        st.write('')
        st.write('')
        st.button('Tout Cocher', on_click=check_ttomm1, key='check_ttomm1')
    
    select, button = st.columns([8, 2])
    with select:
        ttomm2 = st.multiselect('Traitement du myélome multiple 2', list(data['TtoMM2'].unique()), list(data['TtoMM2'].unique()), key='select_ttomm2')
    with button:
        st.write('')
        st.write('')
        st.button('Tout Cocher', on_click=check_ttomm2, key='check_ttomm2')
    selected_data = data.copy()

    if not sex == 'Tout':
        selected_data = selected_data[(selected_data['Genero'] == sex)]

    if not anemia == 'Tout':
        if not anemia == "Oui":
            selected_data = selected_data[(selected_data['Anemia'] == "SI")]
        if not anemia == "Non":
            selected_data = selected_data[(selected_data['Anemia'] == "NO")]  

    if not hipercalcemia == 'Tout':
        if not hipercalcemia == "Oui":
            selected_data = selected_data[(selected_data['Hipercalcemia'] == "SI")]
        if not hipercalcemia == "Non":
            selected_data = selected_data[(selected_data['Hipercalcemia'] == "NO")]  

    erc_leger = "Léger" in erc
    erc_moderée = "Modérée" in erc
    erc_sévère = "Sévère" in erc
    erc_dialisis = "Dialisis" in erc
    sans_erc = "Sans ERC" in erc
    selected_data = selected_data[
        (erc_leger & (selected_data['ERC_Leve'] == "SI")) |
        (erc_moderée & (selected_data['ERC_moderada'] == "SI")) |
        (erc_sévère & (selected_data['ERC_severa'] == "SI")) |
        (erc_dialisis & (selected_data['ERC_dialisis'] == "SI")) |
        (sans_erc & (
            (selected_data['ERC_Leve'] == "NO") |
            (selected_data['ERC_moderada'] == "NO") |
            (selected_data['ERC_severa'] == "NO") |
            (selected_data['ERC_dialisis'] == "NO")
        ))
    ]

    fish_del17p1 = "del17p1" in fish
    fish_t_1114 = "t_1114" in fish
    fish_t414 = "t414" in fish
    fish_amp1q211 = "amp1q211" in fish
    fish_autres = "Autres" in fish
    sans_fish = "Aucun" in fish
    selected_data = selected_data[
        (fish_del17p1 & (selected_data['FISHdel17p1'] == "SI")) |
        (fish_t_1114 & (selected_data['FISHt_1114'] == "SI")) |
        (fish_amp1q211 & (selected_data['FISHamp1q211'] == "SI")) |
        (fish_t414 & (selected_data['FISHt414'] == "SI")) |
        (fish_autres & (selected_data['FISHother'] == "SI")) |
        (sans_fish & (
            (selected_data['FISHdel17p1'] == "NO") |
            (selected_data['FISHt_1114'] == "NO") |
            (selected_data['FISHamp1q211'] == "NO") |
            (selected_data['FISHt414'] == "NO") |
            (selected_data['FISHother'] == "NO")
        ))
    ]


    selected_data = selected_data[(selected_data['TypeMyeloma'].isin(myeloma)) &
                                  (selected_data['Country'].isin(country)) &
                                  (selected_data['Hospital'].isin(hospital)) &
                                  (selected_data['Age_range'].isin(age_range)) &
                                  (selected_data['TtoMM1'].isin(ttomm1)) &
                                  (selected_data['TtoMM2'].isin(ttomm2))]
    n = len(selected_data)
    filters_text.write(f'Les filtres appliqués ont sélectionné {n} patients.')
    st.button('Réinitialiser', on_click=reset_filters)

st.title('Analyse de survie - M1 MIAGE')

with st.expander('Voir les données'):
    st.write(data)

tab_acc, tab_stats, tab_survival, tab_comparison, tab_tests, tab_cox, tab_economic, tab_miss = st.tabs(constant.menu)

with tab_acc:
    st.write(constant.home)

with tab_stats:
    if n > 0:
        chosen_feature_fr = st.selectbox("Sélection d'une variable particulière à étudier", constant.selected_cols_desc_keys)
        chosen_feature = constant.selected_cols_desc[chosen_feature_fr]
        description = selected_data[chosen_feature].describe()

        st.write(description)
        color_list = constant.colors_desc 

        if 'mean' in description.keys():
            # Histogram of continuous feature
            range = description['max'] - description['min']
            fig = px.histogram(x=selected_data[chosen_feature], range_x=(description['min'],description['max']+.05*range))
            color_discrete_sequence=color_list * len(selected_data[chosen_feature])
            fig.update_traces(xbins=dict(start=description['min'], end=description['max']+.05*range, size=.05*range))
            fig.update_layout(
                xaxis_title_text=chosen_feature,
                yaxis_title_text='Quantité'
            )
            st.subheader(f'Représentation graphique : {chosen_feature_fr} ')
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Histogram of categorical feature
            x = data[chosen_feature].unique()
            y_temp = selected_data[chosen_feature].value_counts(sort=False)
            y = []
            for val in x:
                if val in y_temp.keys():
                    y.append(y_temp[val])
                else:
                    y.append(0)

            fig = px.bar(x=x, y=y, color=x, color_discrete_sequence=color_list)
            fig.update_layout(
                xaxis_title_text='Type',
                yaxis_title_text='Quantité'
            )
            st.subheader(f'Représentation graphique : {chosen_feature_fr} ')
            st.plotly_chart(fig, use_container_width=True)
        
with tab_survival:
    if n > 0:
        # Kaplan Meier
        kmf = KaplanMeierFitter()
        selected_data.loc[selected_data.Evento == 0, 'Dead'] = 0
        selected_data.loc[selected_data.Evento == 1, 'Dead'] = 1
        kmf.fit(durations=selected_data['Time'], event_observed=selected_data['Dead'])
        
        fig = go.Figure()
        x = kmf.survival_function_['KM_estimate'].index.values
        y = kmf.survival_function_['KM_estimate']
        y_upper = kmf.confidence_interval_['KM_estimate_upper_0.95']
        y_lower = kmf.confidence_interval_['KM_estimate_lower_0.95']
        fig.add_traces([go.Scatter(x=x, y=y_upper, line=dict(shape='hv'), mode='lines',
                                    line_color='rgba(0,0,0,0)', showlegend=False),
                        go.Scatter(x=x, y=y_lower, line=dict(shape='hv'), mode='lines',
                                    line_color='rgba(0,0,0,0)', name='Interval de Confiance', fill='tonexty', fillcolor='rgba(206, 131, 255, 0.4)')])
        fig.add_traces(go.Scatter(x=x, y=y, line=dict(shape='hv', width=2.5), mode='lines', line_color='rgba(171, 23, 216, 1)', name='KM estimé'))
        fig.update_layout(
            xaxis_title_text="Jour d'exposition",
            yaxis_title_text="Probabilité que la maladie n'empire pas"
        )
        st.subheader("Fonction de Survie des patients")
        st.write('Estimation de la probabilité de décès à l’aide de Kaplan-Meier')
        # st.write(f'The median time is: {kmf.median_survival_time_}')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader('Kaplan-Meier a estimé la survie pour chacun des jours suivants:')
        days = [0,5,11,100,200]
        for i, day in enumerate(days):
            st.write(f'Estimation pour {day} jours : {kmf.predict(day) * 100: .02f}%')

        nb_days = st.number_input('Entrer un nombre de jour ', min_value=0, value=100, step=1, format='%d')
        st.write(f'Estimation pour {nb_days} jours : {kmf.predict(nb_days) * 100: .02f}%')

        st.subheader('Table d’activités Kaplan-Meier')
        st.write(kmf.event_table)

        st.markdown("""---""")

        # Nelson Aalen
        naf = NelsonAalenFitter()
        naf.fit(durations=selected_data['Time'], event_observed=selected_data['Dead'])

        fig = go.Figure()
        x = naf.cumulative_hazard_['NA_estimate'].index.values
        y = naf.cumulative_hazard_['NA_estimate']
        y_upper = naf.confidence_interval_['NA_estimate_upper_0.95']
        y_lower = naf.confidence_interval_['NA_estimate_lower_0.95']
        fig.add_traces([go.Scatter(x=x, y=y_upper, line=dict(shape='hv'), mode='lines',
                                    line_color='rgba(0,0,0,0)', showlegend=False),
                        go.Scatter(x=x, y=y_lower, line=dict(shape='hv'), mode='lines',
                                    line_color='rgba(0,0,0,0)', name='Interval de Confiance', fill='tonexty', fillcolor='rgba(206, 131, 255, 0.4)')])
        fig.add_traces(go.Scatter(x=x, y=y, line=dict(shape='hv', width=2.5), mode='lines', line_color='rgba(171, 23, 216, 1)', name='NA estimé'))
        fig.update_layout(
            xaxis_title_text='Temps',
            yaxis_title_text='Risque'
        )
        st.subheader('Estimation des taux de risque cumulatifs à l’aide de Nelson-Aalen')
        st.write('L’estimateur de Nelson–Aalen est un estimateur non paramétrique de la fonction du taux de risque cumulatif')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""---""")

        # Weibull
        wf = WeibullFitter()
        wf.fit(durations=selected_data['Time'].astype(float), event_observed=selected_data['Dead'].astype(float))

        fig = go.Figure()
        x = wf.cumulative_hazard_['Weibull_estimate'].index.values
        y = wf.cumulative_hazard_['Weibull_estimate']
        y_upper = wf.confidence_interval_['Weibull_estimate_upper_0.95']
        y_lower = wf.confidence_interval_['Weibull_estimate_lower_0.95']
        fig.add_traces([go.Scatter(x=x, y=y_upper, line=dict(shape='hv'), mode='lines',
                                    line_color='rgba(0,0,0,0)', showlegend=False),
                        go.Scatter(x=x, y=y_lower, line=dict(shape='hv'), mode='lines',
                                    line_color='rgba(0,0,0,0)', name='Interval de Confiance', fill='tonexty', fillcolor='rgba(206, 131, 255, 0.4)')])
        fig.add_traces(go.Scatter(x=x, y=y, line=dict(shape='hv', width=2.5), mode='lines', line_color='rgba(171, 23, 216, 1)', name='Weibull estimé'))
        fig.update_layout(
            xaxis_title_text='Temps',
            yaxis_title_text='Risque'
        )
        st.subheader('Estimation des taux de risque cumulatifs à l’aide du modèle de Weibull')
        st.write('Le modèle de Weibull pour les données de survie est un modèle paramétrique, il a une forme fonctionnelle avec des paramètres que nous ajustons les données pour')
        st.plotly_chart(fig, use_container_width=True)

        
with tab_comparison:
    # Select only categorical and handled numerical variables
    selected_cols = constant.selected_cols_group_keys

    surv_comparison_feature = st.selectbox('Variable à utiliser pour la comparaison de survie', selected_cols)
    colors = constant.colors

    if st.checkbox("Montrer l'Interval de Confiance"):
        conf = True
    else:
        conf = False
    
    if st.checkbox('Afficher les courbes sur une grille'):
        grid = True
    else:
        grid = False

    data_group = data[constant.selected_cols_group[surv_comparison_feature]]
    cat_values = data_group.dropna().unique()
    kmf = KaplanMeierFitter()
    data.loc[data.Evento == 0, 'Dead'] = 0
    data.loc[data.Evento == 1, 'Dead'] = 1
    grid_idcs = None
    if grid:
        if len(cat_values) == 1:
            fig = go.Figure()
            grid_idcs = 1
        elif len(cat_values) == 2:
            fig = make_subplots(rows=1, cols=2, x_title='Dias de Exposicion', y_title='Probabilidad de no desmejorar en la enfermedad')
            grid_idcs = 2
        elif len(cat_values) == 3:
            fig = make_subplots(rows=1, cols=3, x_title='Dias de Exposicion', y_title='Probabilidad de no desmejorar en la enfermedad')
            grid_idcs = 3
        elif len(cat_values) > 3:
            fig = make_subplots(rows=math.ceil(len(cat_values) / 3), cols=3, x_title='Dias de Exposicion', y_title='Probabilidad de no desmejorar en la enfermedad')
            grid_idcs = 6
    else:
        fig = go.Figure()
    ## Iterate over all categorical values and plot one survival curve for each
    for i, cat_val in enumerate(cat_values):
        c = colors[i % len(colors)]
        flag = (data_group == cat_val)
        kmf.fit(durations=data[flag]['Time'], event_observed=data[flag]['Dead'])
        x = kmf.survival_function_['KM_estimate'].index.values
        y = kmf.survival_function_['KM_estimate']
        y_upper = kmf.confidence_interval_['KM_estimate_upper_0.95']
        y_lower = kmf.confidence_interval_['KM_estimate_lower_0.95']
        row = None
        col = None
        if grid_idcs == 2 or grid_idcs == 3:
            row = 1
            col = i + 1
        if grid_idcs == 6:
            row = (i // 3) + 1
            col = (i % 3) + 1
        if conf:
            fig.add_traces([go.Scatter(x=x, y=y_upper, line=dict(shape='hv'), mode='lines',
                                        line_color='rgba(0,0,0,0)', showlegend=False),
                            go.Scatter(x=x, y=y_lower, line=dict(shape='hv'), mode='lines',
                                        line_color='rgba(0,0,0,0)', showlegend=False,
                                        fill='tonexty', fillcolor=f'rgba({c[0]}, {c[1]}, {c[2]}, 0.2)')], rows=row, cols=col)
        fig.add_traces(go.Scatter(x=x, y=y, line=dict(shape='hv', width=2.5), mode='lines', line_color=f'rgba({c[0]}, {c[1]}, {c[2]}, 1)',
                                name=f'{surv_comparison_feature}={cat_val}'), rows=row, cols=col)
    if not grid or grid_idcs == 1:
        fig.update_layout(
            # title_text='Estimacion de curvas de sobrevida',
            xaxis_title_text='Dias de Exposicion',
            yaxis_title_text='Probabilidad de no desmejorar en la enfermedad'
        )
    # else:
    #     fig.update_layout(title_text='Estimacion de curvas de sobrevida')
    st.subheader('Estimation de la survie de Kaplan Meier')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")

    # Nelson Aalen
    naf = NelsonAalenFitter()
    grid_idcs = None
    if grid:
        if len(cat_values) == 1:
            fig = go.Figure()
            grid_idcs = 1
        elif len(cat_values) == 2:
            fig = make_subplots(rows=1, cols=2, x_title='Time', y_title='Hazard')
            grid_idcs = 2
        elif len(cat_values) == 3:
            fig = make_subplots(rows=1, cols=3, x_title='Time', y_title='Hazard')
            grid_idcs = 3
        elif len(cat_values) > 3:
            fig = make_subplots(rows=math.ceil(len(cat_values) / 3), cols=3, x_title='Time', y_title='Hazard')
            grid_idcs = 6
    else:
        fig = go.Figure()
    ## Iterate over all categorical values and plot one survival curve for each
    for i, cat_val in enumerate(cat_values):
        c = colors[i % len(colors)]
        flag = (data_group == cat_val)
        naf.fit(durations=data[flag]['Time'], event_observed=data[flag]['Dead'])
        x = naf.cumulative_hazard_['NA_estimate'].index.values
        y = naf.cumulative_hazard_['NA_estimate']
        y_upper = naf.confidence_interval_['NA_estimate_upper_0.95']
        y_lower = naf.confidence_interval_['NA_estimate_lower_0.95']
        row = None
        col = None
        if grid_idcs == 2 or grid_idcs == 3:
            row = 1
            col = i + 1
        if grid_idcs == 6:
            row = (i // 3) + 1
            col = (i % 3) + 1
        if conf:
            fig.add_traces([go.Scatter(x=x, y=y_upper, line=dict(shape='hv'), mode='lines',
                                        line_color='rgba(0,0,0,0)', showlegend=False),
                            go.Scatter(x=x, y=y_lower, line=dict(shape='hv'), mode='lines',
                                        line_color='rgba(0,0,0,0)', showlegend=False,
                                        fill='tonexty', fillcolor=f'rgba({c[0]}, {c[1]}, {c[2]}, 0.2)')], rows=row, cols=col)
        fig.add_traces(go.Scatter(x=x, y=y, line=dict(shape='hv', width=2.5), mode='lines', line_color=f'rgba({c[0]}, {c[1]}, {c[2]}, 1)',
                                name=f'{surv_comparison_feature}={cat_val}'), rows=row, cols=col)
    if not grid or grid_idcs == 1:
        fig.update_layout(
            # title_text='Nelson Aalen Cumulative hazard',
            xaxis_title_text='Temps',
            yaxis_title_text='Risque'
        )
    # else:
    #     fig.update_layout(title_text='Nelson Aalen Cumulative hazard')
    st.subheader('Nelson Aalen Risque cumulé')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")

    # Weibull
    wf = WeibullFitter()
    grid_idcs = None
    if grid:
        if len(cat_values) == 1:
            fig = go.Figure()
            grid_idcs = 1
        elif len(cat_values) == 2:
            fig = make_subplots(rows=1, cols=2, x_title='Time', y_title='Hazard')
            grid_idcs = 2
        elif len(cat_values) == 3:
            fig = make_subplots(rows=1, cols=3, x_title='Time', y_title='Hazard')
            grid_idcs = 3
        elif len(cat_values) > 3:
            fig = make_subplots(rows=math.ceil(len(cat_values) / 3), cols=3, x_title='Time', y_title='Hazard')
            grid_idcs = 6
    else:
        fig = go.Figure()
    ## Iterate over all categorical values and plot one survival curve for each
    for i, cat_val in enumerate(cat_values):
        c = colors[i % len(colors)]
        flag = (data_group == cat_val)
        wf.fit(durations=data[flag]['Time'].astype(float), event_observed=data[flag]['Dead'].astype(float))
        x = wf.cumulative_hazard_['Weibull_estimate'].index.values
        y = wf.cumulative_hazard_['Weibull_estimate']
        y_upper = wf.confidence_interval_['Weibull_estimate_upper_0.95']
        y_lower = wf.confidence_interval_['Weibull_estimate_lower_0.95']
        row = None
        col = None
        if grid_idcs == 2 or grid_idcs == 3:
            row = 1
            col = i + 1
        if grid_idcs == 6:
            row = (i // 3) + 1
            col = (i % 3) + 1
        if conf:
            fig.add_traces([go.Scatter(x=x, y=y_upper, line=dict(shape='hv'), mode='lines',
                                        line_color='rgba(0,0,0,0)', showlegend=False),
                            go.Scatter(x=x, y=y_lower, line=dict(shape='hv'), mode='lines',
                                        line_color='rgba(0,0,0,0)', showlegend=False,
                                        fill='tonexty', fillcolor=f'rgba({c[0]}, {c[1]}, {c[2]}, 0.2)')], rows=row, cols=col)
        fig.add_traces(go.Scatter(x=x, y=y, line=dict(shape='hv', width=2.5), mode='lines', line_color=f'rgba({c[0]}, {c[1]}, {c[2]}, 1)',
                                name=f'{surv_comparison_feature}={cat_val}'), rows=row, cols=col)
    if not grid or grid_idcs == 1:
        fig.update_layout(
            # title_text='Weibull Cumulative hazard',
            xaxis_title_text='Temps',
            yaxis_title_text='Risque'
        )
    # else:
        # fig.update_layout(title_text='Weibull Cumulative hazard')
    st.subheader('Weibull Risque cumulé')
    st.plotly_chart(fig, use_container_width=True)

with tab_tests:
    selected_cols = constant.selected_cols_tests_keys

    tests_col = st.selectbox('Variable sur laquelle exécuter les tests logrank', selected_cols)
    data_tests = constant.selected_cols_tests[tests_col]
    test_cat_values = data[data_tests].dropna().unique()

    if len(data[data_tests].dropna().unique()) == 2:
        flag = (data[data_tests] == test_cat_values[0])
        results = logrank_test(data[flag]['Time'], data[~flag]['Time'], data[flag]['Dead'], data[~flag]['Dead'], alpha=.99)
    else:
        df = pd.DataFrame({
            'durations': data['Time'], # Time 
            'groups': data[data_tests], # Modalities of variable could be strings too
            'events': data['Dead'], # Event
        })
        results = multivariate_logrank_test(df['durations'], df['groups'], df['events'])
    st.subheader('Test statistique de comparaison des fonctions de survie')
    st.write('Comparer la différence entre deux fonctions de survie ou plus')
    st.write('Le test de Mantel-Haenszel appelé log-rank est le plus utilisé, et le plus performant. Un autre test peut être utilisé : le test de Wilcoxon.')
    st.write("Hypothèse nulle H0 : Il n’y a pas de différence de survie entre les groupes d’étude")
    st.write(results)
    
    kmf = KaplanMeierFitter()
    fig = go.Figure()
    ## Iterate over all categorical values and plot one survival curve for each
    for i, cat_val in enumerate(test_cat_values):
        c = colors[i % len(colors)]
        flag = (data[data_tests] == cat_val)
        kmf.fit(durations=data[flag]['Time'], event_observed=data[flag]['Dead'])
        x = kmf.survival_function_['KM_estimate'].index.values
        y = kmf.survival_function_['KM_estimate']
        y_upper = kmf.confidence_interval_['KM_estimate_upper_0.95']
        y_lower = kmf.confidence_interval_['KM_estimate_lower_0.95']
        fig.add_traces([go.Scatter(x=x, y=y_upper, line=dict(shape='hv'), mode='lines',
                                    line_color='rgba(0,0,0,0)', showlegend=False),
                        go.Scatter(x=x, y=y_lower, line=dict(shape='hv'), mode='lines',
                                    line_color='rgba(0,0,0,0)', showlegend=False,
                                    fill='tonexty', fillcolor=f'rgba({c[0]}, {c[1]}, {c[2]}, 0.2)')])
        fig.add_traces(go.Scatter(x=x, y=y, line=dict(shape='hv', width=2.5), mode='lines', line_color=f'rgba({c[0]}, {c[1]}, {c[2]}, 1)',
                                name=f'{tests_col}={cat_val}'))
    fig.update_layout(
        xaxis_title_text='Dias de Exposicion',
        yaxis_title_text='Probabilidad de no desmejorar en la enfermedad'
    )
    st.write('')
    st.subheader('Estimation de la survie de Kaplan Meier')
    st.plotly_chart(fig, use_container_width=True)

with tab_cox:
    cox_variables = st.multiselect('Sélectionner des covariables', raw_data.columns, ['Anemia', 'Hipercalcemia', 'Country', 'Age'])
    if cox_variables:
        cph = CoxPHFitter()
        cph.fit(raw_data, duration_col='Time', event_col='Evento', formula=' + '.join(cox_variables))
        st.subheader('Paramètres du modèle Cox :')
        st.write(cph.params_)
        st.subheader('Valeurs p :')
        p_values = cph.summary.p
        tmp_df = pd.DataFrame(p_values)
        tmp_df['Significance'] = np.where(tmp_df['p']<.05, 'Incidence importante sur la survie', 'Aucun impact significatif sur la survie')
        st.write(tmp_df)
        st.subheader('Rapports de risque:')
        ratios = cph.hazard_ratios_
        st.write(ratios)
        st.write(f'La variable {list(ratios.nlargest(1).index)[0]} a le plus grand impact sur la mort')
        st.subheader('Résultats détaillés :')
        st.write(cph.summary)

with tab_economic:
    treatment = st.selectbox('Selectionner un Traitement du myélome multiple 1 :', data['TtoMM1'].unique())
    treatment_data = data.copy()
    treatment_data = treatment_data[(treatment_data['TtoMM1'] == treatment)]
    remission_prob = treatment_data['Remission'].sum() / len(treatment_data)
    st.subheader(f'Rentabilité : {treatment_data["Cost"].mean() / remission_prob:.02f}$')
    st.subheader(f'Fardeau de la détresse : {treatment_data["Cost"].sum():.02f}$')
    country = st.selectbox('Selectionner un pays :', data['Country'].unique())
    country_data = data.copy()
    country_data = country_data[(country_data['Country'] == country)]
    hospital = st.selectbox('Selectionner un Hôpital :', country_data['Hospital'].unique())
    country_data = country_data[(country_data['Hospital'] == hospital)]
    country_data = country_data[(country_data['TtoMM1'] == treatment)]
    st.subheader(f'Analyse d’impact budgétaire pour le traitement dans certains pays et hôpitaux : {0 if len(country_data) == 0 else country_data["Cost"].sum():.02f}$')

with tab_miss:
    st.subheader('Sélectionner les colonnes à imputer')

    df_miss_select = pd.DataFrame({'Cols': data.columns, 'Types': np.array(data.dtypes), 'NaNs': np.array(data.isna().sum())})
    df_miss_select['Types'] = list(map(lambda x: x.__str__(), df_miss_select['Types']))
    df_miss_select = df_miss_select.convert_dtypes()

    gb = GridOptionsBuilder.from_dataframe(df_miss_select)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children")
    gridOptions = gb.build()

    grid_response = AgGrid(
        df_miss_select,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
    )

    df_selected = pd.DataFrame(grid_response['selected_rows'] )

    if 'Cols' in df_selected:
        imputed_data = data
        if st.button('Apply imputation to selected columns'):
            for col in np.array(df_selected['Cols']):
                if imputed_data[col].dtype == 'string':
                    imputed_data[col] = imputed_data[col].fillna(value=imputed_data[col].mode()[0])
                if imputed_data[col].dtype == 'Float64':
                    imputed_data[col] = imputed_data[col].fillna(value=imputed_data[col].mean())
                if imputed_data[col].dtype == 'Int64':
                    imputed_data[col] = imputed_data[col].fillna(value=int(imputed_data[col].median()))

            st.write('')
            st.subheader('Imputed data:')

            st.write(imputed_data)

            st.download_button(
                label="Download imputed data as CSV",
                data=imputed_data.to_csv().encode('utf-8'),
                file_name='imputed_data.csv',
                mime='text/csv',
            )
