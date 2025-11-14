from odoo import models, fields, api
from odoo.exceptions import UserError
import io
import xlsxwriter

class SalePurchaseReportWizard(models.TransientModel):
    _name = 'sale.purchase.report.wizard'
    _description = 'Sale & Purchase Report Wizard'

    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date > rec.end_date:
                raise UserError("Start date cannot be after end date.")

    def action_generate_excel(self):
        if not self.start_date or not self.end_date:
            raise UserError("Please set both start and end dates.")

        self.env.cr.execute("""
            SELECT p.id, p.name
            FROM product_product p
            WHERE p.id IN (
                SELECT sol.product_id
                FROM sale_order_line sol
                JOIN sale_order so ON sol.order_id = so.id
                WHERE so.date_order >= %s AND so.date_order <= %s
                AND so.state NOT IN ('cancel', 'draft')
                UNION
                SELECT pol.product_id
                FROM purchase_order_line pol
                JOIN purchase_order po ON pol.order_id = po.id
                WHERE po.date_order >= %s AND po.date_order <= %s
                AND po.state NOT IN ('cancel', 'draft')
            )
            ORDER BY p.name
        """, (self.start_date, self.end_date, self.start_date, self.end_date))

        product_data = self.env.cr.fetchall()
        product_ids = [r[0] for r in product_data]

        workbook = xlsxwriter.Workbook(io.BytesIO())
        worksheet = workbook.add_worksheet('Sale Purchase Report')

        # Header
        header_format = workbook.add_format({'bold': True, 'bg_color': '#d3d3d3'})
        headers = ['No.', 'Nama Produk', 'Total Qty Beli', 'Total Qty Jual',
                   'Rata-rata Harga Beli', 'Rata-rata Harga Jual']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        row = 1
        for idx, (prod_id, prod_name) in enumerate(product_data, start=1):
            # Hitung Purchase
            self.env.cr.execute("""
                SELECT
                    COALESCE(SUM(pol.product_qty), 0) AS qty,
                    COALESCE(AVG(pol.price_unit), 0) AS avg_price
                FROM purchase_order_line pol
                JOIN purchase_order po ON pol.order_id = po.id
                WHERE pol.product_id = %s
                  AND po.date_order >= %s AND po.date_order <= %s
                  AND po.state NOT IN ('cancel', 'draft')
            """, (prod_id, self.start_date, self.end_date))
            purchase = self.env.cr.fetchone()

            # Hitung Sale
            self.env.cr.execute("""
                SELECT
                    COALESCE(SUM(sol.product_uom_qty), 0) AS qty,
                    COALESCE(AVG(sol.price_unit), 0) AS avg_price
                FROM sale_order_line sol
                JOIN sale_order so ON sol.order_id = so.id
                WHERE sol.product_id = %s
                  AND so.date_order >= %s AND so.date_order <= %s
                  AND so.state NOT IN ('cancel', 'draft')
            """, (prod_id, self.start_date, self.end_date))
            sale = self.env.cr.fetchone()

            worksheet.write(row, 0, idx)
            worksheet.write(row, 1, prod_name)
            worksheet.write(row, 2, purchase[0] or 0)
            worksheet.write(row, 3, sale[0] or 0)
            worksheet.write(row, 4, round(purchase[1], 2) if purchase[1] else 0)
            worksheet.write(row, 5, round(sale[1], 2) if sale[1] else 0)
            row += 1

        workbook.close()
        output = workbook.filename
        output.seek(0)

        attachment = self.env['ir.attachment'].create({
            'name': f'SalePurchaseReport_{self.start_date}_to_{self.end_date}.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }