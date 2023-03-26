from datetime import  datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import datetime


class OperationsTransformToManagementLawWizard(models.TransientModel):
    _name = 'operations_trans_to_management_law.report.wizard'

    from_date = fields.Date('From', default=fields.Date.today())
    to_date = fields.Date('To', default=fields.Date.today())
   
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'from_date': fields.Date.from_string(self.from_date),
                'to_date': fields.Date.from_string(self.to_date),
            
            },
        }
        return self.env.ref('bank.operations_trans_to_management_law_report').report_action(self, data=data)

class OperationsTransformToManagementLawReport(models.AbstractModel):
    _name = 'report.bank.operations_trans_to_management_law_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
        
        docs = self.env['bank.finance_request'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date)])

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],

            'from_date': from_date,
            'to_date': to_date,
            'docs': docs,
        }

