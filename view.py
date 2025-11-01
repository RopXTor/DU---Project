import streamlit as st
import datetime as dt
import repository


def get_inputs(config):
    """Récupère le fonds choisi par l'utilisateur via Streamlit.

    Args:
        config : Fichier de config sous format toml.

    Returns:
        Le fonds sélectionné (str) et la date de fin (datetime).
    """
    Fund_Stocks = st.selectbox("Selectionner un fonds", config["ALL_Fund"].values())
    end_date = dt.datetime.now() - dt.timedelta(days=1)
    return Fund_Stocks, end_date


def display_info(config):
    """Affiche, à l'utilisateur, le titre et le message d'avertissement.

    Args:
        config : Fichier de config sous format toml.
    """
    st.title(config["Config_Streamlit"]["Title_Page"])
    warning_streamlit = config["Config_Streamlit"]["Reglementation"]
    st.write(f"**:red[{warning_streamlit}]**")


def display_plot_index(Fund_Stocks, end_date, config):
    """Affiche le graphique des principaux indices européen en base 100 et en fonction
    de la date de création du fonds sélectionné. Elle affiche également les performances des indices.

    Args:
        Fund_Stocks (str): Le fonds sélectionné par l'utilisateur.
        end_date (datetime): La date de fin à utiliser pour récupérer les données.
        config : Fichier de config sous format toml.
    """
    
    st.subheader(config["Config_Graph_EU"]["Title"])
    fig, ax = repository.index_plot(Fund_Stocks, end_date, config)
    st.pyplot(fig)
    
    name_index = repository.index(Fund_Stocks, end_date, config)[2]
    perf_index = repository.index(Fund_Stocks, end_date, config)[3]
    
    st.write(f"**Depuis la date de création de {Fund_Stocks} :**")
    st.write(f"La performance de l'indice : **{name_index[0]}** est de **{perf_index[0]}%**.")
    st.write(f"La performance de l'indice : **{name_index[1]}** est de **{perf_index[1]}%**.")
    st.write(f"La performance de l'indice : **{name_index[2]}** est de **{perf_index[2]}%**.")
    st.write(f"La performance de l'indice : **{name_index[3]}** est de **{perf_index[3]}%**.")
    
def display_info_fund(Fund_Stocks, config):
    """Affiche un tableau des caractéristiques du fonds sélectionné.

   Args:
       Fund_Stocks (str): Le fonds sélectionné par l'utilisateur.
       config : Fichier de config sous format toml.

   """
    st.subheader("Caractéristique du fonds")
    st.table(repository.caracteristic_fund(Fund_Stocks, config))  
    
    
def display_plot(Fund_Stocks, end_date, config):
    """Génère un graphique comparant la performance du fonds et de son indice de référence, puis la performance du fonds.

    Args:
        Fund_Stocks (str): Le fonds sélectionné par l'utilisateur.
        end_date (datetime): La date de fin à utiliser pour récupérer les données.
        config : Fichier de config sous format toml.
    """
    st.subheader(config["Config__Graph_Fund"]["Title_Page"])
    fig, ax = repository.plot_perf_fundvsbench(Fund_Stocks, end_date, config)
    st.pyplot(fig)
    
    fund = repository.fund(Fund_Stocks, end_date, config)
    bench = repository.bench(Fund_Stocks, end_date, config)
    
    perf_fund = round(fund.iloc[-1, -1] - 100,2)
    perf_bench = round(bench.iloc[-1,-1]-100,2)
    
    if perf_fund > perf_bench:
        st.write(f"La performance du fonds est de **:green[{perf_fund}%]**.")
        st.write(f"La performance du fonds est de **:red[{perf_bench}%]**.")
    elif perf_fund == perf_bench:
        st.write(f"La performance du fonds est de **{perf_fund}%**.")
        st.write(f"La performance du fonds est de {perf_bench}%.")
    else:
        st.write(f"La performance du fonds est de **:red[{perf_fund}%]**.")
        st.write(f"La performance du fonds est de **:green[{perf_bench}%]**.")
    
    disclamer = config["Config_Streamlit"]["Warning"]
    st.write(f"**:red[{disclamer}]**")


def display_stat(Fund_Stocks, end_date, config):
    """Affiche les statistiques financières du fonds.

    Args:
        Fund_Stocks (str): Le fonds sélectionné par l'utilisateur.
        end_date (datetime): La date de fin à utiliser pour récupérer les données.
        config : Fichier de config sous format toml.
    """
    st.subheader(config["Config_Streamlit"]["Title_Stat"])
    stat = repository.ratio_fund(Fund_Stocks, end_date, config)
    st.write(f"Le Sharpe Ratio du fonds est = {stat[0]}")
    st.write(f"La volatilité du fonds est = {stat[1]}")
    st.write(f"Le Beta du fonds est = {stat[2]}")
    st.write(f"La correlation est = {stat[3]}")
    st.write(f"La VaR(95) est = {stat[4]}%")
    