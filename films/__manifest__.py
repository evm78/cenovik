# -*- coding: utf-8 -*-
{
    'name': "Films",
    'description': """
        Films
    """,
    'author': "Eugene Mahiliavets",
    'website': "https://github.com/",
    'category': 'Uncategorized',
    'version': '0.1',
    'application': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/cinema_views.xml',
        'views/films_views.xml',
    ],
    'license': 'LGPL-3',
}
