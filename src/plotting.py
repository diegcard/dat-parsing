"""
Módulo para generar visualizaciones de datos universitarios.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Dict, Tuple


def configure_plot_style():
    """Configura el estilo general de las visualizaciones."""
    # Configurar estilo de seaborn
    sns.set_style("whitegrid")
    # Configurar paleta de colores
    sns.set_palette("viridis")
    # Configurar tamaño de fuente
    plt.rcParams.update({
        'font.size': 10,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16
    })


def save_plot(fig, output_path: str, dpi: int = 300):
    """
    Guarda una figura en la ruta especificada.
    
    Args:
        fig: Figura de matplotlib a guardar.
        output_path (str): Ruta donde guardar la figura.
        dpi (int, optional): Resolución de la imagen. Default es 300.
    """
    # Crear el directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Guardar la figura
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
    plt.close(fig)


def plot_gpa_distribution(df: pd.DataFrame, output_path: str) -> str:
    """
    Genera un histograma de la distribución de GPA.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        output_path (str): Ruta donde guardar la visualización.
        
    Returns:
        str: Análisis textual de la visualización.
    """
    configure_plot_style()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Crear histograma con KDE
    sns.histplot(df['GPA'], kde=True, bins=20, color='purple', alpha=0.7, ax=ax)
    
    # Añadir líneas verticales para la media y mediana
    mean_gpa = df['GPA'].mean()
    median_gpa = df['GPA'].median()
    ax.axvline(mean_gpa, color='red', linestyle='--', linewidth=1.5, 
               label=f'Media: {mean_gpa:.2f}')
    ax.axvline(median_gpa, color='green', linestyle='-.', linewidth=1.5,
               label=f'Mediana: {median_gpa:.2f}')
    
    # Configurar etiquetas y título
    ax.set_xlabel('GPA (Promedio Académico)')
    ax.set_ylabel('Frecuencia')
    ax.set_title('Distribución del Promedio Académico (GPA) de Estudiantes')
    
    # Añadir leyenda
    ax.legend()
    
    # Guardar la figura
    save_plot(fig, output_path)
    
    # Generar análisis textual
    analysis = (
        f"Análisis de la Distribución de GPA:\n"
        f"- El GPA promedio de los estudiantes es {mean_gpa:.2f}.\n"
        f"- La mediana del GPA es {median_gpa:.2f}, lo que indica que el 50% de los estudiantes tienen un GPA "
        f"{'superior' if median_gpa < mean_gpa else 'inferior'} a este valor.\n"
        f"- La distribución muestra {'una asimetría hacia la derecha' if df['GPA'].skew() > 0 else 'una asimetría hacia la izquierda' if df['GPA'].skew() < 0 else 'simetría'}, "
        f"lo que sugiere que {'hay más estudiantes con GPA por debajo de la media' if df['GPA'].skew() > 0 else 'hay más estudiantes con GPA por encima de la media' if df['GPA'].skew() < 0 else 'la distribución de GPA es bastante uniforme'}.\n"
        f"- El rango de GPA va desde {df['GPA'].min():.2f} hasta {df['GPA'].max():.2f}."
    )
    
    return analysis


def plot_students_per_program(df: pd.DataFrame, output_path: str) -> str:
    """
    Genera un gráfico de barras del número de estudiantes por programa.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        output_path (str): Ruta donde guardar la visualización.
        
    Returns:
        str: Análisis textual de la visualización.
    """
    configure_plot_style()
    
    # Obtener los conteos por programa
    program_counts = df['program'].value_counts()
    
    # Ordenar de mayor a menor y tomar los 15 programas más grandes si hay muchos
    if len(program_counts) > 15:
        program_counts = program_counts.head(15)
        title_suffix = " (Top 15)"
    else:
        title_suffix = ""
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Crear gráfico de barras
    bars = sns.barplot(x=program_counts.values, y=program_counts.index, 
              palette='viridis', alpha=0.8, ax=ax)
    
    # Añadir etiquetas con los valores
    for i, v in enumerate(program_counts.values):
        ax.text(v + 0.5, i, str(v), va='center')
    
    # Configurar etiquetas y título
    ax.set_xlabel('Número de Estudiantes')
    ax.set_ylabel('Programa Académico')
    ax.set_title(f'Número de Estudiantes por Programa Académico{title_suffix}')
    
    # Ajustar diseño
    plt.tight_layout()
    
    # Guardar la figura
    save_plot(fig, output_path)
    
    # Generar análisis textual
    total_students = df.shape[0]
    top_program = program_counts.index[0]
    top_program_count = program_counts.values[0]
    top_program_percentage = (top_program_count / total_students) * 100
    
    analysis = (
        f"Análisis de Estudiantes por Programa:\n"
        f"- De un total de {total_students} estudiantes, el programa con mayor número de estudiantes es '{top_program}' "
        f"con {top_program_count} estudiantes ({top_program_percentage:.1f}% del total).\n"
        f"- Los {len(program_counts)} programas mostrados representan "
        f"{'la totalidad' if len(program_counts) == len(df['program'].unique()) else 'una parte significativa'} de la oferta académica.\n"
        f"- Se observa {'una distribución relativamente uniforme' if program_counts.values.std() / program_counts.values.mean() < 0.5 else 'una variación considerable'} "
        f"en el número de estudiantes por programa."
    )
    
    return analysis


def plot_gpa_vs_credits(df: pd.DataFrame, output_path: str) -> str:
    """
    Genera un gráfico de dispersión de GPA vs Créditos Aprobados.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        output_path (str): Ruta donde guardar la visualización.
        
    Returns:
        str: Análisis textual de la visualización.
    """
    configure_plot_style()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Crear gráfico de dispersión con color por scholarship
    scatter = sns.scatterplot(
        data=df,
        x='Number_of_credits_approved',
        y='GPA',
        hue='scholarship',
        palette={True: 'gold', False: 'steelblue'},
        alpha=0.7,
        s=70,
        ax=ax
    )
    
    # Añadir línea de tendencia
    sns.regplot(
        data=df,
        x='Number_of_credits_approved',
        y='GPA',
        scatter=False,
        ax=ax,
        line_kws={'color': 'red', 'linewidth': 1, 'linestyle': '--'}
    )
    
    # Configurar etiquetas y título
    ax.set_xlabel('Número de Créditos Aprobados')
    ax.set_ylabel('GPA (Promedio Académico)')
    ax.set_title('Relación entre GPA y Número de Créditos Aprobados')
    
    # Actualizar leyenda
    handles, labels = ax.get_legend_handles_labels()
    labels = ['Sin Beca', 'Con Beca'] if labels == ['False', 'True'] else labels
    ax.legend(handles, labels, title='Estatus de Beca')
    
    # Guardar la figura
    save_plot(fig, output_path)
    
    # Calcular correlación para análisis textual
    correlation = df['GPA'].corr(df['Number_of_credits_approved'])
    
    # Comparativa de GPA entre estudiantes con y sin beca
    gpa_with_scholarship = df[df['scholarship'] == True]['GPA'].mean()
    gpa_without_scholarship = df[df['scholarship'] == False]['GPA'].mean()
    scholarship_diff = gpa_with_scholarship - gpa_without_scholarship
    
    analysis = (
        f"Análisis de GPA vs Créditos Aprobados:\n"
        f"- Existe una correlación {'positiva' if correlation > 0 else 'negativa'} de {abs(correlation):.2f} entre el GPA y el número de créditos aprobados, "
        f"lo que sugiere que {'a medida que los estudiantes aprueban más créditos, tienden a tener un GPA más alto' if correlation > 0 else 'no hay una relación fuerte entre ambas variables' if abs(correlation) < 0.3 else 'a medida que los estudiantes aprueban más créditos, tienden a tener un GPA más bajo'}.\n"
        f"- Los estudiantes con beca tienen un GPA promedio de {gpa_with_scholarship:.2f}, mientras que los estudiantes sin beca tienen un GPA promedio de {gpa_without_scholarship:.2f} "
        f"(una diferencia de {abs(scholarship_diff):.2f} puntos {'a favor de los becados' if scholarship_diff > 0 else 'a favor de los no becados'}).\n"
        f"- {'Se observa una tendencia donde los estudiantes con más créditos aprobados generalmente tienen un GPA más alto, lo que podría indicar que la experiencia académica contribuye positivamente al rendimiento.' if correlation > 0.3 else 'No se observa una tendencia clara entre el número de créditos aprobados y el GPA, lo que sugiere que otros factores pueden ser más determinantes en el rendimiento académico.'}"
    )
    
    return analysis


def plot_scholarship_status(df: pd.DataFrame, output_path: str) -> str:
    """
    Genera un gráfico de pastel de la distribución de becas.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        output_path (str): Ruta donde guardar la visualización.
        
    Returns:
        str: Análisis textual de la visualización.
    """
    configure_plot_style()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Calcular porcentajes
    scholarship_counts = df['scholarship'].value_counts()
    scholarship_percent = (scholarship_counts / scholarship_counts.sum()) * 100
    
    # Etiquetas para el gráfico
    labels = [f'Sin Beca ({scholarship_percent[False]:.1f}%)', 
              f'Con Beca ({scholarship_percent[True]:.1f}%)']
    
    # Crear gráfico de pastel
    ax.pie(scholarship_counts, labels=labels, autopct='%1.1f%%', 
           startangle=90, colors=['steelblue', 'gold'], 
           wedgeprops={'edgecolor': 'w', 'linewidth': 1})
    
    # Añadir título
    ax.set_title('Distribución de Estudiantes por Estatus de Beca')
    
    # Hacer el gráfico circular
    ax.axis('equal')
    
    # Guardar la figura
    save_plot(fig, output_path)
    
    # Generar análisis textual
    with_scholarship = scholarship_counts.get(True, 0)
    without_scholarship = scholarship_counts.get(False, 0)
    total = with_scholarship + without_scholarship
    
    analysis = (
        f"Análisis de la Distribución de Becas:\n"
        f"- De un total de {total} estudiantes, {with_scholarship} ({(with_scholarship/total*100):.1f}%) cuentan con beca, "
        f"mientras que {without_scholarship} ({(without_scholarship/total*100):.1f}%) no tienen beca.\n"
        f"- La proporción de estudiantes con beca es de aproximadamente 1 por cada {(total/with_scholarship):.1f} estudiantes.\n"
        f"- {'La mayoría de los estudiantes no cuentan con beca, lo que podría indicar criterios estrictos para su asignación.' if without_scholarship > with_scholarship else 'Una proporción significativa de estudiantes cuenta con beca, lo que podría indicar una fuerte política de apoyo financiero en la institución.'}"
    )
    
    return analysis


def plot_academic_standing_distribution(df: pd.DataFrame, output_path: str) -> str:
    """
    Genera un gráfico de barras de la distribución de rendimiento académico.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        output_path (str): Ruta donde guardar la visualización.
        
    Returns:
        str: Análisis textual de la visualización.
    """
    configure_plot_style()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Obtener conteos de rendimiento académico
    standing_counts = df['academic_standing'].value_counts().sort_index()
    
    # Crear gráfico de barras
    bars = sns.barplot(x=standing_counts.index, y=standing_counts.values, 
                       palette='viridis', alpha=0.8, ax=ax)
    
    # Añadir etiquetas con valores
    for i, v in enumerate(standing_counts.values):
        ax.text(i, v + 5, str(v), ha='center')
    
    # Configurar etiquetas y título
    ax.set_xlabel('Rendimiento Académico')
    ax.set_ylabel('Número de Estudiantes')
    ax.set_title('Distribución de Estudiantes por Rendimiento Académico')
    
    # Rotar etiquetas del eje x si es necesario
    plt.xticks(rotation=45 if len(standing_counts) > 5 else 0)
    
    # Ajustar diseño
    plt.tight_layout()
    
    # Guardar la figura
    save_plot(fig, output_path)
    
    # Generar análisis textual
    total = standing_counts.sum()
    top_standing = standing_counts.idxmax()
    top_standing_count = standing_counts.max()
    
    analysis = (
        f"Análisis de la Distribución de Rendimiento Académico:\n"
        f"- El rendimiento académico más común entre los {total} estudiantes es '{top_standing}', "
        f"con {top_standing_count} estudiantes ({(top_standing_count/total*100):.1f}% del total).\n"
        f"- La distribución muestra que {'la mayoría de los estudiantes se concentran en rendimientos medios' if 'Average' in standing_counts and standing_counts['Average'] == top_standing_count else 'hay una variación significativa en el rendimiento académico de los estudiantes'}.\n"
        f"- {'Hay una proporción relativamente baja de estudiantes con rendimiento académico bajo o en riesgo' if 'Poor' in standing_counts and standing_counts['Poor'] < total * 0.2 else 'Hay una proporción considerable de estudiantes con rendimiento académico bajo, lo que podría requerir programas de apoyo académico'}"
    )
    
    return analysis


def plot_gpa_boxplot_by_program(df: pd.DataFrame, output_path: str) -> str:
    """
    Genera un gráfico de caja del GPA por programa.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos universitarios.
        output_path (str): Ruta donde guardar la visualización.
        
    Returns:
        str: Análisis textual de la visualización.
    """
    configure_plot_style()
    
    # Tomar los 10 programas más comunes para no sobrecargar el gráfico
    top_programs = df['program'].value_counts().head(10).index.tolist()
    df_filtered = df[df['program'].isin(top_programs)].copy()
    
    # Ordenar por GPA promedio
    program_order = df_filtered.groupby('program')['GPA'].mean().sort_values(ascending=False).index
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Crear gráfico de caja
    sns.boxplot(
        data=df_filtered,
        x='program',
        y='GPA',
        order=program_order,
        palette='viridis',
        ax=ax
    )
    
    # Configurar etiquetas y título
    ax.set_xlabel('Programa Académico')
    ax.set_ylabel('GPA (Promedio Académico)')
    ax.set_title('Distribución de GPA por Programa Académico (Top 10 programas por número de estudiantes)')
    
    # Rotar etiquetas del eje x para mejor visualización
    plt.xticks(rotation=45, ha='right')
    
    # Ajustar diseño
    plt.tight_layout()
    
    # Guardar la figura
    save_plot(fig, output_path)
    
    # Calcular estadísticas para el análisis
    program_stats = df_filtered.groupby('program')['GPA'].agg(['mean', 'median', 'std']).loc[program_order]
    top_program = program_stats.index[0]
    top_program_mean = program_stats.loc[top_program, 'mean']
    
    # Obtener programa con mayor variabilidad
    most_variable_program = program_stats['std'].idxmax()
    most_variable_std = program_stats.loc[most_variable_program, 'std']
    
    analysis = (
        f"Análisis de GPA por Programa Académico:\n"
        f"- El programa con el GPA promedio más alto es '{top_program}' con un promedio de {top_program_mean:.2f}.\n"
        f"- El programa con mayor variabilidad en el GPA es '{most_variable_program}' (desviación estándar de {most_variable_std:.2f}), "
        f"lo que indica una mayor dispersión en el rendimiento académico de sus estudiantes.\n"
        f"- {'Se observa una variación significativa en el GPA promedio entre diferentes programas, lo que podría reflejar diferencias en la dificultad académica o en los criterios de evaluación.' if program_stats['mean'].max() - program_stats['mean'].min() > 0.5 else 'No se observan grandes diferencias en el GPA promedio entre los programas, lo que sugiere una consistencia en los estándares académicos.'}\n"
        f"- Este análisis está basado en los 10 programas con mayor número de estudiantes, que representan una parte significativa de la población estudiantil."
    )
    
    return analysis


def plot_correlation_heatmap(correlation_matrix: pd.DataFrame, output_path: str) -> str:
    """
    Genera un mapa de calor de la matriz de correlación.
    
    Args:
        correlation_matrix (pd.DataFrame): Matriz de correlación.
        output_path (str): Ruta donde guardar la visualización.
        
    Returns:
        str: Análisis textual de la visualización.
    """
    configure_plot_style()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Crear mapa de calor
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    heatmap = sns.heatmap(
        correlation_matrix,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        center=0,
        square=True,
        linewidths=1,
        ax=ax
    )
    
    # Configurar título
    ax.set_title('Matriz de Correlación de Variables Numéricas')
    
    # Ajustar diseño
    plt.tight_layout()
    
    # Guardar la figura
    save_plot(fig, output_path)
    
    # Encontrar las correlaciones más fuertes
    corr_data = correlation_matrix.where(~np.eye(correlation_matrix.shape[0], dtype=bool))
    strongest_positive = corr_data.unstack().dropna().sort_values(ascending=False).head(2)
    strongest_negative = corr_data.unstack().dropna().sort_values().head(2)
    
    analysis = (
        f"Análisis de la Matriz de Correlación:\n"
        f"- La correlación positiva más fuerte se observa entre {strongest_positive.index[0][0]} y {strongest_positive.index[0][1]} (r = {strongest_positive.values[0]:.2f}), "
        f"seguida por {strongest_positive.index[1][0]} y {strongest_positive.index[1][1]} (r = {strongest_positive.values[1]:.2f}).\n"
        f"- La correlación negativa más fuerte se observa entre {strongest_negative.index[0][0]} y {strongest_negative.index[0][1]} (r = {strongest_negative.values[0]:.2f}), "
        f"seguida por {strongest_negative.index[1][0]} y {strongest_negative.index[1][1]} (r = {strongest_negative.values[1]:.2f}).\n"
        f"- {'En general, se observan correlaciones fuertes entre múltiples variables, lo que sugiere interdependencias significativas en los datos.' if np.abs(correlation_matrix.values).mean() > 0.4 else 'En general, las correlaciones entre variables son moderadas o débiles, lo que sugiere que las variables son relativamente independientes entre sí.'}"
    )
    
    return analysis


if __name__ == "__main__":
    # Este bloque solo se ejecuta si este script es ejecutado directamente
    import os
    import sys
    
    # Asegurarnos de que podemos importar desde el directorio raíz
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from src.data_loader import load_university_data
    from src.data_processor import preprocess_data
    from src.analysis import get_correlation_matrix
    
    try:
        # Cargar y procesar datos
        data_path = os.path.join('..', 'data', 'university_data.csv')
        df = load_university_data(data_path)
        df = preprocess_data(df)
        
        # Configurar ruta de salida
        output_dir = os.path.join('..', 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Generar visualizaciones
        print("\n===== Generando Distribución de GPA =====")
        analysis_gpa = plot_gpa_distribution(df, os.path.join(output_dir, 'gpa_distribution.png'))
        print(analysis_gpa)
        
        print("\n===== Generando Estudiantes por Programa =====")
        analysis_programs = plot_students_per_program(df, os.path.join(output_dir, 'students_per_program.png'))
        print(analysis_programs)
        
        print("\n===== Generando GPA vs Créditos =====")
        analysis_gpa_credits = plot_gpa_vs_credits(df, os.path.join(output_dir, 'gpa_vs_credits.png'))
        print(analysis_gpa_credits)
        
        print("\n===== Generando Distribución de Becas =====")
        analysis_scholarship = plot_scholarship_status(df, os.path.join(output_dir, 'scholarship_status.png'))
        print(analysis_scholarship)
        
        print("\n===== Generando Distribución de Rendimiento Académico =====")
        analysis_standing = plot_academic_standing_distribution(df, os.path.join(output_dir, 'academic_standing.png'))
        print(analysis_standing)
        
        print("\n===== Generando GPA por Programa =====")
        analysis_gpa_program = plot_gpa_boxplot_by_program(df, os.path.join(output_dir, 'gpa_boxplot_by_program.png'))
        print(analysis_gpa_program)
        
        print("\n===== Generando Mapa de Calor de Correlación =====")
        correlation_matrix = get_correlation_matrix(df)
        analysis_correlation = plot_correlation_heatmap(correlation_matrix, os.path.join(output_dir, 'correlation_heatmap.png'))
        print(analysis_correlation)
        
        print(f"\nTodas las visualizaciones fueron guardadas en: {output_dir}")
        
    except Exception as e:
        print(f"Error al generar visualizaciones: {e}")
