from odoo import models, fields, api
from datetime import  datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import datetime





class FinanceRequestReportWizard(models.TransientModel):
    _name = 'finances_requestes.report.wizard'

    from_date = fields.Date('From', default=fields.Date.today())
    to_date = fields.Date('To', default=fields.Date.today())

    @api.constrains('from_date')
    def _check_date(self):
        if self.from_date > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

    @api.constrains('to_date')
    def _check_date(self):
        if self.to_date > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

    def get_report(self):

        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'from_date': fields.Date.from_string(self.from_date),
                'to_date': fields.Date.from_string(self.to_date),
                # 'state': self.state,
                # 'by': self.by,
                # 'number': self.number.id,
            },
        }

        return self.env.ref('bank.finances_requestes_report').report_action(self, data=data)

class FinanceRequestReport(models.AbstractModel):
    _name = 'report.bank.finances_requestes_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']


        # if:
        docs = self.env['bank.finance_request'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date)])



        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],

            'from_date': from_date,
            'to_date': to_date,
            # 'state': state,
            # 'by':by,

            'docs': docs,
        }


