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
from odoo.addons.smile_log.tools import SmileDBLogger 

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

    docente = fields.Many2one('res.partner',
                              string='Docente',
                              ondelete='cascade', 
                              required=True)

    # Este campo queda obsoleto
    estado = fields.Selection(ESTADO_SOL, 'Estado')

    fecha_sol = fields.Date('Fecha de solicitud', required=True, default=date.today(), readonly=True)
    fecha_ult_estado = fields.Date('Fecha de último estado', required=True, default=date.today(), readonly=True)
    doc_completa = fields.Boolean('Documentación completa')
    expediente = fields.Integer('Expediente')
    resolucion = fields.Integer('Resolución')
    observaciones = fields.Char('Observaciones')

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
    estado_anterior = fields.Char(string='estado_anterior', 
                        compute="_onchange_state", 
                        store = False)

    def _logAction(self, json):
        logger = SmileDBLogger(self._cr.dbname, 'docentes.solicitudes', self.id, self._uid)
        json.update({'user_id':self.env.uid}) 
        logger.info(_(json))
        return

    @api.model
    def create(self, vals):
        vals['state'] = 'sol'
        solicitud = super(DocentesSolicitudes, self).create(vals)
        # solicitud.state = 'sol'
        return solicitud

    @api.model
    def write(self, vals):
        if ('state' in vals.keys()) :
            logjson = {'oldstate':{'state':self.state}, 'newstate':{'state':vals['state']}}
            self._logAction(logjson)
            # Acá se debe enviar el mail
        solicitud = super(DocentesSolicitudes, self).write(vals)
        return solicitud

    def autorizar(self):
        for record in self:
            self._onchange_state()
            record.write({'state': 'aut', 'fecha_ult_estado': date.today()})
        return
    
    def rechazar(self):
        for record in self:
            self._onchange_state()
            record.write({'state': 'rec', 'fecha_ult_estado': date.today()})
        return

    def finalizar(self):
        for record in self:
            self._onchange_state()
            record.write({'state': 'fin', 'fecha_ult_estado': date.today()})
        return

    def cancelar(self):
        for record in self:
            self._onchange_state()
            record.write({'state': 'can', 'fecha_ult_estado': date.today()})
        return

    # @api.depends('state')
    def _onchange_state(self) :
        self.estado_anterior = self.state

    @api.one
    @api.constrains('monto_sol', 'monto_aut', 'monto_ren', 'monto_pag')
    def _validar_montos(self):
        if self.monto_sol > self.monto_aut :
            raise ValidationError('Monto solicitado hhhh es mayor al monto autorizado')
        if self.monto_ren > self.monto_aut :
            raise ValidationError('Monto rendido es mayor al monto autorizado')
        if self.monto_pag > self.monto_aut :
            raise ValidationError('Monto pagado es mayor al monto autorizado')

    @api.onchange('monto_sol', 'monto_aut', 'monto_ren', 'monto_pag')
    def _onchange_monto(self):
        if self.monto_sol > self.monto_aut :
            raise Warning(_('Monto solicitado es mayor al monto autorizado'))
        if self.monto_ren > self.monto_aut :
            raise Warning(_('Monto rendido es mayor al monto autorizado'))
        if self.monto_pag > self.monto_aut :
            raise Warning(_('Monto pagado es mayor al monto autorizado'))

    def _notificar_cambio_estado(self) :
        template_id = self.env.ref("docentes.solicitud_nuevo_estado_email_template").id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        

    @api.onchange('tipo_solicitud')
    def _onchange_tipo_solicitud(self):
        if (self.tipo_solicitud.grupos) :
            groups = (self.tipo_solicitud.grupos+ '.')[:-1] #Creo una copia del valor
            groups = groups.split(',')
            
            # Por defecto 
            self.mostrar_bolsones =  False
            self.mostrar_subsidios = False
            res = {'domain' : {'docente' : [('active', '=', True)],}}

            if ("bolsones" in groups) :
                self.mostrar_bolsones = True
                res['domain']['docente'].append(('esdocente', '=', True))

            if ("subsidios" in groups) :
                self.mostrar_subsidios = True

            return res

class DocentesBolsones(models.Model):
    """
    Gestión de bolsones escolares y por nacimiento para hijos de afiliades
    """
    _name = 'docentes.bolsones'
    _order = 'nivel'
    _description = 'Modelo para la entrega de bolsones a afiliados'
    solicitud = fields.Many2one(
        'docentes.solicitudes', string='Solicitud', ondelete='cascade')

    menor = fields.Many2one('docentes.hijos', string='Menor')

    nivel = fields.Selection(TIPO_BOLSON, 'Bolsón', required=True)

    entregado = fields.Boolean('Entregado')

class TipoSolicitud(models.Model):
    _name = 'docentes.tipo_solicitud'
    _description = 'Modelo para los tipos de solicitud'

    name = fields.Char('Nombre', required=True)
    activo = fields.Boolean('Activo', required=True, default=True)
    grupos = fields.Char('Grupos', help="Escriba en minusculas y separado por comas el nombre de los grupos al que pertenece la solicitud. Evite los espacios")

    _sql_constraints = [('UN_TipoSolicitud_name', 'UNIQUE (name)', 'Ya existe un tipo de solicitud con ese nombre')]

    @api.multi
    def write(self, vals):
        for record in self :
            # Borro los espacios en blanco de los grupos 
            _grupos = (vals['grupos']+ '.')[:-1] #Creo una copia del valor
            vals['grupos'] = _grupos.replace(" ", "")

        tipo = super(TipoSolicitud, self).write(vals)
        return tipo
