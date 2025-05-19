"""
Módulo para cargar datos universitarios desde archivos CSV.
"""
import os
import pandas as pd
from typing import Optional


def load_university_data(csv_file_path: str) -> pd.DataFrame:
    """
    Carga datos universitarios desde un archivo CSV.
    
    Args:
        csv_file_path (str): Ruta al archivo CSV de datos universitarios.
        
    Returns:
        pd.DataFrame: DataFrame con los datos universitarios cargados.
        
    Raises:
        FileNotFoundError: Si el archivo especificado no existe.
    """
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"El archivo {csv_file_path} no existe.")
    
    # Cargar el CSV con las opciones adecuadas
    df = pd.read_csv(
        csv_file_path,
        delimiter=',',
        quotechar='"',  # Especificar que los campos están entre comillas dobles
        dtype={
            'student_id': str,
            'first_name': str,
            'last_name': str,
            'type_id_number': str,
            'identification_number': str,
            'email': str,
            'address': str,
            'gender': str,
            'nationality': str,
            'country_code': str,
            'phone_number': str,
            'program': str,
            'state_program': str,
            'current_semester': int,
            'Number_of_credits_approved': int,
            'credits_remaining': int,
            'GPA': float,
            'student_status': str,
            'advisor_id': str,
            'advisor_name': str,
            'scholarship': bool,
            'payment_status': str,
            'academic_standing': str,
            'course_load': int,
            'marital_status': str,
            'library_books_borrowed': int
        },
        parse_dates=['date_of_birth', 'enrollment_date']
    )
    
    return df


if __name__ == "__main__":
    # Este bloque solo se ejecuta si este script es ejecutado directamente
    # Es útil para pruebas rápidas
    try:
        data_path = os.path.join('data', 'university_data.csv')
        df = load_university_data(data_path)
        print(f"Datos cargados exitosamente. Shape: {df.shape}")
        print(df.dtypes)
        print(df.head())
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
