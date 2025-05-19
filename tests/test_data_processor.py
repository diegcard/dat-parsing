"""
Pruebas unitarias para el módulo data_processor.
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from src.data_processor import preprocess_data, validate_data


@pytest.fixture
def sample_dataframe():
    """
    Fixture que crea un DataFrame de muestra para pruebas.
    """
    # Definir fechas como objetos datetime
    date_of_birth1 = pd.to_datetime('2000-05-15')
    date_of_birth2 = pd.to_datetime('2002-11-30')
    enrollment_date1 = pd.to_datetime('2020-01-15')
    enrollment_date2 = pd.to_datetime('2021-08-20')
    
    # Crear DataFrame de muestra
    data = {
        'student_id': ['STU000001', 'STU000002'],
        'first_name': ['Maria', 'Carlos'],
        'last_name': ['Sutton', 'Torres'],
        'date_of_birth': [date_of_birth1, date_of_birth2],
        'gender': ['Female', 'Male'],
        'nationality': ['Colombia', 'Colombia'],
        'program': ['Biology', 'Computer Science'],
        'state_program': ['Enrolled', 'Enrolled'],
        'current_semester': [8, 5],
        'Number_of_credits_approved': [147, 85],
        'credits_remaining': [30, 92],
        'GPA': [3.07, 4.2],
        'enrollment_date': [enrollment_date1, enrollment_date2],
        'student_status': ['Active', 'Active'],
        'advisor_id': ['ADV0017', 'ADV0020'],
        'advisor_name': ['Emily Davis', 'John Smith'],
        'scholarship': [False, True],
        'payment_status': ['Paid', 'Paid'],
        'academic_standing': ['Average', 'Excellent'],
        'course_load': [18, 20],
        'marital_status': ['Single', 'Single'],
        'library_books_borrowed': [1, 0]
    }
    
    return pd.DataFrame(data)


@pytest.fixture
def dataframe_with_issues():
    """
    Fixture que crea un DataFrame con problemas para pruebas de validación.
    """
    # Definir fechas como objetos datetime
    date_of_birth1 = pd.to_datetime('2000-05-15')
    date_of_birth2 = pd.to_datetime('2050-11-30')  # Fecha en el futuro
    enrollment_date1 = pd.to_datetime('2020-01-15')
    enrollment_date2 = pd.to_datetime('2030-08-20')  # Fecha de matrícula en el futuro
    
    # Crear DataFrame con problemas
    data = {
        'student_id': ['STU000001', 'STU000002'],
        'first_name': ['Maria', 'Carlos'],
        'last_name': ['Sutton', 'Torres'],
        'date_of_birth': [date_of_birth1, date_of_birth2],
        'gender': ['Female', 'Male'],
        'nationality': ['Colombia', 'Colombia'],
        'program': ['Biology', 'Computer Science'],
        'state_program': ['Enrolled', 'Enrolled'],
        'current_semester': [8, -5],  # Semestre negativo
        'Number_of_credits_approved': [147, 85],
        'credits_remaining': [30, -10],  # Créditos restantes negativos
        'GPA': [3.07, 6.0],  # GPA fuera de rango
        'enrollment_date': [enrollment_date1, enrollment_date2],
        'student_status': ['Active', 'Active'],
        'advisor_id': ['ADV0017', 'ADV0020'],
        'advisor_name': ['Emily Davis', 'John Smith'],
        'scholarship': [False, True],
        'payment_status': ['Paid', 'Paid'],
        'academic_standing': ['Average', 'Excellent'],
        'course_load': [18, 20],
        'marital_status': ['Single', 'Single'],
        'library_books_borrowed': [1, 0]
    }
    
    return pd.DataFrame(data)


def test_preprocess_data(sample_dataframe):
    """Prueba que el preprocesamiento funcione correctamente."""
    processed_df = preprocess_data(sample_dataframe)
    
    # Verificar que el DataFrame no se modificó en tamaño (filas)
    assert len(processed_df) == len(sample_dataframe)
    
    # Verificar que se agregaron nuevas columnas
    assert 'age' in processed_df.columns
    assert 'years_enrolled' in processed_df.columns
    assert 'performance_category' in processed_df.columns
    
    # Verificar que los tipos de datos son correctos
    assert processed_df['student_id'].dtype == 'object'  # str
    assert processed_df['GPA'].dtype == 'float64'
    assert processed_df['current_semester'].dtype == 'int64'
    assert processed_df['scholarship'].dtype == 'bool'
    
    # Verificar las nuevas columnas calculadas
    assert processed_df['age'].dtype == 'int64'
    assert all(processed_df['age'] > 0)  # Todas las edades son positivas

def test_validate_data_without_issues(sample_dataframe):
    """Prueba la validación de datos sin problemas."""
    problems = validate_data(sample_dataframe)
    
    # No debería haber problemas en el DataFrame de muestra
    assert len(problems) == 0


def test_validate_data_with_issues(dataframe_with_issues):
    """Prueba la validación de datos con problemas."""
    problems = validate_data(dataframe_with_issues)
    
    # Debería detectar al menos 3 problemas:
    # 1. Semestre negativo
    # 2. Créditos restantes negativos
    # 3. GPA fuera de rango
    # 4. Fecha de nacimiento en el futuro
    # 5. Fecha de matrícula en el futuro
    assert len(problems) >= 3
    
    # Verificar mensajes específicos
    has_negative_semester = any("valores negativos encontrados en la columna 'current_semester'" in p for p in problems)
    has_negative_credits = any("valores negativos encontrados en la columna 'credits_remaining'" in p for p in problems)
    has_gpa_out_of_range = any("valores de GPA están fuera del rango 0-5" in p for p in problems)
    
    assert has_negative_semester
    assert has_negative_credits
    assert has_gpa_out_of_range


def test_feature_engineering(sample_dataframe):
    """Prueba que el cálculo de características adicionales funcione correctamente."""
    processed_df = preprocess_data(sample_dataframe)
    
    # Verificar que se calcularon correctamente las edades y años matriculados
    today = datetime.now()
    
    # Verificar que las edades son razonables
    for i, row in processed_df.iterrows():
        expected_age = (today - sample_dataframe.loc[i, 'date_of_birth']).days // 365
        assert abs(row['age'] - expected_age) <= 1  # Permitir una diferencia de 1 año por redondeo
