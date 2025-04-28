### ESTE ARCHIVO ES EL QUE DEFINE QUE DIRECTORIO ES UN PAQUETE.

# Le digo que a la hora de importar el paquete (from hack4u o import)  quiero hacer lo siguiente.-
# Al hacer eso puedo hacer lo siguiente:
# from hack4u import list_courses --> Sin tener que poner from hack4u.courses
from .courses import *

# De la misma forma al hacer un from 'este_paquete' hacer lo siguiente. 
from .utils import *