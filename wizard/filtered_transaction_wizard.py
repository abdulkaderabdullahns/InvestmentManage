from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import datetime

class FilteredTransactionReportWizard(models.TransientModel):
    _name = 'filtered_transaction.report.wizard'

    from_date = fields.Date('From', default=fields.Date.today())

    @api.constrains('from_date')
    def _check_date_from(self):
        if self.from_date > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))




    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'from_date': fields.Date.from_string(self.from_date),
                # 'state': self.state,
                # 'by': self.by,
                # 'number': self.number.id,
            },
        }

        return self.env.ref('bank.filtered_transaction_report').report_action(self, data=data)


class FilteredTransactionReport(models.AbstractModel):
    _name = 'report.bank.filtered_transaction_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data['form']['from_date']

        # if:
        docs = self.env['bank.transaction_installments'].search([('req_date', '>=', from_date)])

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],

            'from_date': from_date,
            # 'state': state,
            # 'by':by,

            'docs': docs,
        }



