from alpesonline.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from alpesonline.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from alpesonline.modulos.rutas.infraestructura.fabricas import FabricaRepositorio
from alpesonline.modulos.rutas.infraestructura.repositorios import RepositorioRutas
from alpesonline.modulos.rutas.dominio.entidades import Ruta
from alpesonline.modulos.rutas.infraestructura.dto import Ruta as RutaDTO

from alpesonline.seedwork.infraestructura.utils import millis_a_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod

class ProyeccionRuta(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionRutasLista(ProyeccionRuta):
    def __init__(self, id_ruta, id_cliente, estado, fecha_creacion, fecha_actualizacion):
        self.id_reserva = id
        self.id_cliente = id_cliente
        self.estado = estado
        self.fecha_creacion = millis_a_datetime(fecha_creacion)
        self.fecha_actualizacion = millis_a_datetime(fecha_actualizacion)
    
    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        
        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioRutas)
        
        repositorio.agregar(
            Ruta(
                id=str(self.id_reserva), 
                id_cliente=str(self.id_cliente), 
                estado=str(self.estado), 
                fecha_creacion=self.fecha_creacion, 
                fecha_actualizacion=self.fecha_actualizacion))
        
        db.session.commit()

class ProyeccionRutaHandler(ProyeccionHandler):
    
    def handle(self, proyeccion: ProyeccionRuta):
        from alpesonline.config.db import db
        proyeccion.ejecutar(db=db)
        

@proyeccion.register(ProyeccionRutasLista)
def ejecutar_proyeccion_ruta(proyeccion, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionRutaHandler()
            handler.handle(proyeccion)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
    