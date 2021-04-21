# Historico-Blue-CCL
## Cómo funciona:

+ Un primer script (dolar blue parser.py) scrapea la página web www.cotizacion-dolar.com.ar y guarda en un Excel históricos diarios del dólar Blue (las dos puntas, compra y venta) para un determinado año.

+ Hay 2 scripts (dolar blue MSFT.py y dolar blue AL30.py) que grafican el dólar blue comparado al dólar CCL de MSFT y el bono argenitna AL30. Estos graficos se muestran a través de una webapp sencilla.

+ Otro script agrega los datos scrapeados del primer Excel a otro Excel, este último Excel se va a utiizar como dataset para reealizar los gráficos. Es decir, se crean varios archivos Excel. Se crea un archivo Excel por cada año de información de dólar blue que se solicitó. Y también habrá un Excel con los datos de todos los años concatenados.

![](blue%20AL30.png)
![](blue%20msft.png)
![](Foto%20actualizador.png)


