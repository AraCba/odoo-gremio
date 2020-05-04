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
from odoo.exceptions import Warning, ValidationError
#from odoo.addons.docentes.models.base import Base
from datetime import date

ESTADO_SOL = [
    ('sol', 'Solicitada'),
    ('aut', 'Autorizada'),
    ('rec', 'Rechazada'),
    #    (doc,'A la espera de documentación'),
    ('fin', 'Finalizada'),
    ('can', 'Cancelada')
]

# ESTADO_BOL = [
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
    ('inicial4', 'Inicial [Sala de 4 años]'),
    ('inicial5', 'Inicial [Sala de 5 años]'),
    ('primaria1', 'Primario [1º Grado]'),
    ('primaria2', 'Primario [2º Grado]'),
    ('primaria3', 'Primario [3º Grado]'),
    ('primaria4', 'Primario [4º Grado]'),
    ('primaria5', 'Primario [5º Grado]'),
    ('primaria6', 'Primario [6º Grado]'),
    ('secundariaR', 'Secundario [Rivadavia]'),
    ('secundariaO', 'Secundario [Oficio]'),
    ('secundariaA', 'Secundario [A4]'),
    ('universitario', 'Universitario'),
    ('otro', 'Otro')
]

est_solic = False
class DocentesSolicitudes(models.Model):
    """
    Solicitudes al gremio de docentes afiliados
    """
    _name = 'docentes.solicitudes'
    _order = 'fecha_sol desc, fecha_ult_estado desc, docente'
    _description = 'Modelo Solicitudes de servicios a afiliados'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    docente = fields.Many2one('res.partner',
                              string='Docente',
                              ondelete='cascade', 
                              required=True)
    docente_bis = fields.Many2one('docentes.docente', string='Docente_bis')

    # Este campo queda obsoleto
    estado = fields.Selection(ESTADO_SOL, 'Estado')

    fecha_sol = fields.Date('Fecha de solicitud', required=True, default=date.today(), readonly=True)
    fecha_ult_estado = fields.Date('Fecha de último estado', required=True, default=date.today(), readonly=True)
    doc_completa = fields.Boolean('Documentación completa')
    # expediente = fields.Integer('Expediente')
    # resolucion = fields.Integer('Resolución')
    observaciones = fields.Char('Observaciones')
    expediente_resolucion = fields.Char('Expediente/resolución')
    notas = fields.Text('Notas')

    # Este campo queda obsoleto
    tipo = fields.Selection(TIPO_SOL, 'Tipo de solicitud')

    bolsones = fields.One2many('docentes.bolsones', 'solicitud', string='Bolsones')
    state = fields.Selection([
            ('nue', 'Nueva'),
            ('sol', 'Solicitada'),
            ('aut', 'Autorizada'),
            ('rec', 'Rechazada'),
            ('fin', 'Finalizada'),
            ('can', 'Cancelada')
        ], 
        string='Estado', index=True, readonly=True, default='nue',
        track_visibility='onchange', copy=False)

    responsable = fields.Many2one('res.users',
                              string='Responsable',
                              required=True,
                              default=lambda self: self.env.uid)

    tipo_solicitud = fields.Many2one('docentes.tipo_solicitud', 
                        string='Tipo de solicitud')

    # Subsidios
    monto_sol = fields.Float('Monto solicitado')
    monto_aut = fields.Float('Monto autorizado')
    monto_ren = fields.Float('Monto rendido')
    monto_pag = fields.Float('Monto pagado')

    # Variables para ocultar / mostrar pestañas 
    mostrar_bolsones = fields.Boolean(string='ocultar_bolsones', 
                        compute="_onchange_tipo_solicitud", 
                        store = False)
    mostrar_subsidios = fields.Boolean(string='ocultar_bolsones', 
                        compute="_onchange_tipo_solicitud", 
                        store = False)
    mostrar_prestamos = fields.Boolean(string='ocultar_prestamos', 
                        compute="_onchange_tipo_solicitud", 
                        store = False)
    mostrar_notas = fields.Boolean(string='ocultar_notas', 
                        compute="_onchange_tipo_solicitud", 
                        store = False)

    @api.model
    def create(self, vals):
        vals['state'] = 'sol'
        solicitud = super(DocentesSolicitudes, self).create(vals)
        return solicitud

    @api.multi
    def write(self, vals):
        solicitud = super(DocentesSolicitudes, self).write(vals)
        return solicitud

    def autorizar(self):
        for record in self:
            groups = (self.tipo_solicitud.grupos+ '.')[:-1] #Creo una copia del valor
            groups = groups.split(',')
            if 'subsidios' in groups :
                if record.monto_aut <= 0 :
                    raise ValidationError('Monto autorizado debe ser mayor a 0')
            if 'bolsones' in groups :
                if len(record.bolsones) < 1 :
                    raise ValidationError('Debe existir al menos un bolsón')
            record.write({'state': 'aut', 'estado_anterior': self.state, 'fecha_ult_estado': date.today()})
        return
    
    def rechazar(self):
        for record in self:
            record.write({'state': 'rec', 'estado_anterior': self.state, 'fecha_ult_estado': date.today()})
        return

    def finalizar(self):
        for record in self:
            groups = (self.tipo_solicitud.grupos+ '.')[:-1] #Creo una copia del valor
            groups = groups.split(',')
            if 'subsidios' in groups :
                if record.monto_pag <= 0 or record.monto_pag > record.monto_aut :
                    raise ValidationError('Monto pagado debe ser mayor a 0 y menor o igual al monto autorizado')
            if not record.doc_completa : 
                raise ValidationError('Para finalizar la solicitud se debe tener la documentación completa')
            record.write({'state': 'fin', 'estado_anterior': self.state, 'fecha_ult_estado': date.today()})
        return

    def cancelar(self):
        for record in self:
            record.write({'state': 'can', 'estado_anterior': self.state, 'fecha_ult_estado': date.today()})
        return

    @api.onchange('tipo_solicitud')
    def _onchange_tipo_solicitud(self):
        if (self.tipo_solicitud.grupos) :
            groups = (self.tipo_solicitud.grupos+ '.')[:-1] #Creo una copia del valor
            groups = groups.split(',')
            
            # Por defecto 
            res = {'domain' : {'docente' : [('active', '=', True)],}}

            if self.tipo_solicitud.aplica_docente : 
                res['domain']['docente'].append(('esdocente', '=', True),)

            # Cuando un campo es computed no se debe usar la expresión write sobre él.
            # Se debe hacer campo = <algo>
            # Lo siguiente no funciona
            # self.write({
            #     'mostrar_bolsones': _mostrar_bolsones, 
            #     'mostrar_subsidios': _mostrar_subsidios,
            #     'mostrar_prestamos': _mostrar_prestamos,
            #     'mostrar_notas': _mostrar_notas
            # })
            self.mostrar_bolsones = True if 'bolsones' in groups else False
            self.mostrar_subsidios = True if 'subsidios' in groups else False
            self.mostrar_prestamos = True if 'prestamos' in groups else False
            self.mostrar_notas = True if 'notas' in groups else False

            return res

    @api.multi
    def message_get_suggested_recipients(self):
        recipients = super(DocentesSolicitudes, self).message_get_suggested_recipients()
        recipients[self.id].append((self.docente.id, self.docente.name, 'Solicitante'))
        return recipients


class DocentesBolsones(models.Model):
    """
    Gestión de bolsones escolares y por nacimiento para hijos de afiliades
    """

    _name = 'docentes.bolsones'
    _order = 'nivel'
    _description = 'Modelo para la entrega de bolsones a afiliados'

    solicitud = fields.Many2one(
        'docentes.solicitudes', string='Solicitud', ondelete='cascade')

    menor = fields.Many2one('docentes.hijos', 
        string='Menor', 
        domain="[('verificado','=', True)]")

    nivel = fields.Selection(TIPO_BOLSON, 'Bolsón', required=True)

    entregado = fields.Boolean('Entregado')

    solicitante = fields.Char(string='Solicitante', compute='_get_solicitante', store=False)

    @api.depends('solicitud')
    def _get_solicitante(self) :
        for record in self:
            record.solicitante = record.solicitud.docente.name
        return

    @api.model
    def create(self, vals):
        bolson = super(DocentesBolsones, self).create(vals)
        return bolson

    @api.onchange('solicitud')
    def _onchange_solicitud(self):
        res = {'domain' : {'menor' : [('verificado', '=', True)],}}

        hijos = self.solicitud.docente.hijo_id
        hijos_ids = []
        for hijo in hijos :
            hijos_ids.append(hijo.id)
        res['domain']['menor'].append(('id', 'in', hijos_ids),)

        return res

class OptionSelection(models.AbstractModel):
    _name = 'docentes.optionselection'
    _description = 'Modelo genérico para los opciones de los selectores'

    name = fields.Char('Nombre', required=True)
    activo = fields.Boolean('Activo', required=True, default=True)

    _sql_constraints = [('UN_OptSelection_name', 'UNIQUE (name)',
                         'Ya existe una opción con ese nombre')]

class TipoSolicitud(models.Model):
    _name = 'docentes.tipo_solicitud'
    _inherit = 'docentes.optionselection'
    _description = 'Modelo para los tipos de solicitud'

    grupos = fields.Char('Grupos', help="Escriba en minusculas y separado por comas el nombre de los grupos al que pertenece la solicitud. Evite los espacios")
    aplica_docente = fields.Boolean('Aplica a docente')

    @api.multi
    def write(self, vals):
        for record in self :
            # Borro los espacios en blanco de los grupos 
            _grupos = (vals['grupos']+ '.')[:-1] #Creo una copia del valor
            vals['grupos'] = _grupos.replace(" ", "")

        tipo = super(TipoSolicitud, self).write(vals)
        return tipo

# class CodigoAporte(models.Model):
#     _name = 'docentes.codigo_aporte'
#     _inherit = 'docentes.optionselection'

# class CategoriaAporte(models.Model):
#     _name = 'docentes.categoria_aporte'
#     _inherit = 'docentes.optionselection'

# class CaracterAporte(models.Model):
#     _name = 'docentes.caracter_aporte'
#     _inherit = 'docentes.optionselection'

# class DependenciaAporte(models.Model):
#     _name = 'docentes.dependencia_aporte'
#     _inherit = 'docentes.optionselection'

# class SubdependenciaAporte(models.Model):
#     _name = 'docentes.subdependencia_aporte'
#     _inherit = 'docentes.optionselection'