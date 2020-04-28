from odoo import api, fields, models, _


class Docente(models.Model):
    _name = 'docentes.docente'
    _inherits = {'res.partner': 'partner_id'}

    legajo = fields.Char(string='legajo', required=True)

    _sql_constraints = [('UN_docente_legajo', 'UNIQUE (legajo)',
                         'Ya existe un legajo con ese valor')]
