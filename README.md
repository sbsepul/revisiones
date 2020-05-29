# Revisiones

Los directorios que se utilizan son 

* `files/`: Guardar `Rubrica_T?.xlsx` y el `.zip`  que contiene los archivos `.pdf`

* `output/` : Lugar donde se guardarán los comentarios escritos en `Rubrica_T?.xlsx` y los directorios con los `.pdf` de cada alumno

Los comandos para la creación de output son los siguientes:

`revision_alumno.py`:

```bash
python revision_alumno -h 		# muestra ayuda
python revision_alumno archivo_pdfs.zip		# archivo_pdfs es un ejemplo depende de como lo hayan descargado
```

`generador_rubrica.py`:

```
python generador_rubrica.py 
```

`read_pdf.py`:

Ejecutar despues de:

```bash
python revision_alumno archivo_pdfs.zip
```

una vez creados los directorios, queremos descargar los proyectos, eso se hace con el siguiente comando:

```
python read_pdf.py
```

Va a solicitar la cuenta y clave de Github. No hay problema en autentificación, entonces continua.

y luego queremos descomprimirlos. Eso se hace con:

```
python revision_alumnos.py master_project --dir_main archivos_Tarea_1
```

(archivos_<algo_mas>) es el nombre por defecto. Tarea_1 era el nombre del archivo zip que se descargó en ucursos.

Finalmente hay que revisar quienes faltan, que son los directorios que se imprimieron en pantalla.

​	