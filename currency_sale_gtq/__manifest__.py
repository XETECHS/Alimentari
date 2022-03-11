# -*- coding: utf-8 -*-
{
    'name': 'Company Currency Total in Sale',
    'version': '14.0.1.0.0',
    'summary': 'View the total amount in company currency in Sale',
    'description': 'amount in company currency amount total in company currency total',
    'category': 'Sales',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': '@juancacorps',
    'depends': [
        'account',
        'sale',
        'purchase'
    ],
    'website': 'https://www.cybrosys.com',
    'data': [
        'views/sale_view.xml', 'views/purchase_view.xml'
    ],
    'qweb': [],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
