# -*- coding: utf-8 -*-
##############################################################################
#
#    Módulo Docentes para Odoo
#    Copyright (C) Jonathan Mutal, Araceli Acosta
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
from odoo.addons.docentes.models.base import Base

TIPO_APORTE = [
    ('640', 'Descuento cod 640'),
    ('ACT', 'Cuota activo manual'),
    ('JUB', 'Cuota jubilade'),
    ('BEC', 'Cuota becarie'),
    ('CON', 'Cuota contratade'),
    ('OTR', 'Otros aportes')
]


class DocentesAportes(models.Model):
    """
    Aportes de docentes afiliados
    """
    _name = 'docentes.aportes'
    _order = 'fecha desc, nombre, codigo'
    _description = 'Modelo para los aportes'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    docente = fields.Many2one('res.partner',
        string='Docente',
        ondelete='cascade')
    # docente_bis = fields.Many2one('docentes.docente',
    #     string='Docente',
    #     ondelete='cascade')
    legajo = fields.Integer('Legajo', required=True)
    nombre = fields.Char('Nombre', size=30, required=True)
    cuil = fields.Char('Cuil')
    fecha = fields.Date('Fecha', required=True)
    codigo = fields.Selection(TIPO_APORTE,'Codigo')
    codigo_bis = fields.Many2one('docentes.codigo.aporte', string='Código_bis')
    aporte = fields.Float('Aporte', required=True)

    @api.model
    @api.depends('docente','legajo', 'nombre', 'fecha')
    def create(self, vals={}):
        """
        Override the create's method
        """

        docentes = Base(self.env['res.partner'])

        if 'docente' in vals:
            docente_dic = {
                'id': vals['docente']
            }
            docente = docentes.get(docente_dic)

            vals.update({
                'nombre': docente.name,
                'legajo': docente.legajo
                })
        
        # Se esta creando por importacion
        else:
            partner = self.env['res.partner'].search([['legajo','=',vals['legajo']]])
            if partner.id == 0 :
                docente = {'legajo': vals['legajo'], 'name': vals['nombre'], 'estado': 'nuevo', 'esdocente': True}
                if 'cuil' in vals:
                    docente.update({'vat': vals['cuil']})
                partner = self.env['res.partner'].create(docente)

            vals.update({'docente': partner.id})

        aporte = Base(self.env['docentes.aportes']).get(vals)

        if aporte:
            return super(DocentesAportes, self)

        return super(DocentesAportes, self).create(vals)

class CodigoAporte(models.Model) :
    _name = 'docentes.codigo.aporte'
    _rec_name = 'codigo'

    codigo = fields.Char(string='Codigo', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    activo = fields.Boolean(string='Activo', default=True)