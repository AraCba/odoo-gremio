from odoo import api, fields, models, _


class TipoCargo(models.Model) : 
  _name = 'docentes.tipo.cargo'
  _rec_name = 'codigo'

  horas = fields.Boolean(string="Es por horas", required=True)
  codigo = fields.Char(string="Código", required=True)
  name = fields.Char(string="Descripción", required=True)
  dedicacion = fields.Char(string="Dedicación", required=True)

class CaracterCargo(models.Model) :
  _name = 'docentes.caracter.cargo'
  _rec_name = 'codigo'

  codigo = fields.Char(string="Código", required=True)
  name = fields.Char(string="Descripción", required=True)

class EtiquetaCargo(models.Model) :
  _name = 'docentes.etiqueta.cargo'

  name = fields.Char(string="Nombre", required=True)

class DependenciaCargo(models.Model) :
  _name = 'docentes.dependencia.cargo'
  _rec_name = 'codigo'

  codigo = fields.Char(string="Código", required=True)
  name = fields.Char(string="Descripción", required=True)
  padre = fields.Many2one('docentes.dependencia.cargo', string='Padre')

class Cargo(models.Model) :
  _name = 'docentes.cargo'

  tipo_cargo = fields.Many2one('docentes.tipo.cargo', string='Tipo')
  nro_cargo = fields.Char(string="Número de cargo", help="Se corresponde con el número del sistema universitario")
  cant_horas = fields.Integer(string="Cantidad de horas")
  caracter = fields.Many2one('docentes.caracter.cargo', string='Caracter')
  dependencia = fields.Many2one('docentes.dependencia.cargo', string='Dependencia')
  etiqueta = fields.Many2many(
        'docentes.etiqueta.cargo', 'docente_etiqueta_cargo_rel', 'cargo_id', 'etiqueta_cargo_id',
        string='Etiquetas')
  # docente = fields.Many2one('res.partner', string='Docente')
  docente = fields.Many2one('docentes.docente', string='Docente', required=True)
