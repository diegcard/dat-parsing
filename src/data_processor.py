"""
Módulo para procesar y limpiar datos universitarios.
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, List


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa y limpia los datos universitarios.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios cargados.
        
    Returns:
        pd.DataFrame: DataFrame con los datos procesados y limpios.
    """
    # Crear una copia del DataFrame para no modificar el original
    processed_df = df.copy()
    
    # Manejo de valores faltantes (aunque no esperamos valores faltantes en los datos generados)
    # Para columnas numéricas, usar la mediana
    numeric_cols = ['current_semester', 'Number_of_credits_approved', 'credits_remaining', 
                    'GPA', 'course_load', 'library_books_borrowed']
    for col in numeric_cols:
        if processed_df[col].isna().any():
            processed_df[col] = processed_df[col].fillna(processed_df[col].median())
    
    # Para columnas categóricas, usar 'Unknown'
    categorical_cols = ['gender', 'nationality', 'program', 'state_program', 
                        'student_status', 'payment_status', 'academic_standing']
    for col in categorical_cols:
        if processed_df[col].isna().any():
            processed_df[col] = processed_df[col].fillna('Unknown')
    
    # Verificación/conversión de tipos de datos
    # Asegurarse de que student_id sea string
    processed_df['student_id'] = processed_df['student_id'].astype(str)
    
    # Asegurarse de que GPA sea float
    processed_df['GPA'] = processed_df['GPA'].astype(float)
    
    # Asegurarse de que current_semester, credits_approved y credits_remaining sean int
    processed_df['current_semester'] = processed_df['current_semester'].astype(int)
    processed_df['Number_of_credits_approved'] = processed_df['Number_of_credits_approved'].astype(int)
    processed_df['credits_remaining'] = processed_df['credits_remaining'].astype(int)
    
    # Asegurarse de que scholarship sea boolean
    processed_df['scholarship'] = processed_df['scholarship'].astype(bool)
    
    # Ingeniería de características
    # Calcular la edad de los estudiantes
    today = datetime.now()
    processed_df['age'] = (today - processed_df['date_of_birth']).dt.days // 365
    
    # Calcular años matriculados
    processed_df['years_enrolled'] = (today - processed_df['enrollment_date']).dt.days / 365
    
    # Validación de datos
    # GPA debe estar entre 0 y 5
    processed_df.loc[processed_df['GPA'] < 0, 'GPA'] = 0
    processed_df.loc[processed_df['GPA'] > 5, 'GPA'] = 5
    
    # credits_remaining no debe ser negativo
    processed_df.loc[processed_df['credits_remaining'] < 0, 'credits_remaining'] = 0
    
    # Crear categoría de rendimiento académico basado en GPA
    processed_df['performance_category'] = pd.cut(
        processed_df['GPA'], 
        bins=[0, 2.0, 3.0, 3.5, 4.0, 5.0], 
        labels=['Muy bajo', 'Bajo', 'Medio', 'Alto', 'Excelente']
    )
    
    return processed_df


def validate_data(df: pd.DataFrame) -> List[str]:
    """
    Valida los datos universitarios y devuelve una lista de problemas encontrados.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        
    Returns:
        List[str]: Lista de problemas encontrados en los datos.
    """
    problems = []
    
    # Verificar valores negativos en columnas que deberían ser no negativas
    for col in ['current_semester', 'Number_of_credits_approved', 'credits_remaining', 
                'course_load', 'library_books_borrowed']:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            problems.append(f"{neg_count} valores negativos encontrados en la columna '{col}'")
    
    # Verificar GPA fuera de rango
    gpa_out_of_range = ((df['GPA'] < 0) | (df['GPA'] > 5)).sum()
    if gpa_out_of_range > 0:
        problems.append(f"{gpa_out_of_range} valores de GPA están fuera del rango 0-5")
    
    # Verificar fechas de nacimiento que resulten en edades negativas o muy altas
    today = datetime.now()
    ages = (today - df['date_of_birth']).dt.days / 365
    young = (ages < 15).sum()
    old = (ages > 80).sum()
    if young > 0:
        problems.append(f"{young} estudiantes tienen menos de 15 años")
    if old > 0:
        problems.append(f"{old} estudiantes tienen más de 80 años")
    
    # Verificar fechas de matrícula en el futuro
    future_enrollments = (df['enrollment_date'] > today).sum()
    if future_enrollments > 0:
        problems.append(f"{future_enrollments} fechas de matrícula están en el futuro")
    
    return problems


if __name__ == "__main__":
    # Este bloque solo se ejecuta si este script es ejecutado directamente
    import os
    from data_loader import load_university_data
    
    try:
        data_path = os.path.join('..', 'data', 'university_data.csv')
        df = load_university_data(data_path)
        print(f"Datos cargados exitosamente. Shape: {df.shape}")
        
        processed_df = preprocess_data(df)
        print(f"Datos procesados exitosamente. Shape: {processed_df.shape}")
        
        problems = validate_data(processed_df)
        if problems:
            print("Problemas encontrados en los datos:")
            for problem in problems:
                print(f"- {problem}")
        else:
            print("No se encontraron problemas en los datos.")
            
        print("\nColumnas añadidas durante el procesamiento:")
        new_cols = set(processed_df.columns) - set(df.columns)
        for col in new_cols:
            print(f"- {col}")
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
