:: Archivo que corre todos los comandos

@echo off
title run

:: -------------------------------------
:: Sobre directorios
:: FILES_INPUT: contiene a Rubrica.xlsx y Tarea_1.zip
:: FILES_OUTPUT: es creado
:: -------------------------------------
:: Constantes

:: set RUBRICA              = "Rubrica_T1"
set FILES_INPUT=files/
set FILES_OUTPUT=output/
set TAREA=Tarea_2
set REVISION_ESTUDIANTES=archivos_%TAREA% 

:: -------------------------------------
:: Comandos

:: Crea los directorios de los alumnos que subieron pdf con el pdf dentro y los deja en output/archivos_Tarea_1/
:: (OPCIONAL) echo python revision_alumnos %TAREA% --dir_in %FILES_INPUT% --dir_out %FILES_OUTPUT%
echo python revision_alumnos.py %TAREA%
python revision_alumnos.py %TAREA%
pause>nul|set/p =Siguiente script es read_pdf.py, presione cualquier tecla para continuar...
echo .
:: Busca la url del proyecto Github en los pdf de las tareas y descarga luego de entregarle la cuenta Github que tenemos
echo python read_pdf.py
python read_pdf.py
pause>nul|set/p =Siguiente script es revision_alumnos.py, presione cualquier teclas para continuar...
echo .
:: Descomprime los proyectos por cada directorio de los estudiantes
:: (OPCIONAL) echo python revision_alumnos master_project --dir_main %REVISION_ESTUDIANTES% --dir_in %FILES_INPUT% --dir_out %FILES_OUTPUT%
echo python revision_alumnos.py master_project --dir_main %REVISION_ESTUDIANTES%
python revision_alumnos.py master_project --dir_main %REVISION_ESTUDIANTES%
pause>nul|set/p =Siguiente script es generador_rubrica.py, presione cualquier teclas para continuar...
echo .
:: Crea los archivos txt de la Rubrica y los deja en output/comentarios/
:: echo python generador_rubrica.py
:: python generador_rubrica.py
:: pause>nul|set/p =Trabajo finalizado, presione alguna tecla para salir

exit

