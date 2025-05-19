"""
Módulo para realizar análisis de datos universitarios.
"""
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Tuple


def get_descriptive_statistics(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Calcula estadísticas descriptivas para las columnas numéricas especificadas.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        columns (Optional[List[str]], optional): Lista de columnas para las que calcular estadísticas.
            Si es None, se calculan para todas las columnas numéricas. Default es None.
        
    Returns:
        pd.DataFrame: DataFrame con las estadísticas descriptivas.
    """
    if columns is None:
        # Columnas numéricas por defecto
        columns = ['GPA', 'Number_of_credits_approved', 'credits_remaining', 
                   'current_semester', 'course_load', 'library_books_borrowed']
                   
    # Filtrar solo las columnas numéricas que existen en el DataFrame
    numeric_columns = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    
    if not numeric_columns:
        return pd.DataFrame()
    
    # Calcular estadísticas descriptivas
    stats = df[numeric_columns].describe()
    
    # Añadir la mediana en caso de que no esté incluida
    if '50%' not in stats.index:
        medians = df[numeric_columns].median()
        stats = pd.concat([stats, pd.DataFrame(medians.values, 
                                              index=['median'], 
                                              columns=medians.index)])
    
    return stats


def get_value_counts(df: pd.DataFrame, column_name: str) -> pd.Series:
    """
    Obtiene el conteo de frecuencias para una columna categórica.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        column_name (str): Nombre de la columna para la que calcular frecuencias.
        
    Returns:
        pd.Series: Serie con los conteos de frecuencias.
        
    Raises:
        ValueError: Si la columna no existe en el DataFrame.
    """
    if column_name not in df.columns:
        raise ValueError(f"La columna '{column_name}' no existe en el DataFrame.")
    
    return df[column_name].value_counts()


def get_correlation_matrix(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Calcula la matriz de correlación para las columnas numéricas especificadas.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        columns (Optional[List[str]], optional): Lista de columnas para las que calcular correlaciones.
            Si es None, se calculan para todas las columnas numéricas. Default es None.
        
    Returns:
        pd.DataFrame: DataFrame con la matriz de correlación.
    """
    if columns is None:
        # Detectar automáticamente columnas numéricas
        numeric_dtypes = ['int64', 'float64']
        columns = df.select_dtypes(include=numeric_dtypes).columns.tolist()
    else:
        # Filtrar solo las columnas numéricas que existen en el DataFrame
        columns = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    
    if not columns:
        return pd.DataFrame()
    
    return df[columns].corr()


def analyze_gpa_by_program(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estadísticas del GPA por programa académico.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        
    Returns:
        pd.DataFrame: DataFrame con estadísticas de GPA por programa.
    """
    # Agrupar por programa y calcular estadísticas
    gpa_stats = df.groupby('program')['GPA'].agg([
        ('promedio', 'mean'),
        ('mediana', 'median'),
        ('mínimo', 'min'),
        ('máximo', 'max'),
        ('desviación_estándar', 'std'),
        ('count', 'count')
    ]).sort_values('promedio', ascending=False)
    
    return gpa_stats


def analyze_scholarship_distribution(df: pd.DataFrame, groupby_column: str = 'program') -> pd.DataFrame:
    """
    Analiza la distribución de becas por una columna de agrupación.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        groupby_column (str, optional): Columna por la que agrupar. Default es 'program'.
        
    Returns:
        pd.DataFrame: DataFrame con la distribución de becas.
        
    Raises:
        ValueError: Si la columna de agrupación no existe en el DataFrame.
    """
    if groupby_column not in df.columns:
        raise ValueError(f"La columna '{groupby_column}' no existe en el DataFrame.")
    
    # Agrupar por la columna especificada y calcular estadísticas de becas
    scholarship_dist = df.groupby(groupby_column)['scholarship'].agg([
        ('total_estudiantes', 'count'),
        ('estudiantes_con_beca', lambda x: x.sum()),
        ('porcentaje_con_beca', lambda x: x.mean() * 100)
    ]).sort_values('porcentaje_con_beca', ascending=False)
    
    return scholarship_dist


def analyze_credits_by_semester(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza los créditos aprobados por semestre.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        
    Returns:
        pd.DataFrame: DataFrame con estadísticas de créditos por semestre.
    """
    # Agrupar por semestre y calcular estadísticas de créditos
    credits_stats = df.groupby('current_semester')['Number_of_credits_approved'].agg([
        ('promedio_creditos', 'mean'),
        ('total_estudiantes', 'count'),
        ('mediana_creditos', 'median'),
        ('max_creditos', 'max'),
        ('min_creditos', 'min')
    ]).sort_index()
    
    return credits_stats


def analyze_student_status_by_academic_standing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza el estado del estudiante por rendimiento académico.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        
    Returns:
        pd.DataFrame: DataFrame con la distribución de estados por rendimiento académico.
    """
    # Crear tabla de contingencia
    status_standing = pd.crosstab(
        df['academic_standing'], 
        df['student_status'],
        normalize='index'
    ) * 100
    
    # Añadir totales por categoría
    status_standing['total_count'] = df.groupby('academic_standing').size()
    
    return status_standing


def get_top_programs_by_gpa(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Obtiene los programas con mayor GPA promedio.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        top_n (int, optional): Número de programas a devolver. Default es 5.
        
    Returns:
        pd.DataFrame: DataFrame con los programas top por GPA.
    """
    top_programs = df.groupby('program')['GPA'].agg([
        ('promedio_gpa', 'mean'),
        ('total_estudiantes', 'count')
    ]).sort_values('promedio_gpa', ascending=False).head(top_n)
    
    return top_programs


if __name__ == "__main__":
    # Este bloque solo se ejecuta si este script es ejecutado directamente
    import os
    import sys
    
    # Asegurarnos de que podemos importar desde el directorio raíz
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from src.data_loader import load_university_data
    from src.data_processor import preprocess_data
    
    try:
        # Cargar y procesar datos
        data_path = os.path.join('..', 'data', 'university_data.csv')
        df = load_university_data(data_path)
        df = preprocess_data(df)
        
        # Ejecutar análisis
        print("\n===== Estadísticas Descriptivas =====")
        desc_stats = get_descriptive_statistics(df)
        print(desc_stats)
        
        print("\n===== Distribución por Programa =====")
        program_counts = get_value_counts(df, 'program')
        print(program_counts.head(10))
        
        print("\n===== Matriz de Correlación =====")
        corr_matrix = get_correlation_matrix(df, ['GPA', 'Number_of_credits_approved', 'age'])
        print(corr_matrix)
        
        print("\n===== GPA por Programa =====")
        gpa_by_program = analyze_gpa_by_program(df)
        print(gpa_by_program.head(10))
        
        print("\n===== Distribución de Becas por Género =====")
        scholarship_by_gender = analyze_scholarship_distribution(df, 'gender')
        print(scholarship_by_gender)
        
        print("\n===== Créditos por Semestre =====")
        credits_by_semester = analyze_credits_by_semester(df)
        print(credits_by_semester)
        
    except Exception as e:
        print(f"Error al realizar el análisis: {e}")
