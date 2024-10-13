from odoo import models, fields, api
import requests
import json
from odoo.http import request, route

class WhatsAppMessage(models.Model):
    _name = 'whatsapp.message'
    _description = 'Message WhatsApp'

    recipient = fields.Char(string='Destinataire', required=True)
    message = fields.Text(string='Message', required=True)
    message_type = fields.Selection([
        ('text', 'Texte'),
        ('image', 'Image'),
        ('document', 'Document'),
        ('interactive', 'Interactif')
    ], string='Type de message', default='text')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('sent', 'Envoyé'),
        ('failed', 'Échec')
    ], string='État', default='draft')

    def send_message(self):
        api_url = 'https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages'
        headers = {
            'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'to': self.recipient,
            'type': self.message_type,
        }
        
        if self.message_type == 'text':
            data['text'] = {'body': self.message}
        elif self.message_type == 'interactive':
            # Exemple de message interactif (à adapter selon vos besoins)
            data['interactive'] = json.loads(self.message)
        
        response = requests.post(api_url, json=data, headers=headers)
        
        if response.status_code == 200:
            self.state = 'sent'
        else:
            self.state = 'failed'

class WhatsAppWebhook(models.AbstractModel):
    _name = 'whatsapp.webhook'
    _description = 'Webhook WhatsApp'

    @api.model
    @route('/whatsapp/webhook', type='json', auth='public', methods=['POST'])
    def webhook(self):
        data = json.loads(request.httprequest.data)
        
        if 'entry' in data:
            for entry in data['entry']:
                for change in entry['changes']:
                    if change['field'] == 'messages':
                        for message in change['value']['messages']:
                            self._process_message(message)
        
        return {'status': 'ok'}

    def _process_message(self, message):
        if message['type'] == 'text':
            self._handle_text_message(message)
        elif message['type'] == 'interactive':
            self._handle_interactive_message(message)
        # Ajoutez d'autres types de messages selon vos besoins

    def _handle_text_message(self, message):
        # Traitez le message texte ici
        self.env['whatsapp.message'].create({
            'recipient': message['from'],
            'message': message['text']['body'],
            'message_type': 'text',
            'state': 'sent'  # Considéré comme envoyé car c'est un message reçu
        })

    def _handle_interactive_message(self, message):
        # Traitez le message interactif ici
        interactive_data = json.dumps(message['interactive'])
        self.env['whatsapp.message'].create({
            'recipient': message['from'],
            'message': interactive_data,
            'message_type': 'interactive',
            'state': 'sent'  # Considéré comme envoyé car c'est un message reçu
        })