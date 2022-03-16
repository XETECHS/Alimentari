# -*- coding: utf-8 -*-
# from odoo import http


# class Alimentari(http.Controller):
#     @http.route('/alimentari/alimentari', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alimentari/alimentari/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('alimentari.listing', {
#             'root': '/alimentari/alimentari',
#             'objects': http.request.env['alimentari.alimentari'].search([]),
#         })

#     @http.route('/alimentari/alimentari/objects/<model("alimentari.alimentari"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alimentari.object', {
#             'object': obj
#         })
