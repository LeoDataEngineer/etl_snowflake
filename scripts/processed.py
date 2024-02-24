import requests
import pandas as pd

def procesar_data():
        df = pd.read_csv('subte_data_raw.csv')
        df['Direction_to'] = df['Direction_ID'].map({1: 'Inbound', 0: 'Outbound'})
        df['Direction_to'] = df.groupby('id_linea')['stop_name'].transform('last')
        new_order_columns = ['id_linea', 'Route_Id', 'Direction_ID', 'Direction_to', 'start_date', 'stop_name', 'arrival_time', 'arrival_delay', 'departure_time', 'departure_delay']
        df = df[new_order_columns]

        df['start_date'] = pd.to_datetime(df['start_date'], format='%Y%m%d')
        df['arrival_time'] = pd.to_datetime(df['arrival_time'], unit='s')
        df['departure_time'] = pd.to_datetime(df['departure_time'], unit='s')

        df['arrival_delay'] = df['arrival_delay'] / 60
        df['departure_delay'] = df['departure_delay'] / 60

        df.to_csv('subte_data_processed.csv', index=False)
        print("Datos extraídos y guardados en 'subte_data.csv'.")
    

procesar_data()
