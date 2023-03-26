from odoo import models, fields, api


class InstallmentsPaymentstypeReportWizard(models.TransientModel):
    _name = 'installments_payments.report.wizard'

    from_date = fields.Date('From', default=fields.Date.today())
    to_date = fields.Date('To', default=fields.Date.today())
    # requer_ids = fields.Many2one("bank.transaction_installments")
    customer_id = fields.Many2one("bank.customers", string="Customer ")
    # customer_name = fields.Char()
    fin_type = fields.Selection(
        [("Agricultural Finance", "تمويل الزراعي"), ("Animal Finance", "FemAnimal Financeale"),
         ("Microfinance", "Microfinance"), ("other", "Other")], defualt="Agricultural Finance", string="Finance Type",
        Tracking=True)

    name_section = fields.Many2one("bank.section",string='Section')
    name_activity = fields.Many2one("bank.activity", string="Activity ")
    for_number = fields.Many2one("bank.formula", string="Formula ")


    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'from_date': fields.Date.from_string(self.from_date),
                'to_date': fields.Date.from_string(self.to_date),
                'customer_id': self.requer_num.number.customer_id.customer_id,
                # 'customer_name': self.customer.id.name,
                'fin_type':self.fin_type,
                'name_section': self.requer_num.number.name_section.id,
                'name_activity': self.requer_num.number.name_activity.id,
                'for_number': self.requer_num.number.for_number.id,

                # 'state': self.state,
                # 'by': self.by,
                # 'number': self.number.id,
            },
        }

        return self.env.ref('bank.installments_payments_report').report_action(self, data=data)


class InstallmentsPaymentstypeReport(models.AbstractModel):
    _name = 'report.bank.installments_payments_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
        customer_id = data['form']['customer_id']
        # customer_name = data['form']['customer_id']
        fin_type = data['form']['fin_type']
        name_section = data['form']['name_section']
        name_activity = data['form']['name_activity']
        for_number = data['form']['for_number']

        # state = data['form']['state']
        # by = data['form']['by']
        # number = data['form']['number']
        #

        if customer_id:
            docs = self.env['bank.transaction_installments'].search(
                [('req_date', '>=', from_date), ('req_date', '<=', to_date),
                 ('customer_id', '=', customer_id)])
        # if customer_id:
        #     docs = self.env['bank.transaction_installments'].search(
        #         [('req_date', '>=', from_date), ('req_date', '<=', to_date),
        #          ('customer_id.name', '=', customer_id.name)])
        # if customer_name:
        #     docs = self.env['bank.transaction_installments'].search(
        #         [('req_date', '>=', from_date), ('req_date', '<=', to_date)])
        if fin_type:
            docs = self.env['bank.transaction_installments'].search(
                [('req_date', '>=', from_date), ('req_date', '<=', to_date),
                 ('fin_type', '=', fin_type)])

        if name_section:
             docs = self.env['bank.transaction_installments'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date),
                                                        ('name_section','=',name_section)])
        if name_activity:
            docs = self.env['bank.transaction_installments'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date),
                                                   ('name_activity','=',name_activity)])
        if for_number:
            docs = self.env['bank.transaction_installments'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date),
                                                   ('for_number','=',for_number)])
        else:
            docs = self.env['bank.transaction_installments'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date)])


        # # if:
        # docs = self.env['bank.first_payments_customers'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date),
        #                                                 ('fin_type', '=', fin_type)])

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],

            'from_date': from_date,
            'to_date': to_date,
            'customer_id':customer_id,
            # 'customer_id.name':customer_id.name,
            'fin_type':fin_type,
            'name_section': name_section,
            'name_activity': name_activity,
            'for_number': for_number,
            # 'state': state,
            # 'by':by,

            'docs': docs,
        }
