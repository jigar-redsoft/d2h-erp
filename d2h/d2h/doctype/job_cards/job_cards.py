# Copyright (c) 2024, ashish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class JobCards(Document):
	def validate(self):
		if self.status == "In Process":
			allow_status = { "value": True, "items": []}
			for item in self.activity_items:
				stock_qty = frappe.db.get_value("Bin", {"item_code": item.item}, "actual_qty")
				in_process_items = frappe.get_all("Activity Item", filters={"item": item.item, "parenttype":"Job Cards", "status": "In Process"}, fields=["name", "status", "item", "quantity"])
				total_quantity = 0
				for in_process_item in in_process_items:
					total_quantity += in_process_item.quantity
				if total_quantity + item.quantity > stock_qty:
					allow_status["value"] = False
					allow_status["items"].append(item.item)
			
			if not allow_status["value"]:
				frappe.throw("Item(s) " + ", ".join(allow_status["items"]) + " are not available in stock to process")
				

		for item in self.activity_items:
			item.status = self.status
				

@frappe.whitelist()
def get_items(activities):
	activities = json.loads(activities)
	data = []
	for activity in activities:
		items = frappe.get_all("Activity Item", filters={"parent": activity}, fields=["item", "quantity"])
		for item in items:
			data.append({
				"item": item.item,
				"quantity": item.quantity
			})
	return data

@frappe.whitelist()
def get_activity_items_status(items):
	items = json.loads(items)
	data = { "status": True, "items": [] }
	for item in items:
		data.append({
			"item": item.item,
			"quantity": item.quantity
		})
	return data