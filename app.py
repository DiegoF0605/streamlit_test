import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables de estado

if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iteraciones', 'media']
    )

st.header('Lanzar una moneda (un saludo a la gordita :D)')

# Placeholder para el gráfico
chart_placeholder = st.empty()

def toss_coin(n):

    trial_outcomes = scipy.stats.bernoulli.rvs(
        p=0.5,
        size=n
    )

    outcome_no = 0
    outcome_1_count = 0

    means = [0.5]

    chart_placeholder.line_chart(means)

    for r in trial_outcomes:

        outcome_no += 1

        if r == 1:
            outcome_1_count += 1

        mean = outcome_1_count / outcome_no

        means.append(mean)

        chart_placeholder.line_chart(means)

        time.sleep(0.05)

    return mean

number_of_trials = st.slider(
    '¿Número de intentos?',
    min_value=1,
    max_value=1000,
    value=10
)

start_button = st.button('Ejecutar')

if start_button:

    st.write(
        f'Experimento con {number_of_trials} intentos en curso.'
    )

    st.session_state['experiment_no'] += 1

    mean = toss_coin(number_of_trials)

    new_row = pd.DataFrame(
        [[
            st.session_state['experiment_no'],
            number_of_trials,
            mean
        ]],
        columns=['no', 'iteraciones', 'media']
    )

    st.session_state['df_experiment_results'] = pd.concat(
        [
            st.session_state['df_experiment_results'],
            new_row
        ],
        ignore_index=True
    )

st.dataframe(
    st.session_state['df_experiment_results']
)
