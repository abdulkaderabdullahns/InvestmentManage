from odoo import models, fields, api


class InstallmentsNotPaymentstypeReportWizard(models.TransientModel):
    _name = 'installments_not_payments.report.wizard'

    from_date = fields.Date('From', default=fields.Date.today())
    to_date = fields.Date('To', default=fields.Date.today())

    customer = fields.Many2one("bank.customers", string="Customer ")
    cust_name = fields.Char(related='customer.name', string="Customer")
    re_number = fields.Many2one("bank.transaction_installments", "Requer id", required="1")
    req_date = fields.Date(string="Requer Date", related='re_number.req_date')
    fintype = fields.Selection(
        [("Agricultural Finance", "Agricultural Finance"),
         ("Animal Finance", "FemAnimal Financeale"),
         ("Microfinance", "Microfinance"),
         ("other", "Other")], string='finance type')

    number = fields.Many2one("bank.section",string='Section')
    number_id = fields.Many2one("bank.activity", string="Activity ")
    for_number = fields.Many2one("bank.formula", string="Formula ")


    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'from_date': fields.Date.from_string(self.from_date),
                'to_date': fields.Date.from_string(self.to_date),
                'customer': self.customer.id,
                'cust_name': self.cust_name,
                're_number': self.re_number,
                'req_date': self.req_date,
                'fintype':self.fintype,
                'number': self.number.id,
                'number_id': self.number_id.id,
                'for_number': self.for_number.id,

                # 'state': self.state,
                # 'by': self.by,
                # 'number': self.number.id,
            },
        }

        return self.env.ref('bank.installments_not_payments_report').report_action(self, data=data)


class InstallmentsNotPaymentstypeReport(models.AbstractModel):
    _name = 'report.bank.installments_not_payments_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
        customer = data['form']['customer']
        cust_name = data['form']['cust_name']
        re_number = data['form']['re_number']
        req_date = data['form']['req_date']
        fintype = data['form']['fintype']
        number = data['form']['number']
        number_id = data['form']['number_id']
        for_number = data['form']['for_number']

        # state = data['form']['state']
        # by = data['form']['by']
        # number = data['form']['number']
        #

        if customer:
            docs = self.env['bank.installments_payments'].search(
                [('req_date', '>=', from_date), ('req_date', '<=', to_date),
                 ('customer', '=', customer)])
        if cust_name:
            docs = self.env['bank.installments_payments'].search(
                [('req_date', '>=', from_date), ('req_date', '<=', to_date),
                 ('cust_name', '=', cust_name)])
        if re_number:
            docs = self.env['bank.installments_payments'].search(
                [('req_date', '>=', from_date), ('req_date', '<=', to_date),
                ('re_number', '=', re_number)])
        if req_date:
            docs = self.env['bank.installments_payments'].search(
                [('req_date', '>=', from_date), ('req_date', '<=', to_date),
                 ('req_date', '=', req_date)])
        if fintype:
            docs = self.env['bank.installments_payments'].search(
                [('req_date', '>=', from_date), ('req_date', '<=', to_date),
                 ('fintype', '=', fintype)])

        if number:
             docs = self.env['bank.installments_payments'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date),
                                                        ('number','=',number)])
        if number_id:
            docs = self.env['bank.installments_payments'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date),
                                                   ('number_id','=',number_id)])
        if for_number:
            docs = self.env['bank.installments_payments'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date),
                                                   ('for_number','=',for_number)])


        # # if:
        # docs = self.env['bank.first_payments_customers'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date),
        #                                                 ('fin_type', '=', fin_type)])

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],

            'from_date': from_date,
            'to_date': to_date,
            'customer':customer,
            'cust_name':cust_name,
            're_number':re_number,
            'req_date':req_date,
            'fintype':fintype,
            'number': number,
            'number_id': number_id,
            'for_number': for_number,
            # 'state': state,
            # 'by':by,

            'docs': docs,
        }
