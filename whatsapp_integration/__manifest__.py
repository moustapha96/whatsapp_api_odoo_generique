{
    'name': 'WhatsApp Business Integration',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Intégration de l\'API WhatsApp Business pour Odoo avec Webhook',
    'description': """
        Ce module permet d'intégrer l'API WhatsApp Business dans Odoo.
        Il offre des fonctionnalités pour envoyer des messages WhatsApp directement depuis Odoo
        et traite les retours via un webhook.
    """,
    'author': 'Votre Nom',
    'website': 'https://www.votresite.com',
    'depends': ['base', 'web'],
    'data': [
        'views/whatsapp_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}