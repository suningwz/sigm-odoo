from odoo import fields, api, models, _

class TravelOrderReport(models.AbstractModel):
	_name = 'report.travel_order.travel_pdf_report'

	@api.model
	def _get_report_values(self, docids, data):
		"""In this function can access the data returned from the button click function"""
		model_id = data['model_id']
		value = []
		query = """
					SELECT * FROM travel_order as to
					JOIN travel_order_line AS tol ON to.id = tol.order_id
					WHERE to.id = %s
				"""
		value.append(model_id)
		self._cr.execute(query, value)
		record = self._cr.dictfetchall()
		return {
			'docs' : record,
			'date_today' : fields.Datetime.now()
		}