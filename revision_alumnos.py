'''
	Con el siguiente comando se crean directorios según
	archivo zip de archivos de alumnos:

	revision_alumnos -rz <file.zip>

	Además se crea un archivo json que contendrá:

	Alumnos: {
		name_alumno: <str>,
		comentario: <str>
	}

'''

import argparse
import zipfile as zf
import os
from os import listdir

# for .gitignore
DIRECTORY_OUTPUT = "output/"

def get_args():
	parser = argparse.ArgumentParser(description='Unzip in directories the files in zip.')
	parser.add_argument('file', help='file zip that will be unzippped')
	parser.add_argument('--dir_out', default=None,
                    help='directory output where zip that will be unzippped')
	parser.add_argument('--dir_in', default=None,
                    help='directory input where is the file zip')
	parser.add_argument('--dir_main', default=None,
                    help='directory of students')
	return parser.parse_args()


'''
Verifica si un directorio existe, si no es asi lo crea
'''
def create_dir(path):
	if not os.path.exists(os.path.dirname(path)):
		try:
			os.makedirs(os.path.dirname(path))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise


'''
Descomprime un zip y por cada archivo crea un directorio con el nombre del archivo

'''
def unzip_file(file_zip, dir_out, dir_in):
	dirout = dir_out if(dir_out) else f"{DIRECTORY_OUTPUT}archivos_{file_zip}/"
	dirin = dir_in if(dir_in) else f"files/"
	file = f"{dirin}{file_zip}.zip"
	with zf.ZipFile(file, 'r') as zip_ref:
		for pdf_file in zip_ref.namelist():
			student = os.path.splitext(pdf_file)[0]
			directory_student = f"{student}/"
			path = f"{dirout}{directory_student}"
			create_dir(path)
			zip_ref.extract(pdf_file, path)

def unzip_in_drectory(file_zip, directory_main):
	dir_all_students = f"{DIRECTORY_OUTPUT}{directory_main}"
	directories = [f for f in listdir(dir_all_students)]
	for student_dir in directories:
		check_student = False
		full_path = f"{dir_all_students}/{student_dir}/"
		for file in listdir(full_path):
			if(file.endswith(".zip")):
				check_student = True
				full_file = f"{full_path}{file}"
				try:
					with zf.ZipFile(full_file, 'r') as zip_ref:
						zip_ref.extractall(full_path)
				except:
					next
		if(not check_student):
			print(f"{student_dir[:-1]} falta")

if __name__ == '__main__':
	args = get_args()
	if(args.dir_main):
		unzip_in_drectory(args.file, args.dir_main)
	else:
		unzip_file(args.file, args.dir_out, args.dir_in)