"""
Pruebas unitarias para el módulo analysis.
"""
import pytest
import pandas as pd
import numpy as np
from src.analysis import (
    get_descriptive_statistics, 
    get_value_counts, 
    get_correlation_matrix,
    analyze_gpa_by_program,
    analyze_scholarship_distribution,
    analyze_credits_by_semester,
    analyze_student_status_by_academic_standing,
    get_top_programs_by_gpa
)


@pytest.fixture
def sample_dataframe():
    """
    Fixture que crea un DataFrame de muestra para pruebas.
    """
    # Crear DataFrame de muestra con datos variados
    data = {
        'student_id': ['STU000001', 'STU000002', 'STU000003', 'STU000004', 'STU000005', 'STU000006'],
        'gender': ['Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
        'program': ['Biology', 'Computer Science', 'Biology', 'Mathematics', 'Computer Science', 'Mathematics'],
        'current_semester': [8, 5, 3, 6, 7, 2],
        'Number_of_credits_approved': [147, 85, 50, 110, 130, 35],
        'credits_remaining': [30, 92, 127, 67, 47, 142],
        'GPA': [3.07, 4.2, 3.8, 2.9, 3.5, 4.0],
        'student_status': ['Active', 'Active', 'Inactive', 'Active', 'Active', 'Inactive'],
        'scholarship': [False, True, False, True, False, True],
        'academic_standing': ['Average', 'Excellent', 'Good', 'Average', 'Good', 'Excellent'],
        'course_load': [18, 20, 15, 19, 17, 16],
        'library_books_borrowed': [1, 0, 3, 2, 1, 0]
    }
    
    return pd.DataFrame(data)


def test_get_descriptive_statistics(sample_dataframe):
    """Prueba la función de estadísticas descriptivas."""
    stats = get_descriptive_statistics(sample_dataframe)
    
    # Verificar que se calcularon estadísticas para las columnas correctas
    assert 'GPA' in stats.columns
    assert 'current_semester' in stats.columns
    assert 'Number_of_credits_approved' in stats.columns
    
    # Verificar que las estadísticas son correctas
    assert stats.loc['mean', 'GPA'] == pytest.approx(3.5783, 0.001)
    assert stats.loc['min', 'Number_of_credits_approved'] == 35
    assert stats.loc['max', 'current_semester'] == 8
    
    # Probar con lista específica de columnas
    specific_stats = get_descriptive_statistics(sample_dataframe, ['GPA', 'course_load'])
    assert len(specific_stats.columns) == 2
    assert 'GPA' in specific_stats.columns
    assert 'course_load' in specific_stats.columns


def test_get_value_counts(sample_dataframe):
    """Prueba la función de conteo de valores."""
    program_counts = get_value_counts(sample_dataframe, 'program')
    
    # Verificar los conteos
    assert program_counts['Biology'] == 2
    assert program_counts['Computer Science'] == 2
    assert program_counts['Mathematics'] == 2
    
    # Verificar que la suma de los conteos es igual al número de filas
    assert program_counts.sum() == len(sample_dataframe)
    
    # Probar con otra columna
    gender_counts = get_value_counts(sample_dataframe, 'gender')
    assert gender_counts['Female'] == 3
    assert gender_counts['Male'] == 3
    
    # Probar con columna inexistente
    with pytest.raises(ValueError):
        get_value_counts(sample_dataframe, 'columna_inexistente')


def test_get_correlation_matrix(sample_dataframe):
    """Prueba la función de matriz de correlación."""
    corr_matrix = get_correlation_matrix(sample_dataframe)
    
    # Verificar que la matriz tiene la forma correcta
    assert corr_matrix.shape[0] == corr_matrix.shape[1]  # Es cuadrada
    
    # Verificar que las correlaciones en la diagonal son 1.0
    for col in corr_matrix.columns:
        assert corr_matrix.loc[col, col] == 1.0
    
    # Verificar algunas correlaciones específicas
    assert corr_matrix.loc['GPA', 'Number_of_credits_approved'] == pytest.approx(sample_dataframe['GPA'].corr(sample_dataframe['Number_of_credits_approved']), 0.001)
    
    # Probar con lista específica de columnas
    specific_corr = get_correlation_matrix(sample_dataframe, ['GPA', 'course_load'])
    assert specific_corr.shape == (2, 2)
    assert 'GPA' in specific_corr.columns
    assert 'course_load' in specific_corr.columns


def test_analyze_gpa_by_program(sample_dataframe):
    """Prueba la función de análisis de GPA por programa."""
    gpa_stats = analyze_gpa_by_program(sample_dataframe)
    
    # Verificar que hay estadísticas para cada programa
    assert len(gpa_stats) == 3  # Tres programas en el conjunto de datos
    
    # Verificar columnas de estadísticas
    assert 'promedio' in gpa_stats.columns
    assert 'mediana' in gpa_stats.columns
    assert 'mínimo' in gpa_stats.columns
    assert 'máximo' in gpa_stats.columns
    
    # Verificar promedios específicos
    assert gpa_stats.loc['Computer Science', 'promedio'] == pytest.approx(3.85, 0.001)
    assert gpa_stats.loc['Biology', 'promedio'] == pytest.approx(3.435, 0.001)
    assert gpa_stats.loc['Mathematics', 'promedio'] == pytest.approx(3.45, 0.001)



def test_analyze_credits_by_semester(sample_dataframe):
    """Prueba la función de análisis de créditos por semestre."""
    credits_stats = analyze_credits_by_semester(sample_dataframe)
    
    # Verificar que hay estadísticas para cada semestre
    assert len(credits_stats) == 6  # Seis semestres diferentes
    
    # Verificar columnas de estadísticas
    assert 'promedio_creditos' in credits_stats.columns
    assert 'total_estudiantes' in credits_stats.columns
    
    # Verificar valores específicos
    semester_5_row = credits_stats.loc[5]
    assert semester_5_row['total_estudiantes'] == 1
    assert semester_5_row['promedio_creditos'] == 85
    
    semester_8_row = credits_stats.loc[8]
    assert semester_8_row['total_estudiantes'] == 1
    assert semester_8_row['promedio_creditos'] == 147



def test_get_top_programs_by_gpa(sample_dataframe):
    """Prueba la función para obtener los programas principales por GPA."""
    top_programs = get_top_programs_by_gpa(sample_dataframe, top_n=2)
    
    # Verificar que se seleccionan correctamente los N principales
    assert len(top_programs) == 2
    
    # Verificar que las columnas son correctas
    assert 'promedio_gpa' in top_programs.columns
    assert 'total_estudiantes' in top_programs.columns
    
    # Verificar que el orden es correcto (descendente por GPA promedio)
    assert top_programs.index[0] == 'Computer Science'  # Programa con mayor GPA promedio
    assert top_programs.index[1] == 'Mathematics'  # Segundo programa con mayor GPA promedio
