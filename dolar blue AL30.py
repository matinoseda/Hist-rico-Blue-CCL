import pandas as pd
import datetime as dt
import json
from pymatriz.enums import MarketDataEntry, Market
from pymatriz.client import MatrizAPIClient
import plotly.express as px
import plotly.graph_objects as go

with open("c.json") as json_file:
    archivo = json.load(json_file)
username = archivo["pymatriz"]["usuario"]
password = archivo["pymatriz"]["contraseña"]

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
client = MatrizAPIClient(username=username, password=password)
client.connect()

AL30 = client.get_daily_history(["AL30"], terms=[MarketDataEntry.TERM_24HS, MarketDataEntry.TERM_48HS])
AL30D = client.get_daily_history(["AL30D"], terms=[MarketDataEntry.TERM_24HS, MarketDataEntry.TERM_48HS])
AL30C = client.get_daily_history(["AL30C"], terms=[MarketDataEntry.TERM_24HS, MarketDataEntry.TERM_48HS])
for df_ARG in [AL30,AL30D,AL30C]:
    df_ARG.reset_index(inplace=True)
    df_ARG.drop_duplicates(subset="time", keep="last", inplace=True)
    df_ARG["time"] = pd.to_datetime(df_ARG.time, utc=False)
    df_ARG["time"] = df_ARG["time"].dt.date # esto es clave, no borrar
    df_ARG.set_index(df_ARG.time, inplace=True)
    df_ARG.sort_index()
    print(df_ARG.head())
    #print(df_ARG.info())

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

df = pd.DataFrame()
df["blue"] = df_blue.bid
df["AL30"] = AL30.close
df["AL30D"] = AL30D.close
df["AL30C"] = AL30C.close
df["MEP"] = df["AL30"]/df["AL30D"]
df["CCL"] = df["AL30"]/df["AL30C"]
df.dropna(inplace=True)
df["ratio BLUE/CCL"] = df.blue/df["CCL"]
df["ratio BLUE/MEP"] = df.blue/df["MEP"]

print(df)
print(len(df))

# fig = px.line(df, x=df.index, y="ratio BLUE/CCL", title="Ratio USD BLUE/CCL del BONO AL30")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df["blue"],
                    mode='lines',
                    name='dólar blue'))
fig.add_trace(go.Scatter(x=df.index, y=df["MEP"],
                    mode='lines',
                    name='dólar MEP AL30'))
fig.add_trace(go.Scatter(x=df.index, y=df["CCL"],
                    mode='lines',
                    name='dólar CCL AL30'))
fig.update_xaxes(
    # rangeslider_visible=True,
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
