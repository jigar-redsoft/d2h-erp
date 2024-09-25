# Copyright (c) 2024, ashish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class JobCards(Document):
	pass

@frappe.whitelist()
def get_equipments(activities):
	activities = json.loads(activities)
	data = []
	for activity in activities:
		equipments = frappe.get_all("Activity Equipment", filters={"parent": activity}, fields=["equipment", "quantity"])
		for equipment in equipments:
			data.append({
				"equipment": equipment.equipment,
				"quantity": equipment.quantity
			})
	return data