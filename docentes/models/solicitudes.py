# -*- coding: utf-8 -*-
##############################################################################
#
#    Módulo Docentes para Odoo
#    Copyright (C) Araceli Acosta
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, _
#from odoo.addons.docentes.models.base import Base

ESTADO_SOL = [
    ('sol','Solicitada'),
    ('aut','Autorizada'),
    ('rec','Rechazada'),
#    (doc,'A la espera de documentación'),
    ('fin','Finalizada'),
    ('can','Cancelada')
    ]

#ESTADO_BOL = [
#    (sol,'Solicitado'),
#    (aut,'Autorizado'),
#    (rec,'Rechazado'),
#    (doc,'A la espera de documentación'),
#    (fin,'Entregado'),
#    (can,'Cancelado'),
#    ]

TIPO_SOL = [
    ('bol_esc', 'Bolsones escolares'),
    ('bol_nac', 'Bolsones por nacimiento'),
    ('sub_aca', 'Subsidios para actividades académicas y gremiales'),
    ('sub_col', 'Subsidios para actividades colectivas'),
    ('sub_ext', 'Subsidios extraordinarios'), 
    ('sub_esc', 'Subsidio escolar por discapacidad'),
    ('viatico', 'Reintegro de viáticos veeduria')
    ]

TIPO_BOLSON = [
    ('nacimiento', 'Nacimiento'),
    ('inicial4','Inicial [Sala de 4 años]'),
    ('inicial5','Inicial [Sala de 5 años]'),
    ('primaria1','Primario [1º Grado]'),
    ('primaria2','Primario [2º Grado]'),
    ('primaria3','Primario [3º Grado]'),
    ('primaria4','Primario [4º Grado]'),
    ('primaria5','Primario [5º Grado]'),
    ('primaria6','Primario [6º Grado]'),
    ('secundariaR','Secundario [Rivadavia]'),
    ('secundariaO','Secundario [Oficio]'),
    ('secundariaA','Secundario [A4]'),
    ('universitario','Universitario'),
    ('otro','Otro')
    ]
    
class DocentesSolicitudes(models.Model):
    """
    Solicitudes al gremio de docentes afiliados
    """
    _name = 'docentes.solicitudes'
    _order = 'fecha_sol desc, fecha_ult_estado desc, docente'
    _description = 'Modelo Solicitudes de servicios a afiliados'

    docente = fields.Many2one('res.partner',
        string='Docente',
        ondelete='cascade',  required=True)

    estado = fields.Selection(ESTADO_SOL, 'Estado', required=True)
##    fecha_sol = fields.Date('Fecha de solicitud', readonly=True, required=True)
##    fecha_ult_estado = fields.Date('Fecha de último estado', readonly=True, required=True)
    fecha_sol = fields.Date('Fecha de solicitud', required=True)
    fecha_ult_estado = fields.Date('Fecha de último estado', required=True)
    doc_completa = fields.Boolean('Documentación completa')
    expediente = fields.Integer('Expediente')
    resolucion = fields.Integer('Resolución')
    observaciones = fields.Char('Observaciones')
    tipo = fields.Selection(TIPO_SOL, 'Tipo de solicitud', required=True)

    bolsones = fields.One2many('docentes.bolsones', 'solicitud', string='Bolsones')

#Subsidios 
    monto_sol = fields.Float('Monto solicitado')
    monto_aut = fields.Float('Monto autorizado')
    monto_ren = fields.Float('Monto rendido')


class DocentesBolsones(models.Model):
    """
    Gestión de bolsones escolares y por nacimiento para hijos de afiliades
    """
    _name = 'docentes.bolsones'
    _order = 'nivel'
    _description = 'Modelo para la entrega de bolsones a afiliados'


    solicitud = fields.Many2one('docentes.solicitudes', string='Solicitud', ondelete='cascade')

    menor = fields.Many2one('docentes.hijos', string='Menor')

    nivel = fields.Selection(TIPO_BOLSON, 'Bolsón', required=True)

    entregado = fields.Boolean('Entregado')




