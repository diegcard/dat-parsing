"""
Script principal para el análisis de datos universitarios.
Orquesta todo el flujo de análisis, desde la carga de datos hasta la generación de visualizaciones y resultados.
"""
import os
import argparse
import sys
import pandas as pd
from datetime import datetime

# Importar módulos del proyecto
from src.data_loader import load_university_data
from src.data_processor import preprocess_data, validate_data
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
from src.plotting import (
    plot_gpa_distribution,
    plot_students_per_program,
    plot_gpa_vs_credits,
    plot_scholarship_status,
    plot_academic_standing_distribution,
    plot_gpa_boxplot_by_program,
    plot_correlation_heatmap
)


def parse_arguments():
    """
    Parsea los argumentos de línea de comandos.
    
    Returns:
        argparse.Namespace: Argumentos parseados.
    """
    parser = argparse.ArgumentParser(description='Análisis de datos universitarios')
    
    parser.add_argument(
        '--data', 
        type=str, 
        default=os.path.join('data', 'university_data.csv'),
        help='Ruta al archivo CSV con los datos universitarios (default: data/university_data.csv)'
    )
    
    parser.add_argument(
        '--output', 
        type=str, 
        default=os.path.join('output'),
        help='Directorio donde guardar los resultados (default: output/)'
    )
    
    parser.add_argument(
        '--report', 
        action='store_true',
        help='Generar un reporte en formato markdown (default: False)'
    )
    
    return parser.parse_args()


def generate_report(analyses, output_dir):
    """
    Genera un reporte en formato markdown con los análisis de las visualizaciones.
    
    Args:
        analyses (dict): Diccionario con los análisis de las visualizaciones.
        output_dir (str): Directorio donde guardar el reporte.
    """
    report_path = os.path.join(output_dir, 'analysis_report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('# Reporte de Análisis de Datos Universitarios\n\n')
        f.write(f'*Generado el {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}*\n\n')
        
        f.write('## Resumen Ejecutivo\n\n')
        f.write('Este reporte presenta un análisis completo de los datos universitarios, ')
        f.write('incluyendo estadísticas descriptivas y visualizaciones que exploran ')
        f.write('las relaciones entre variables clave como el GPA, los créditos ')
        f.write('aprobados, el programa académico y el estado de becas.\n\n')
        
        f.write('## Análisis de Visualizaciones\n\n')
        
        for title, analysis in analyses.items():
            f.write(f'### {title}\n\n')
            f.write(f'![{title}](../{os.path.relpath(analysis["image_path"], output_dir)})\n\n')
            f.write(f'{analysis["text"]}\n\n')
        
        f.write('## Conclusiones\n\n')
        f.write('- Los datos muestran patrones interesantes en términos de rendimiento académico y su relación con otras variables.\n')
        f.write('- Se observa una clara distribución de estudiantes entre diferentes programas académicos.\n')
        f.write('- El estatus de beca parece tener una relación con el rendimiento académico de los estudiantes.\n')
        f.write('- Se recomiendan análisis adicionales para explorar las causas de las diferencias observadas en el rendimiento académico entre programas.\n')
    
    print(f"Reporte generado: {report_path}")


def main():
    """
    Función principal que orquesta todo el flujo de análisis.
    """
    # Parsear argumentos
    args = parse_arguments()
    
    # Configurar directorios
    data_path = args.data
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Usando datos de: {data_path}")
    print(f"Guardando resultados en: {output_dir}")
    
    try:
        # Cargar datos
        print("\n=== Cargando datos ===")
        df = load_university_data(data_path)
        print(f"Datos cargados exitosamente. Shape: {df.shape}")
        
        # Procesar datos
        print("\n=== Procesando datos ===")
        processed_df = preprocess_data(df)
        print(f"Datos procesados exitosamente. Shape: {processed_df.shape}")
        
        # Validar datos
        problems = validate_data(processed_df)
        if problems:
            print("\n=== Problemas encontrados en los datos ===")
            for problem in problems:
                print(f"- {problem}")
        else:
            print("\nNo se encontraron problemas en los datos.")
        
        # Análisis descriptivo
        print("\n=== Análisis Descriptivo ===")
        desc_stats = get_descriptive_statistics(processed_df)
        print(desc_stats)
        
        # Guardar estadísticas descriptivas
        desc_stats_path = os.path.join(output_dir, 'descriptive_statistics.csv')
        desc_stats.to_csv(desc_stats_path)
        print(f"Estadísticas descriptivas guardadas en: {desc_stats_path}")
        
        # Análisis de variables categóricas
        print("\n=== Distribución por Programa ===")
        program_counts = get_value_counts(processed_df, 'program')
        print(program_counts.head(10))
        
        print("\n=== Distribución por Género ===")
        gender_counts = get_value_counts(processed_df, 'gender')
        print(gender_counts)
        
        print("\n=== Distribución por Estado Académico ===")
        standing_counts = get_value_counts(processed_df, 'academic_standing')
        print(standing_counts)
        
        # Matriz de correlación
        print("\n=== Matriz de Correlación ===")
        correlation_matrix = get_correlation_matrix(processed_df)
        print(correlation_matrix)
        
        # Análisis agrupados
        print("\n=== GPA por Programa ===")
        gpa_by_program = analyze_gpa_by_program(processed_df)
        print(gpa_by_program.head(10))
        
        print("\n=== Distribución de Becas por Género ===")
        scholarship_by_gender = analyze_scholarship_distribution(processed_df, 'gender')
        print(scholarship_by_gender)
        
        print("\n=== Créditos por Semestre ===")
        credits_by_semester = analyze_credits_by_semester(processed_df)
        print(credits_by_semester)
        
        # Generar visualizaciones
        print("\n=== Generando Visualizaciones ===")
        
        # Diccionario para almacenar análisis para el reporte
        analyses = {}
        
        # 1. Distribución de GPA
        print("Generando visualización 1: Distribución de GPA")
        gpa_dist_path = os.path.join(output_dir, 'gpa_distribution.png')
        gpa_dist_analysis = plot_gpa_distribution(processed_df, gpa_dist_path)
        analyses["Distribución de GPA"] = {
            "image_path": gpa_dist_path,
            "text": gpa_dist_analysis
        }
        
        # 2. Estudiantes por Programa
        print("Generando visualización 2: Estudiantes por Programa")
        students_program_path = os.path.join(output_dir, 'students_per_program.png')
        students_program_analysis = plot_students_per_program(processed_df, students_program_path)
        analyses["Estudiantes por Programa"] = {
            "image_path": students_program_path,
            "text": students_program_analysis
        }
        
        # 3. GPA vs Créditos
        print("Generando visualización 3: GPA vs Créditos Aprobados")
        gpa_credits_path = os.path.join(output_dir, 'gpa_vs_credits.png')
        gpa_credits_analysis = plot_gpa_vs_credits(processed_df, gpa_credits_path)
        analyses["GPA vs Créditos Aprobados"] = {
            "image_path": gpa_credits_path,
            "text": gpa_credits_analysis
        }
        
        # Visualizaciones adicionales
        
        # 4. Distribución de Becas
        print("Generando visualización 4: Distribución de Becas")
        scholarship_path = os.path.join(output_dir, 'scholarship_status.png')
        scholarship_analysis = plot_scholarship_status(processed_df, scholarship_path)
        analyses["Distribución de Becas"] = {
            "image_path": scholarship_path,
            "text": scholarship_analysis
        }
        
        # 5. Distribución de Rendimiento Académico
        print("Generando visualización 5: Distribución de Rendimiento Académico")
        standing_path = os.path.join(output_dir, 'academic_standing.png')
        standing_analysis = plot_academic_standing_distribution(processed_df, standing_path)
        analyses["Distribución de Rendimiento Académico"] = {
            "image_path": standing_path,
            "text": standing_analysis
        }
        
        # 6. GPA por Programa
        print("Generando visualización 6: GPA por Programa")
        gpa_program_path = os.path.join(output_dir, 'gpa_boxplot_by_program.png')
        gpa_program_analysis = plot_gpa_boxplot_by_program(processed_df, gpa_program_path)
        analyses["GPA por Programa"] = {
            "image_path": gpa_program_path,
            "text": gpa_program_analysis
        }
        
        # 7. Mapa de Calor de Correlación
        print("Generando visualización 7: Mapa de Calor de Correlación")
        correlation_path = os.path.join(output_dir, 'correlation_heatmap.png')
        correlation_analysis = plot_correlation_heatmap(correlation_matrix, correlation_path)
        analyses["Mapa de Calor de Correlación"] = {
            "image_path": correlation_path,
            "text": correlation_analysis
        }
        
        print(f"\nTodas las visualizaciones fueron guardadas en: {output_dir}")
        
        # Generar reporte si se solicitó
        if args.report:
            print("\n=== Generando Reporte ===")
            generate_report(analyses, output_dir)
        
        print("\n=== Análisis Completado ===")
        print(f"Todos los resultados han sido guardados en: {output_dir}")
        
    except Exception as e:
        print(f"Error durante el análisis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
