# Este archivo se debe ejecutar para poder subir el archivo a pypi

# Leer el contenido del archivo README.md 
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="everagm-hack4",
    version="0.1.0", # Si se sube otro archivo con el mismo nombre y la misma version no deja subirlo, aunque eliminemos el archivo.
    packages=find_packages(), # Permite buscar todos los paquetes disponiblles.
    install_requires=[],
    author="Ever Granadino",
    description="Una biblioteca para consultar cursos de hack4u.",
    long_description=long_description, # Equivale a la variable que definimos arriba. 
    long_description_content_type="text/markdown",
    url="https://hack4u.io",     
)