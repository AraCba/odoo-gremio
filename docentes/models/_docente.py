from odoo import api, fields, models, _


class Docente(models.Model):
    _name = 'docentes.docente'
    _inherits = {'res.partner': 'partner_id'}
    _rec_name = 'legajo' # Para que funcionen las importaciones que enlazan por legajo

    legajo = fields.Char(string='legajo', required=True)

    _sql_constraints = [('UN_docente_legajo', 'UNIQUE (legajo)',
                         'Ya existe un legajo con ese valor')]

    @api.multi
    def name_get(self):
        result = []
        for record in self :
            # Si estoy importando por csv, entonces busco por legajo
            if 'import_file' in self.env.context :
                result.append((record.id, record.legajo))
            else :
                result.append((record.id, record.name))

        return result

    # @api.model
    # def create(self, vals):
    #     if 'esdocente' not in vals :
    #         vals.update({'esdocente': True})
    #     else :
    #         vals['esdocente'] = True
    #     docente = super(Docente, self).create(vals)
    #     return docente
