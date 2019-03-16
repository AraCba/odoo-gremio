from odoo import api, fields, models, _


SITUACION = [
    ('ASA', 'Activo sin aportes'),
    ('PCA', 'Afiliade no cotizante con aportes'),
    ('NACA', 'No afiliade con aportes'),
    ('HCA', 'Histórico con aportes'),
    ('PASA', 'Pendiente de alta sin aportes'),
    ('PACA', 'Pendiente de alta con aportes'),
    ('PBSA', 'Pendiente de baja sin aportes'),
    ('PBCA', 'Pendiente de baja con aportes'),
    ('JPCA', 'Jubilade no cotizante con aportes'),
    ('JASA', 'Jubilade cotizante sin aportes'),
    ('BPCA', 'Becarie no cotizante con aportes'),
    ('BASA', 'Becarie cotizante sin aportes'),
    ('CPCA', 'Contratade no cotizante con aportes'),
    ('CASA', 'Contratade cotizante sin aportes'),
    ('OTRA', 'Otra situación')
]





class DocentesGestionDeCambio(models.Model):
    _name = 'docentes.gestion_de_cambios'
    _order = 'fecha_consulta desc, docente, situacion'

    fecha_desde = fields.Date('Fecha desde',
                                  readonly=True)
    fecha_hasta = fields.Date('Fecha hasta',
                                  readonly=True)

    fecha_consulta = fields.Date('Fecha de consulta',
                                  readonly=True)

    descripcion = fields.Char('Descripción', 
                                  readonly=True)


    docente = fields.Many2one('res.partner', 'Docente',
                                 required=True,
                                 ondelete='cascade',
                                 readonly=True
                                 )

    situacion = fields.Selection(SITUACION, 'Situación', readonly=True)

#    @api.multi
#    def crearDocente(self):
#        id_docente = self.docente.id
#        self.docente.update({'esdocente': True, 'estado':'none'})
#        return {
#            'type': 'ir.actions.act_window',
#            'name': 'Gestión de cambios',
#            'res_model': 'res.partner',
#            'res_id': id_docente,
#            # 'taget': 'new',
#            'view_mode': 'form',
#            'view_type': 'form'
#        }



