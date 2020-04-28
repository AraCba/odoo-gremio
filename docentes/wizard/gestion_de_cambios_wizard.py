from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.addons.docentes.models.base import Base
from odoo.addons.docentes.models.docentes import *
from odoo.addons.docentes.models.gestion_de_cambios import SITUACION

NONE = 'none'
NUEVO = 'nuevo'
HIST = 'hist'
BAJA = 'baja'
PEND_B = 'pend_b'
PEND_A = 'pend_a'
PASIVO = 'pasivo'
JUB = 'jub'
JUBA = 'juba'
ACTIVO = 'activo'
BECARIEA = 'becariea'
BECARIE = 'becarie'
CONTRATADEA = 'contratadea'
CONTRATADE = 'contratade'

## Sera usado para gestion_de_cambios_wizard, en vez de tener muchos ifs.
DOCENTE_APORTO = {
    NONE: 'NACA',
    BAJA: 'NACA',
    HIST: 'HCA',
    PASIVO: 'PCA',
    PEND_B: 'PBCA',
    PEND_A: 'PACA',
    JUB: 'JPCA',
    BECARIE: 'BPCA',
    CONTRATADE: 'CPCA'
}

DOCENTE_NO_APORTO = {
    ACTIVO: 'ASA',
    PEND_A: 'PASA',
    PEND_B: 'PBSA',
    JUBA: 'JASA',
    BECARIEA: 'BASA',
    CONTRATADEA: 'CASA'
}



class DocentesGestionDeCambioWiz(models.TransientModel):
    _name ='docentes.gestion.wizard'

    fecha_desde = fields.Date('Fecha desde',
                           help="Elegir la fecha desde la que se realiza la consulta",
                           default=fields.Datetime.now(),
                           required=True)
    fecha_hasta = fields.Date('Fecha hasta',
                           help="Elegir la fecha hasta la que se realiza la consulta",
                           default=fields.Datetime.now(),
                           required=True)

    fecha_consulta = fields.Date('Fecha de consulta',
                           default=fields.Datetime.now(),
                           required=True, 
                           readonly=True)

    descripcion = fields.Char('Descripción', 
                           help="Describir la consulta que permita identificar el período y si es de aportantes y/o no aportantes",
                           required=True)

    aportaron = fields.Boolean('¿Aportaron?', 
                           help="Incluir aquellos que aportaron y no deberían haber aportado",
                           required=True)

    no_aportaron = fields.Boolean('¿No Aportaron?',
                           help="Incluir aquellos que no aportaron y deberían haber aportado",
                           required=True)

    @api.multi
    @api.depends('fecha_desde', 'fecha_hasta')
    def set_situacion(self):
        if self.fecha_desde >= self.fecha_hasta :
            raise UserError("El campo Fecha desde debe ser menor que el campo Fecha hasta")

        result = False

        if self.no_aportaron :
            self.env.cr.execute("select calcularInconsistencias(%s, %s, %s, %s)", ('no_aporto', self.fecha_desde, self.fecha_hasta, self.descripcion))
            result = True if len(self.env.cr.fetchall()) >= 1 else result
            # self.env['docentes.gestion_de_cambios'].invalidate_cache()

        if self.aportaron:
            self.env.cr.execute("select calcularInconsistencias(%s, %s, %s, %s)", ('aporto', self.fecha_desde, self.fecha_hasta, self.descripcion))
            result = True if len(self.env.cr.fetchall()) >= 1 else result
            # self.env['docentes.gestion_de_cambios'].invalidate_cache()

        if not result :
            raise UserError("No hay docentes con posibles cambios entre esas fechas")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Gestión de cambios',
            'res_model': 'docentes.gestion_de_cambios',
            # 'res_id': id_ge.id,
            # 'taget': 'new',
            'views': [[False, 'tree']],
            'domain': [['descripcion', "=", self.descripcion]]
#            'view_mode': 'tree',
#            'view_type': 'tree'
        }

