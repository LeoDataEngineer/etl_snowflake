from time import time
from fastapi import FastAPI, HTTPException, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pandas as pd
import subprocess
# Se crea una instancia de la aplicación FastAPI
app = FastAPI()
pronostico = pd.read_csv('data_snow/data_snow.csv')

# HTML que se enviará como respuesta en la ruta "/"
html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI</title>
        <link rel="icon" href="/static/Subte-logo.svg" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <!-- Agregar la imagen Subte-logo.svg desde la carpeta /static -->
            <img src="/static/Subte_logo.jpg" alt="Logo del Subte" style="max-width: 200px;">
            
            <h1>Hello, Bienvenidos a la API:</h1>
            <p>Pronóstico de demora en las llegadas y salidas de trenes del SUBTE de la ciudad de Buenos Aires.</p>
            <p>FastAPI@{__version__}</p>
            <p>Link para ver la API: <a href="/docs">/docs</a></p>
            <p>Realizado por Leo</p>
        </div>
    </body>
</html>
"""

# Definición de la ruta principal "/"    
@app.get("/")
async def root():
    return HTMLResponse(html)


# Definición de la ruta "/get_pronostico ", que permite obtener todos los datos de la tabla pronósticos guardados en la BD.
@app.get('/get_pronostico', 
         summary="Obtiene la informacion", 
         description="""Pronostico:  retorna toda la tabla  del pronostico en un json."""
        )
  
def obtener_pronostico_data_subte():
    df = pronostico
    
    return df


# Definición de la ruta "/get_pronostico/{linea}/{direccion}/{estacion}"
@app.get('/get_pronostico/{linea}/{direccion}/{estacion}', 
         summary="Obtiene la informacion de la demora  en una estación", 
         description="""Pronostico de la demora en llegada y salida de los trenes del subte de la Ciudad de Buienos aires.
         
         Ejemplo: linea_de_subte: LineaA, direccion_a (hacia donde): Plaza de Mayo, estación: San Pedrito"""
        )
  
def obtener_pronostico_delay_subte(linea_de_subte : str, direccion_a: str, estacion: str):
     df_pronostico = pronostico
    
    # Filtrar datos según los parámetros de la solicitud
    resultado_loc = df_pronostico.loc[(df_pronostico['Route_Id'] == linea_de_subte) & 
                                      (df_pronostico['Direction_to'] == direccion_a) & 
                                      (df_pronostico['stop_name'] == estacion), 
                                     ['arrival_delay', 'departure_delay']]
    
    
    return resultado_loc
