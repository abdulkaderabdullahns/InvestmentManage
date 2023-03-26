from datetime import  datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import datetime


class OperationsMaidOnActivityWizard(models.TransientModel):
    _name = 'operations_maid_on_activity.report.wizard'

    from_date = fields.Date('From', default=fields.Date.today())

    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'from_date ': fields.Date.from_string(self.from_date),
            
            },
        }
        return self.env.ref('bank.operations_maid_on_activity_report').report_action(self, data=data)

class OperationsMaidOnActivityReport(models.AbstractModel):
    _name = 'report.bank.operations_maid_on_activity_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        
        from_date  = data['form']['from_date ']
        
        docs = self.env['bank.finance_request'].search([('req_date', '>=', from_date )])

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],

            
            'from_date ': from_date ,
            'docs': docs,
        }
