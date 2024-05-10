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


@st.cache_data
def load_data():
    data_path = './data/mock_data_4.csv'
    data = pd.read_csv(data_path, sep=';', encoding='utf-8')
    data = data.rename(columns={'time': 'Time'})
    data = data.drop('Numero_paciente', axis=1)
    raw_data = data.copy()
    data = data.convert_dtypes()
    return data, raw_data

def reset_filters():
    st.session_state.select_sex = 'All'
    st.session_state.select_anemia = 'All'
    st.session_state.select_ttomm1 = list(data['TtoMM1'].unique())
    st.session_state.select_ttomm2 = list(data['TtoMM2'].unique())

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

# st.write(data.dtypes)

with st.sidebar:
    st.subheader('Filters selection')
    filters_text = st.container()
    sex = st.selectbox('Gender', ('All', 'M', 'F'), key='select_sex')
    anemia = st.selectbox('Anemia', ('All', 'SI', 'NO'), key='select_anemia')
    select, button = st.columns([8, 2])
    with select:
        country = st.multiselect('Country', list(data['Country'].unique()), list(data['Country'].unique()), key='select_country')
    with button:
        st.write('')
        st.write('')
        st.button('Check all', on_click=check_country, key='check_country')
    select, button = st.columns([8, 2])
    with select:
        hospital = st.multiselect('Hospital', list(data['Hospital'].unique()), list(data['Hospital'].unique()), key='select_hospital')
    with button:
        st.write('')
        st.write('')
        st.button('Check all', on_click=check_hospital, key='check_hospital')
    select, button = st.columns([8, 2])
    with select:
        age_range = st.multiselect('Age_range', list(data['Age_range'].unique()), list(data['Age_range'].unique()), key='select_age_range')
    with button:
        st.write('')
        st.write('')
        st.button('Check all', on_click=check_age_range, key='check_age_range')
    select, button = st.columns([8, 2])
    with select:
        myeloma = st.multiselect('TypeMyeloma', list(data['TypeMyeloma'].unique()), list(data['TypeMyeloma'].unique()), key='select_myeloma')
    with button:
        st.write('')
        st.write('')
        st.button('Check all', on_click=check_myeloma, key='check_myeloma')
    select, button = st.columns([8, 2])
    with select:
        ttomm1 = st.multiselect('TtoMM1', list(data['TtoMM1'].unique()), list(data['TtoMM1'].unique()), key='select_ttomm1')
    with button:
        st.write('')
        st.write('')
        st.button('Check all', on_click=check_ttomm1, key='check_ttomm1')
    select, button = st.columns([8, 2])
    with select:
        ttomm2 = st.multiselect('TtoMM2', list(data['TtoMM2'].unique()), list(data['TtoMM2'].unique()), key='select_ttomm2')
    with button:
        st.write('')
        st.write('')
        st.button('Check all', on_click=check_ttomm2, key='check_ttomm2')
    selected_data = data.copy()
    if not sex == 'All':
        selected_data = selected_data[(selected_data['Genero'] == sex)]
    if not anemia == 'All':
         selected_data = selected_data[(selected_data['Anemia'] == anemia)]
    selected_data = selected_data[(selected_data['TypeMyeloma'].isin(myeloma)) &
                                  (selected_data['Country'].isin(country)) &
                                  (selected_data['Hospital'].isin(hospital)) &
                                  (selected_data['Age_range'].isin(age_range)) &
                                  (selected_data['TtoMM1'].isin(ttomm1)) &
                                  (selected_data['TtoMM2'].isin(ttomm2))]
    n = len(selected_data)
    filters_text.write(f'Applied filters have selected {n} patients.')
    st.button('Reset filters', on_click=reset_filters)

st.title('iDecide')

with st.expander('See raw data'):
    st.write(data)

tab_stats, tab_survival, tab_comparison, tab_tests, tab_cox, tab_economic, tab_miss = st.tabs(['Descriptive Statistics', 'Survival Functions',
                                                                                                'Groups Comparison', 'Tests Comparisons', 'Survival Regression (Cox)',
                                                                                                'Economic Analysis', 'Missing Data'])

with tab_stats:
    if n > 0:
        chosen_feature = st.selectbox('Variable for which to display descriptive statistics', selected_data.columns)

        description = selected_data[chosen_feature].describe()

        st.write(description)

        if 'mean' in description.keys():
            # Histogram of continuous feature
            range = description['max'] - description['min']
            fig = px.histogram(x=selected_data[chosen_feature], range_x=(description['min'],description['max']+.05*range))
            fig.update_traces(xbins=dict(start=description['min'], end=description['max']+.05*range, size=.05*range))
            fig.update_layout(
                xaxis_title_text=chosen_feature,
                yaxis_title_text='Count'
            )
            st.subheader(f'{chosen_feature} Graphical Representation')
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
            fig = px.bar(x=x, y=y)
            fig.update_layout(
                xaxis_title_text='Type',
                yaxis_title_text='Count'
            )
            st.subheader(f'{chosen_feature} Graphical Representation')
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
                                    line_color='rgba(0,0,0,0)', name='Confidence Interval', fill='tonexty', fillcolor='rgba(0, 0, 255, 0.2)')])
        fig.add_traces(go.Scatter(x=x, y=y, line=dict(shape='hv', width=2.5), mode='lines', line_color='rgba(0, 0, 255, 1)', name='KM estimate'))
        fig.update_layout(
            xaxis_title_text='Dias de Exposicion',
            yaxis_title_text='Probabilidad de no desmejorar en la enfermedad'
        )
        st.subheader('Survival Function of Patients')
        st.write('Estimation of Probability of Death using Kaplan-Meier')
        # st.write(f'The median time is: {kmf.median_survival_time_}')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader('Kaplan-Meier estimated survival for each of the following days:')
        days = [0,5,11,100,200]
        for i, day in enumerate(days):
            st.write(f'Estimate for {day} days: {kmf.predict(day) * 100: .02f}%')

        nb_days = st.number_input('Enter a number of days', min_value=0, value=100, step=1, format='%d')
        st.write(f'Estimate for {nb_days} days: {kmf.predict(nb_days) * 100: .02f}%')

        st.subheader('Kaplan-Meier Event Table')
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
                                    line_color='rgba(0,0,0,0)', name='Confidence Interval', fill='tonexty', fillcolor='rgba(0, 0, 255, 0.2)')])
        fig.add_traces(go.Scatter(x=x, y=y, line=dict(shape='hv', width=2.5), mode='lines', line_color='rgba(0, 0, 255, 1)', name='NA estimate'))
        fig.update_layout(
            xaxis_title_text='Time',
            yaxis_title_text='Hazard'
        )
        st.subheader('Estimation of cumulative hazard rates using Nelson-Aalen')
        st.write('The Nelson–Aalen estimator is a non-parametric estimator of the cumulative hazard rate function')
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
                                    line_color='rgba(0,0,0,0)', name='Confidence Interval', fill='tonexty', fillcolor='rgba(0, 0, 255, 0.2)')])
        fig.add_traces(go.Scatter(x=x, y=y, line=dict(shape='hv', width=2.5), mode='lines', line_color='rgba(0, 0, 255, 1)', name='Weibull estimate'))
        fig.update_layout(
            xaxis_title_text='Time',
            yaxis_title_text='Hazard'
        )
        st.subheader('Estimation of cumulative hazard rates using the Weibull model')
        st.write('The Weibull model for survival data is a parametric model, it has a functional form with parameters that we are fitting the data to')
        st.plotly_chart(fig, use_container_width=True)

        
with tab_comparison:
    # Select only categorical and handled numerical variables
    selected_cols = ['Genero', 'Regimenafiliacion', 'Anemia', 'Hipercalcemia', 'ERC_Leve', 'ERC_moderada', 'ERC_severa', 'ERC_dialisis',
                     'Lesiones_oseas', 'Infecciones_recurrentes', 'Fragilidad', 'FISHdel17p1', 'FISHt_1114', 'FISHt414', 'FISHamp1q211', 'FISHother',
                     'SubclasificacionplataformaMM', 'ISSPlataforma1', 'CoadOseo1', 'RespuestaClinica', 'Country', 'Hospital', 'TypeMyeloma',
                     'Age_range', 'Evento', 'TtoMM1', 'TtoMM2']

    surv_comparison_feature = st.selectbox('Variable to use for survival comparison', selected_cols)
    colors = [
        (255,   0,   0),
        (  0, 255,   0),
        (  0,   0, 255),
        (255, 128,   0),
        (  0, 255, 128),
        (128,   0, 255),
        (128, 255,   0),
        (  0, 128, 255),
        (255,   0, 128),
        (255, 255,   0),
        (  0, 255, 255),
        (255,   0, 255),
        (128, 128, 128),
    ]

    if st.checkbox('Show confidence interval'):
        conf = True
    else:
        conf = False
    
    if st.checkbox('Display curves on a grid'):
        grid = True
    else:
        grid = False

    cat_values = data[surv_comparison_feature].dropna().unique()
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
        flag = (data[surv_comparison_feature] == cat_val)
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
    st.subheader('Kaplan Meier Survival Estimation')
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
        flag = (data[surv_comparison_feature] == cat_val)
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
            xaxis_title_text='Time',
            yaxis_title_text='Hazard'
        )
    # else:
    #     fig.update_layout(title_text='Nelson Aalen Cumulative hazard')
    st.subheader('Nelson Aalen Cumulative hazard')
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
        flag = (data[surv_comparison_feature] == cat_val)
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
            xaxis_title_text='Time',
            yaxis_title_text='Hazard'
        )
    # else:
        # fig.update_layout(title_text='Weibull Cumulative hazard')
    st.subheader('Weibull Cumulative hazard')
    st.plotly_chart(fig, use_container_width=True)

with tab_tests:
    selected_cols = ['Genero', 'Regimenafiliacion', 'Anemia', 'Hipercalcemia', 'ERC_Leve', 'ERC_moderada', 'ERC_severa', 'ERC_dialisis',
                     'Lesiones_oseas', 'Infecciones_recurrentes', 'Fragilidad', 'FISHdel17p1', 'FISHt_1114', 'FISHt414', 'FISHamp1q211', 'FISHother',
                     'SubclasificacionplataformaMM', 'ISSPlataforma1', 'CoadOseo1', 'RespuestaClinica', 'Age_range', 'Country', 'Hospital', 'TypeMyeloma',
                     'Evento', 'TtoMM1', 'TtoMM2']

    tests_col = st.selectbox('Variable on which to run logrank tests', selected_cols)
    test_cat_values = data[tests_col].dropna().unique()

    if len(data[tests_col].dropna().unique()) == 2:
        flag = (data[tests_col] == test_cat_values[0])
        results = logrank_test(data[flag]['Time'], data[~flag]['Time'], data[flag]['Dead'], data[~flag]['Dead'], alpha=.99)
    else:
        df = pd.DataFrame({
            'durations': data['Time'], # Time 
            'groups': data[tests_col], # Modalities of variable could be strings too
            'events': data['Dead'], # Event
        })
        results = multivariate_logrank_test(df['durations'], df['groups'], df['events'])
    st.subheader('Statistical test of comparison of the survival functions')
    st.write('Compare the difference between two or more survival functions')
    st.write('The Mantel-Haenszel test called log-rank test is the most used, and the most performant. Another test can be used: the Wilcoxon test.')
    st.write('Null hypothesis H0: There is no difference in survival between the study groups')
    st.write(results)
    
    kmf = KaplanMeierFitter()
    fig = go.Figure()
    ## Iterate over all categorical values and plot one survival curve for each
    for i, cat_val in enumerate(test_cat_values):
        c = colors[i % len(colors)]
        flag = (data[tests_col] == cat_val)
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
    st.subheader('Kaplan Meier Survival Estimation')
    st.plotly_chart(fig, use_container_width=True)

with tab_cox:
    cox_variables = st.multiselect('Select covariates', raw_data.columns, ['Anemia', 'Hipercalcemia', 'Country', 'Age'])
    if cox_variables:
        cph = CoxPHFitter()
        cph.fit(raw_data, duration_col='Time', event_col='Evento', formula=' + '.join(cox_variables))
        st.subheader('Cox model parameters:')
        st.write(cph.params_)
        st.subheader('p-Values:')
        p_values = cph.summary.p
        tmp_df = pd.DataFrame(p_values)
        tmp_df['Significance'] = np.where(tmp_df['p']<.05, 'Significant impact on survival', 'No significant impact on survival')
        st.write(tmp_df)
        st.subheader('Hazard ratios:')
        ratios = cph.hazard_ratios_
        st.write(ratios)
        st.write(f'The variable {list(ratios.nlargest(1).index)[0]} has the greatest impact on death')
        st.subheader('Detailed Results:')
        st.write(cph.summary)

with tab_economic:
    treatment = st.selectbox('Select a TtoMM1 treatment', data['TtoMM1'].unique())
    treatment_data = data.copy()
    treatment_data = treatment_data[(treatment_data['TtoMM1'] == treatment)]
    remission_prob = treatment_data['Remission'].sum() / len(treatment_data)
    st.subheader(f'Cost Effectiveness: {treatment_data["Cost"].mean() / remission_prob:.02f}$')
    st.subheader(f'Burden of Desease: {treatment_data["Cost"].sum():.02f}$')
    country = st.selectbox('Select a country', data['Country'].unique())
    country_data = data.copy()
    country_data = country_data[(country_data['Country'] == country)]
    hospital = st.selectbox('Select a hospital', country_data['Hospital'].unique())
    country_data = country_data[(country_data['Hospital'] == hospital)]
    country_data = country_data[(country_data['TtoMM1'] == treatment)]
    st.subheader(f'Budget Impact Analysis for treatment in selected country and hospital: {0 if len(country_data) == 0 else country_data["Cost"].sum():.02f}$')

with tab_miss:
    st.subheader('Select columns to impute')

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