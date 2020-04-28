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
    docente_bis = fields.Many2one('docentes.docente',
        string='Docente',
        ondelete='cascade')
    legajo = fields.Integer('Legajo', required=True)
    nombre = fields.Char('Nombre', size=30, required=True)
    cuil = fields.Char('Cuil')
    fecha = fields.Date('Fecha', required=True)
    codigo = fields.Selection(TIPO_APORTE,'Codigo', required=True)
    aporte = fields.Float('Aporte', required=True)

    # codigo_aporte = fields.Many2one('docentes.codigo_aporte', string='Codigo de aporte')
    # categoria_aporte = fields.Many2one('docentes.categoria_aporte', string='Categoria del aporte')
    # caracter_aporte = fields.Many2one('docentes.caracter_aporte', string='Caracter del aporte')
    # dependencia_aporte = fields.Many2one('docentes.dependencia_aporte', string='Dependencia del aporte')
    # subdependencia_aporte = fields.Many2one('docentes.subdependencia_aporte', string='Subdependencia del aporte')

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

        else:
            docente_dic = {
                'legajo': vals['legajo']
            }

            if vals['cuil']:
               docente = docentes.get_create(
                    objeto_dic=docente_dic,
                    estado='nuevo',
                    name=vals['nombre'],
                    vat=vals['cuil']
                    )
            else:
                docente = docentes.get_create(
                    objeto_dic=docente_dic,
                    estado='nuevo',
                    name=vals['nombre']
                    )

            vals.update({
                'docente': docente.id,
                })

        aporte = Base(self.env['docentes.aportes']).get(vals)

        if aporte:
            return super(DocentesAportes, self)

        return super(DocentesAportes, self).create(vals)

