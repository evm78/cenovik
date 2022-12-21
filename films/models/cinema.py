# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Cinema(models.Model):
    # _name = 'cinema'
    _name = 'res.company'
    _inherit = 'res.company'
    _description = 'Cinema'

    name = fields.Char(related='partner_id.name', string='Cinema Name', required=True, store=True, readonly=False)
    film_details = fields.One2many('films.details', 'cinema_id', string='Films Details')



