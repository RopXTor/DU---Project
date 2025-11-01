import os
import tomli
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


def get_config(config_file="config.toml"):
    full_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(full_path, mode="rb") as f:
        return tomli.load(f)


def get_data(ticker, begin_date, end_date):
    """ Télécharge le cours ajusté pour un ticker et une periode donnés.

    Args:
        ticker (str): Le ticker de l'action.
        begin_date (datetime): La date de début de la période.
        end_date (datetime): La date de fin de la période.

    Returns:
        DataFrame: Un DataFrame contenant les données historiques de l'action.
    """
    return yf.download(ticker, begin_date, end_date, auto_adjust=False)


def index(Fund_Stocks, end_date, config):
    """Récupère les données financières de l'indice et calcule sa performance.

    Args:
        Fund_Stocks (str): Le fonds sélectionné par l'utilisateur.
        end_date (datetime): La date de fin à utiliser pour récupérer les données.
        config : Fichier de config sous format toml.

    Returns:
        data_index (DataFrame): DataFrame des données de l'indice ajustées et normalisées.
        ticker_index (list): Liste des tickers des indices.
        name_index (list): Liste des noms des indices.
        perf_index (list): Liste des performances des indices.
    """
    ticker_index= config["Ticker_StockMarkets_Config"]["StockMarkets"]
    begin_date = config[Fund_Stocks]["begin_date"]

    data_index = pd.DataFrame(get_data(ticker_index, begin_date, end_date)["Adj Close"],  columns=ticker_index).fillna(method="ffill").fillna(method='bfill')
    
    name_index, perf_index = [], []
    for keys_index,values_index in data_index.items():
        name_columns = yf.Ticker(keys_index).info["longName"].replace(".", "  ").split("  ")[0]
        data_index[f"{name_columns}"] = values_index / values_index.iloc[0] * 100
        name_index.append(name_columns)
        perf_index.append(round(data_index.iloc[-1,-1]-100,2))
    return data_index, ticker_index, name_index, perf_index


def index_plot(Fund_Stocks, end_date, config):
    """Génère un graphique des performances des indices boursiers en base 100.

    Args:
        Fund_Stocks (str): Le fonds sélectionné par l'utilisateur.
        end_date (datetime): La date de fin à utiliser pour récupérer les données.
        config : Fichier de config sous format toml.

    Returns:
        fig : Un objet matplotlib Figure contenant le graphique.
        ax : Un objet matplotlib Axes contenant les axes du graphique.
    """
    data_index = index(Fund_Stocks, end_date, config)[0]
    ticker_index = index(Fund_Stocks, end_date, config)[1]
    
    fig, ax = plt.subplots()
    ax.plot(data_index.iloc[:, -(len(ticker_index)):])
    
    ax.set(xlabel=config["Config_Graph_EU"]["x_label"], ylabel=config["Config_Graph_EU"]["y_label"],
           title=config["Config_Graph_EU"]["Title"])
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    ax.legend(data_index.iloc[:, -(len(ticker_index)):])
    return fig, ax


def fund(Fund_Stocks, end_date,config):
    """Calcule l'évolution d'un fonds en base 100 à partir de ses composants, en fonction de leur poids.

    Args:
        Fund_Stocks (str): Le fonds sélectionné par l'utilisateur.
        end_date (datetime): La date de fin à utiliser pour récupérer les données.
        config : Fichier de config sous format toml.

    Returns:
        DataFrame: Un DataFrame contenant les prix ajustés des actions,
                   leurs performances pondérées en base 100,
                   et l'évolution globale du fonds ("Base100_Fund").
    """
    begin_date = config[Fund_Stocks]["begin_date"]
    stocks = config[Fund_Stocks]["stock"]
    weights = config[Fund_Stocks]["weight"]

    data_fund = pd.DataFrame(get_data(stocks, begin_date, end_date)["Adj Close"], columns=stocks).fillna(method='ffill')
   
    i_count = 0    
    for keys_stocks,values_stocks in data_fund.items():
        data_fund[f"Base100_{keys_stocks}"] = values_stocks / values_stocks.iloc[0] * weights[i_count] * 100
        i_count += 1
    data_fund["Base100_Fund"] = (data_fund.iloc[:, -(i_count):]).sum(axis=1)
    return data_fund
    

def bench(Fund_Stocks, end_date, config):
    """Calcule la performance de l'indice de référence (benchmark) en base 100.

    Args:
        Fund_Stocks (str): Le fonds sélectionné par l'utilisateur.
        end_date (datetime): La date de fin à utiliser pour récupérer les données.
        config : Fichier de config sous format toml.

    Returns:
        DataFrame: Un DataFrame contenant les données de clôture ajustées du benchmark et la base 100.
    """
    benchmark = config[Fund_Stocks]["benchmark"]
    bench = pd.DataFrame(get_data(benchmark, config[Fund_Stocks]["begin_date"], end_date)["Adj Close"]).fillna(method='ffill')
    bench["Base100"] = (bench / bench.iloc[0]) * 100
    return bench
        
    
def plot_perf_fundvsbench(Fund_Stocks, end_date, config):
    """Génère un graphique, en base 100, comparant la performance du fonds à celle de son benchmark.

    Args:
        Fund_Stocks (str): Le fonds sélectionné par l'utilisateur.
        end_date (datetime): La date de fin à utiliser pour récupérer les données.
        config : Fichier de config sous format toml.

    Returns:
        fig : Un objet matplotlib Figure contenant le graphique.
        ax : Un objet matplotlib Axes contenant les axes du graphique.
    """
    title_plot = config["Config__Graph_Fund"]["Title_Plot"]
    
    fig, ax = plt.subplots()
    
    ax.plot(fund(Fund_Stocks, end_date, config)["Base100_Fund"],color = config[Fund_Stocks]["Color_fund"],
            label = config[Fund_Stocks]["Name_Fund"])
    ax.plot(bench(Fund_Stocks, end_date, config)["Base100"], color = config[Fund_Stocks]["Color_bench"],
            label = config[Fund_Stocks]["Name_Bench"])
    ax.set(xlabel=config["Config__Graph_Fund"]["x_label"], ylabel=config["Config__Graph_Fund"]["y_label"],
       title= f"{Fund_Stocks}{title_plot}")
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    
    ax.legend()
    return fig, ax


def ratio_fund(Fund_Stocks, end_date, config):
    """Calcule les principaux ratios financiers d’un fonds.

    Args:
        Fund_Stocks (str): Le fonds sélectionné par l'utilisateur.
        end_date (datetime): La date de fin à utiliser pour récupérer les données.
        config : Fichier de config sous format toml.

    Returns:
        sharpe_ratio (float) : Rendement ajusté du risque, arrondis à 4 décimales.
        volatility (float) : Volatilité annuelle en pourcentage, arrondis à 4 décimales.
        beta (float) : Sensibilité du fonds par rapport à son benchmark, arrondis à 4 décimales.
        correlation (float) : Corrélation entre le fonds et son benchmark, arrondis à 4 décimales.
        var_95 (float) : Value at Risk à 95% en pourcentage, arrondis à 4 décimales.
    """
    trading_days = config["parameters_trading"]["trading_days"]
    risk_free_rate = config["risk_free"]["rf_EU"]
    
    return_ptf = fund(Fund_Stocks, end_date, config)["Base100_Fund"].pct_change().fillna(0)
    return_bench = bench(Fund_Stocks, end_date, config)["Base100"].pct_change().fillna(0)

    mean_return = np.mean(return_ptf) * trading_days
    std_return = np.std(return_ptf) * np.sqrt(trading_days)
        
    sharpe_ratio = (mean_return - risk_free_rate) / std_return
    volatility = std_return * 100
    beta = return_ptf.cov(return_bench) / np.var(return_bench)
    correlation = return_bench.corr(return_ptf)
    var_95 = np.percentile(return_ptf, 5) * 100
    return (
    round(sharpe_ratio, 2),
    round(volatility, 2),
    round(beta, 2),
    round(correlation, 2),
    round(var_95, 2))


def caracteristic_fund(Fund_Stocks, config):
    """Construit un tableau contenant les caractéristiques principales d’un fonds.

    Args:
        Fund_Stocks (str): Le fonds sélectionné par l'utilisateur.
        config : Fichier de config sous format toml.

    Returns:
        DataFrame: Un tableau contenant les caractéristiques clés du fonds.
    """
    df_caract = pd.DataFrame({
        f"Caractéristiques - {Fund_Stocks}": [
            config[Fund_Stocks]["begin_date"],
            config[Fund_Stocks]["Isin"],
            config[Fund_Stocks]["Fees"],
            config[Fund_Stocks]["Juridique"],
            config[Fund_Stocks]["BBG"],
            config[Fund_Stocks]["Valo"],
            config[Fund_Stocks]["Devise"],
            config[Fund_Stocks]["Centralisation"],
            config["Config_Streamlit"]["Disclaimer"]
        ]},
        index=[
            "Inception Date",
            "ISIN Code",
            "Fees",
            "Forme juridique",
            "Bloomberg Code",
            "Valorisateur",
            "Devise de cotation",
            "Centralisation des ordres",
            "Avertissement"
        ])
    
    return df_caract
