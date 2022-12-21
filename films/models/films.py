# -*- coding: utf-8 -*-
import requests
import base64

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class FilmsFind(models.Model):
    _name = 'films.select'
    _description = 'Select Film'

    name_russian = fields.Char(string="Name")
    year = fields.Char(string="Year")
    small_poster = fields.Char(string="Poster")
    description = fields.Text(string="Description")

    def name_get(self):
        return [(film.id, "%s" % film.name_russian) for film in self]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if not recs:
            recs = self.search([('year', operator, name)] + args, limit=limit)
        return recs.name_get()


class FilmsDetails(models.Model):
    _name = 'films.details'
    _description = 'Films Details'

    film_id = fields.Many2one('films', string='Film', required=True, index=True, copy=False)
    cinema_id = fields.Many2one('res.company', string='Cinema Reference', index=True, copy=False)
    user_id = fields.Many2one('res.users', string='User', required=True, index=True, copy=False)
    date_view = fields.Datetime(string='Viewing date', required=True)


class Films(models.Model):
    _name = 'films'
    _description = 'Films'

    name = fields.Char(string="Name", required=True, on_change="on_change_seq_choosed(seq_choosed)")
    year = fields.Char(string="Year")
    poster = fields.Binary(string="Poster", store=True)
    description = fields.Text(string="Description")

    film_select = fields.Many2one('films.select', 'Select film')

    def action_find_film(self):
        url = ("https://kinobd.net/api/films/search/title?q=%s" % self.name)
        response = requests.get(url)
        if response.ok:
            content = response.json()
        else:
            raise UserError('Response error!')

        if len(content['data']) == 0:
            raise UserError('No found films')
        elif len(content['data']) == 1:
            self.load_film(content['data'][0])
            return

        self.env['films.select'].search([]).unlink()
        for item in content['data']:
            self.env['films.select'].create({
                'name_russian': item['name_russian'],
                'year': item['year'],
                'small_poster': item['small_poster'],
                'description': item['description'],
            })

        action = self.env.ref('films.view_films_find_form')
        if not (action):
            raise ValidationError("Films Find Action not found!")

        return {
            'type': 'ir.actions.act_window',
            'name': action.name,
            'res_model': action.model,
            'view_id': action.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
        }

    def load_film(self, data):
        def get_image_from_url(url):
            data = ""
            try:
                data = base64.b64encode(requests.get(url.strip()).content).replace(b"\n", b"")
            except Exception:
                raise UserError("Can’t load the image from URL %s" % url)
            return data

        if not data:
            return

        film = self.env['films'].browse(self.env.context.get('active_id'))
        if film.exists():
            film.name = data['name_russian']
            film.year = data['year']
            #film.poster = get_image_from_url(data['small_poster'])
            film.description = data['description']

    def select_film(self):
        self.load_film(self.film_select)





