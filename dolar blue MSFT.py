import pandas as pd
import yfinance as yf
import datetime as dt
from pymatriz.enums import MarketDataEntry, Market
from pymatriz.client import MatrizAPIClient
import plotly.express as px
import json


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

df_blue = pd.read_excel("blue.xlsx")
df_blue.set_index("fecha", inplace=True)
df_blue.sort_index(inplace=True)
# print(df_blue.head())
# print(df_blue.info())
# print(df_blue.dtypes)
#--------------------------------------------------------------------------------------------------------
fecha_inicio = '2019-1-1'
fecha_fin = dt.datetime.today()

df_USA = yf.download('MSFT', start= fecha_inicio, end=fecha_fin)['Adj Close'].to_frame()
#
# print(df_USA.head())
# print(df_USA.info())
#--------------------------------------------------------------------------------------------------------
with open("c.json") as json_file:
    archivo = json.load(json_file)
username = archivo["pymatriz"]["usuario"]
password = archivo["pymatriz"]["contraseña"]

client = MatrizAPIClient(username=username, password=password)
client.connect()

df_ARG = client.get_daily_history(["MSFT"], terms=[MarketDataEntry.TERM_24HS, MarketDataEntry.TERM_48HS])
df_ARG.reset_index(inplace=True)
df_ARG.drop_duplicates(subset="time", keep="last", inplace=True)
df_ARG["time"] = pd.to_datetime(df_ARG.time, utc=False)
df_ARG["time"] = df_ARG["time"].dt.date      #esto es importante, no borrar
df_ARG.set_index(df_ARG.time, inplace=True)
df_ARG.sort_index()
print(df_ARG.head())
#print(df_ARG.info())

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def separador_ratios(indice):
    return indice/2
    # if dt.datetime(indice.values()) < dt.datetime(2020,9,20):
    #     return df["ARG"]/df["USA"]*5
    # else:
    #     return df["ARG"]/df["USA"]*10

df = pd.DataFrame()
df["blue"] = df_blue.bid
df["ARG"] = df_ARG.close
df["USA"] = df_USA["Adj Close"]
df.dropna(inplace=True)
df["ccl MSFT"] =df["ARG"]/df["USA"]*10
df.loc["2019-01-01":"2020-10-21",["ccl MSFT"]] = df.applymap(separador_ratios)
df["ratio"] = df.blue/df["ccl MSFT"]
print(df.head())
print(len(df))

fig = px.line(df, x=df.index, y="ratio")
fig.update_layout(xaxis_range=['2019-1-01','2021-03-31'],
                  title_text="Ratio USD BLUE/CCL de MSFT")
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=2, label="2y", step="year", stepmode="backward"),
            dict(step="all")])),
    rangebreaks=[
        dict(bounds=["sat", "mon"]),  # hide weekends
        dict(values=["2015-12-25", "2016-01-01"])  # hide Christmas and New Year's
        ])
fig.show()