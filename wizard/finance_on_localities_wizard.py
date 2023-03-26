from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import datetime

class FinanceOnLocalitiesWizard(models.TransientModel):
    _name = 'finance_on_localities.report.wizard'

    from_date = fields.Date('From', default=fields.Date.today())
    to_date = fields.Date('To', default=fields.Date.today())

    @api.constrains('from_date')
    def _check_date_from(self):
        if self.from_date > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

    @api.constrains('to_date')
    def _check_date_to(self):
        if self.to_date < datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))
   
    def get_localities_data(self, from_date, to_date):
        lines = []
        finance_request_data =self.env['bank.finance_request'].search([])
        locality_list =finance_request_data.mapped('localities_id')

        
        total_localities_amount = sum(finance_request_data.mapped('amount_cert'))
        self.env['bank.localities'].search([]).write({"locality_share": 0})

        for locality in locality_list:
            locality_amount = sum(finance_request_data.filtered(lambda p: p.localities_id == locality).mapped('amount_cert'))
            locality_share = round((locality_amount / total_locality_amount) * 100, 2)

            lines.append({
                'locality': locality.localities_id,
                'locality_amount':locality_amount,
                'locality_share': locality_share,
            })
            locality.locality_share = locality_share

        return lines

    def get_report(self):
        locality_data = self.get_localities_data(self.from_date, self.to_date)
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'data': locality_data,

            
            }
        
        return self.env.ref('bank.finance_on_localities_report').report_action(self, data=data)

    def get_chart(self):
        locality_data = self.get_locality_data(self.from_date, self.to_date)
        action = {
            'view_mode': 'graph',
            'res_model': 'bank.localities',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'name': _('Finance On Localities In Period From: {} To: {}'.format(self.from_date, self.to_date)),
        }
        return action 


class FinanceOnLocalitiesReport(models.AbstractModel):
    _name = 'report.bank.finance_on_localities_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'docs': data.get('data'),
            'from_date': data.get('from_date'),
            'to_date': data.get('to_date'),
        }
