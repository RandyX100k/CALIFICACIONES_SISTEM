from flask import render_template

class Cursos():
    def __init__(self,app):
        self.app = app
    def Curso_template(self,template,**kwargs):
        return render_template(template,**kwargs)