class Course:
    def __init__(self, name, duration, link):
        self.__name = name
        self.__duration = duration
        self.__link = link
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name
    
    @property
    def duration(self):
        return self.__duration
    
    @duration.setter
    def duration(self, duration):
        self.__duration = duration
    
    @property
    def link(self):
        return self.__link
    
    @link.setter
    def link(self, link):
        self.__link = link
        
    # Se puede ver la información del objeto en una lista de objetos.
    def __repr__(self):
        return f"{self.__name} [{self.__duration} horas] ({self.__link})]"

        

# Se crea una lista con 3 objetos temporales. 
courses = [
    Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalización de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Course("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/")   
]
def list_courses():
    return courses
        
def search_course_by_name(name):
    for course in courses:
        if course.name == name :
            return course
        
    return None
        