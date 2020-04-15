# -*- coding: utf-8 -*-
##############################################################################
#
#    Módulo Docentes para Odoo
#    Copyright (C) Araceli Acosta.
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


{
    'name': 'Docentes',
    'version': '2.2.2',
    'category': 'Asociacion',
    'summary': """Docentes y Afiliados""",

    'description': """
Este módulo permite gestionar Docentes y Afiliados de una asociación.
=========================================================================

Incorpora nueva información a la categoría Partner y menúes específicos para filtar la información. También incorpora operaciones para gestionar los aportes y solicitudes de bolsones y subsidios. 
    """,
    'author': "Araceli Acosta, Jonathan Mutal, Mauricio Clerici",
    'depends': ['base','smile_log','mail','portal'],
    'data': [
        'security/docentes_security.xml',
        'views/docentes_view.xml',
        'views/docentes_mails_view.xml',
        'views/aportes_view.xml',
        'views/hijos_view.xml',
        'views/solicitudes_view.xml',
        'views/tipo_solicitud_view.xml',
        'views/gestion_de_cambios_view.xml',
        'views/docentes_altas_view.xml',
        'data/email_template.xml',
        'wizard/gestion_de_cambios_wizard_view.xml',
        
    ],
    'application': True,
}

