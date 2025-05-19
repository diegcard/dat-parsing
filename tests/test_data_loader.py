"""
Pruebas unitarias para el módulo data_loader.
"""
import os
import pytest
import pandas as pd
import tempfile
from src.data_loader import load_university_data


@pytest.fixture
def sample_csv_path():
    """
    Fixture que crea un archivo CSV de muestra para pruebas.
    """
    # Crear un archivo temporal
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False, mode='w') as f:
        # Escribir datos de muestra
        f.write('"student_id","first_name","last_name","type_id_number","identification_number","date_of_birth","email","address","gender","nationality","country_code","phone_number","program","state_program","current_semester","Number_of_credits_approved","credits_remaining","GPA","enrollment_date","student_status","advisor_id","advisor_name","scholarship","payment_status","academic_standing","course_load","marital_status","library_books_borrowed"\n')
        f.write('"STU000001","Maria","Sutton","TI","2319391115","2008-01-20","maria.sutton@university.edu.co","0882 Bennett Mountains, Anthonystad, NV 47979","Female","Colombia","+57","3235187121","Biology","Enrolled","8","147","30","3.078070164006662","2021-11-08","Active","ADV0017","Emily Davis","False","Paid","Average","18","Single","1"\n')
        f.write('"STU000002","Carlos","Torres","CC","1012345678","2000-05-15","carlos.torres@university.edu.co","123 Main St, Cityville","Male","Colombia","+57","3001234567","Computer Science","Enrolled","5","85","92","4.2","2022-01-15","Active","ADV0020","John Smith","True","Paid","Excellent","20","Single","0"\n')
        
        # Obtener la ruta del archivo
        temp_path = f.name
    
    # Devolver la ruta y asegurarnos de que se elimine después
    yield temp_path
    os.unlink(temp_path)


def test_load_university_data_success(sample_csv_path):
    """Prueba que los datos se carguen correctamente."""
    df = load_university_data(sample_csv_path)
    
    # Verificar que el DataFrame tiene la forma correcta
    assert df.shape == (2, 28)
    
    # Verificar que los tipos de datos son correctos
    assert df['student_id'].dtype == 'object'  # str
    assert df['GPA'].dtype == 'float64'
    assert df['current_semester'].dtype == 'int64'
    assert df['Number_of_credits_approved'].dtype == 'int64'
    assert df['credits_remaining'].dtype == 'int64'
    
    # Verificar que las fechas fueron parseadas correctamente
    assert pd.api.types.is_datetime64_dtype(df['date_of_birth'])
    assert pd.api.types.is_datetime64_dtype(df['enrollment_date'])
    
    # Verificar algunos valores específicos
    assert df.loc[0, 'first_name'] == 'Maria'
    assert df.loc[1, 'GPA'] == 4.2
    assert df.loc[0, 'current_semester'] == 8


def test_load_university_data_file_not_found():
    """Prueba que se lance FileNotFoundError si el archivo no existe."""
    with pytest.raises(FileNotFoundError):
        load_university_data('archivo_inexistente.csv')


def test_load_university_data_date_parsing(sample_csv_path):
    """Prueba que las fechas se carguen correctamente como objetos datetime."""
    df = load_university_data(sample_csv_path)
    
    # Verificar que las columnas de fecha son objetos datetime
    assert pd.api.types.is_datetime64_dtype(df['date_of_birth'])
    assert pd.api.types.is_datetime64_dtype(df['enrollment_date'])
    
    # Verificar valores específicos de fechas
    assert df.loc[0, 'date_of_birth'].strftime('%Y-%m-%d') == '2008-01-20'
    assert df.loc[1, 'enrollment_date'].strftime('%Y-%m-%d') == '2022-01-15'


def test_load_university_data_numeric_parsing(sample_csv_path):
    """Prueba que las columnas numéricas se carguen correctamente."""
    df = load_university_data(sample_csv_path)
    
    # Verificar que las columnas numéricas tienen los tipos correctos
    assert df['current_semester'].dtype == 'int64'
    assert df['Number_of_credits_approved'].dtype == 'int64'
    assert df['credits_remaining'].dtype == 'int64'
    assert df['GPA'].dtype == 'float64'
    assert df['course_load'].dtype == 'int64'
    assert df['library_books_borrowed'].dtype == 'int64'
    
    # Verificar valores específicos
    assert df.loc[0, 'GPA'] == 3.078070164006662
    assert df.loc[1, 'Number_of_credits_approved'] == 85
