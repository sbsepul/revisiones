"""
Modulo que transforma la rúbrica en excel en un formato fácil de pasar a u-cursos
"""
from typing import Tuple
from pathlib import Path

import os
import pandas as pd
from textwrap import wrap

# for .gitignore
DIRECTORY_OUTPUT = "output/"

DIRECTORY_TEST = "files/"

INDICE_NOMBRE_ALUMNO = 0
SECCIONES = ("Funcionalidad", "Diseño", "Código Fuente", "Coverage", "Javadoc", "Resumen")
NOTA = "Nota"
COMENTARIOS = ("Comentarios", "Corrector")
COVERAGE = "Porcentaje de coverage"
ROOT = Path(os.path.dirname(os.path.realpath(__file__)))
DIRECTORY_COMMENTS = "comentarios/"
SEC_ADICIONALES = "Adicionales"


def concat_test_dir(file):
    return f"{DIRECTORY_TEST}{file}"

def get_total(puntaje: str):
    """ Borra el substring `Total: ` del puntaje """
    return puntaje.replace("Total: ", "").replace(",", ".")

def excel_sheet(data, revision, nombre_alumno, nota) -> Tuple[str, str]:
    """ Convierte la rúbrica a una tupla fácil de pasar a un archivo .txt

    :param excel_filename: el nombre del excel con la rúbrica
    :return: una tupla con el nombre del alumno y los comentarios de revisión
    """
    value_item = 0
    for index, row in data.iterrows():
        if index == INDICE_NOMBRE_ALUMNO:
            nombre_alumno = f"{row[1]}"
        item = row[0]

        # Puntajes totales de las subsecciones
        if item in SECCIONES:
            value_item += 1
            item_count = 0
            if (item=="Código Fuente"):
                value_item -=1
                revision += "\n" + "#" * 80 + f"\n ↑↑↑ (Total items anteriores) {item}: {round(row[2], 2)} / {get_total(row[3])} ↑↑↑\n" + "#" * 80    
            else: 
                revision += "\n" + "=" * 80 + f"\n({value_item}) {item}: {round(row[2], 2)} / {get_total(row[3])}\n"
        # Nota final
        elif item == NOTA:
            nota = f"{row[3]}"
        # Notas del corrector
        elif item in COMENTARIOS:
            if(pd.isna(row[1])):
                revision += "#" * 80 +  f"\n{item}: No aplica"
            else:
                revision += f"\n{item}: {row[1]}"
        # Descuentos adicionales
        elif item == SEC_ADICIONALES:
            value_item += 1
            item_count = 0
            revision += "\n" + "=" * 80 + f"\n\n({value_item}) {item}: {row[2]}\n"
        # Detalle de los descuentos
        elif index > 1 and row[2] != 0:
            if item == COVERAGE:
                if row[3] != 0:
                    revision += f"\n{item}: {row[2] * 100}% = {row[3]}"
            else:
                item_count += 1
                revision += f"\n({value_item}.{item_count}) {row[0]}: {row[1]}x{row[2]} = {row[3]}"
                if (not pd.isna(row[4])):
                    separate = wrap(row[4], 60)
                else:
                    separate = ["No aplica"]
                detalle = separate[0] + "\n\t " + "\n\t ".join(separate[1:])
                revision += f"\nDetalle: {detalle}\n"
    if not nombre_alumno:
        print(f"Falta nombre del alumno en hoja {index+1}")
        #raise Exception("Falta nombre del alumno!!")
    return nombre_alumno, f"Alumno: {nombre_alumno}\nNota: {nota}\n\n{revision}"


def excel_a_string(excel_filename: str):
    """
       Lee cada hoja del excel de Rubrica para devolver una lista de tuplas
       las cuales permiten redactar un archivo txt por cada alumno
    """
    revision_alumno = []
    xl = pd.ExcelFile(excel_filename)
    for sheet in xl.sheet_names:
        revision = ""
        nombre_alumno = ""
        nota = ""
        df = xl.parse(sheet, header=None)
        nombre_alumno, revision = excel_sheet(df, revision, nombre_alumno, nota)
        revision_alumno.append([nombre_alumno, revision])
    return revision_alumno

if __name__ == '__main__':
    path_dir = f"{DIRECTORY_OUTPUT}{DIRECTORY_COMMENTS}"
    if not os.path.exists(os.path.dirname(path_dir)):
        try:
            os.makedirs(os.path.dirname(path_dir))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    ALUMNOS = excel_a_string(concat_test_dir("Rubrica_T1.xlsx"))
    for alumno in ALUMNOS:
        NOMBRE_ALUMNO, REVISION = alumno
        with open(f"{path_dir}{NOMBRE_ALUMNO}.txt", "w+",
                  encoding='utf-8') as comentarios_alumno:
            comentarios_alumno.write(REVISION)
