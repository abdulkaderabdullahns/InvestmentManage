from odoo import models, fields, api


class TransactionInstallmentsReportWizard(models.TransientModel):
    _name = 'transaction_installments.report.wizard'

    from_date = fields.Date('From', default=fields.Date.today())
    to_date = fields.Date('To', default=fields.Date.today())


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

        return self.env.ref('bank.transaction_installments_report').report_action(self, data=data)


class TransactionInstallmentsReport(models.AbstractModel):
    _name = 'report.bank.transaction_installments_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']

        # if:
        docs = self.env['bank.transaction_installments'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date)])

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],

            'from_date': from_date,
            'to_date': to_date,
            # 'state': state,
            # 'by':by,

            'docs': docs,
        }



