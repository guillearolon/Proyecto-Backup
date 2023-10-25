from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from tabla import procesar_archivo_json
from tareas import app, db
import os
import plotly.express as px
import pandas as pd
import json

#INICIO
@app.route('/')
def index():
    return render_template('comafi.html')

#TAGS
@app.route('/tags')
def mostrar_tabla():
    campos = procesar_archivo_json()
    return render_template('tabla.html', campos=campos)

@app.route('/grafico')
def mostrar_grafico():
    # Obtener la lista de archivos en la carpeta actual
    carpeta = '.'  # Puedes cambiar esto a la ruta de tu carpeta
    archivos_json = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.json')]

    # Elegir un archivo JSON (puedes personalizar esta lógica según tus necesidades)
    archivo_json = archivos_json[0]

    with open(archivo_json, 'r') as datos_json:
        datos = json.load(datos_json)

    # Crear un DataFrame de Pandas a partir de los datos
    data_frame = pd.DataFrame(datos["Report"])

    # Convierte la columna 'Status Veeam' en una columna categórica
    data_frame['Status Veeam'] = data_frame['Status Veeam'].astype(str)

    # Crear una columna 'Color' para asignar colores
    data_frame['Color'] = 'black'
    data_frame.loc[data_frame['Status Veeam'] == 'Success', 'Color'] = 'green'
    data_frame.loc[data_frame['Status Veeam'] == 'Failed', 'Color'] = 'red'
    data_frame.loc[data_frame['Status Veeam'] == 'Warning', 'Color'] = 'yellow'

    # Crear el histograma con Plotly Express
    titulo = f"Status Veeam {archivo_json}"
    fig = px.histogram(data_frame, x="Status Veeam", color='Color', color_discrete_map={'green': 'green', 'black': 'black', 'red': 'red', 'yellow': 'yellow'})

    # Convertir el gráfico Plotly en un fragmento HTML
    plotly_html = fig.to_html(full_html=False)

    # Renderizar la plantilla HTML y pasar el gráfico
    return render_template('grafico.html', titulo=titulo, plotly_html=plotly_html)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run('localhost', debug=True)