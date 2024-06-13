# Copyright (c) 2024, Hilda Chepkirui and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe.utils import flt

class Order(Document):
	pass

@frappe.whitelist(allow_guest=True)
def create_or_update_invoice(order_id='Mwangi-06'):
	print(f"Processing order_id: {order_id}")
	doc = frappe.get_doc("Order", order_id)

	if not doc:
		print("Order not found")
		return {"error": "Order not found"}
	
	customer_name = doc.customer_name
	print(f"Customer name from order: {customer_name}")

	customer = frappe.get_value("Customer", {"customer_name": customer_name}, "name")
	if not customer:
		customer = frappe.get_doc({
			'doctype': 'Customer',
			'customer_name': customer_name,
			'customer_type': "Individual",
		})
		try:
			customer.insert(ignore_permissions=True)
			frappe.db.commit()
			print(f"Created new customer: {customer.name}")
		except Exception as e:
			frappe.log_error(f"Error creating customer: {e}")
			return {"error": f"Error creating customer: {e}"}
	else:
		customer = frappe.get_doc("Customer", customer)
	
	try:
		invoice = create_or_update_sales_invoice(doc, customer)
	except Exception as e:
		frappe.log_error(f"Error processing order items: {e}")
		return {"error": f"Error processing order items: {e}"}
	
	# return "success"
def create_or_update_sales_invoice(doc, customer):
	existing_invoice = frappe.get_all("Sales Invoice", filters={"customer": customer.name, "status": "Draft"})
	if existing_invoice:
		invoice = frappe.get_doc("Sales Invoice", existing_invoice[0].name)
		print(f"Using existing invoice: {invoice.name}")
	else:
		invoice = frappe.new_doc("Sales Invoice")
		invoice.customer = customer.name
	# 	({
	# 		"doctype": "Sales Invoice",
	# 		"customer": customer.name,
	# 		"items": [],
	# 	})
	# 	invoice.insert(ignore_permissions=True)
	# 	frappe.db.commit()
	# 	print("Created new invoice")
	return update_invoice_items(invoice, doc.order_item)
def update_invoice_items(invoice, order_items):
	existing_item_codes = [item.item_code for item in invoice.items]

	for order in order_items:
		print(f"Processing order item: {order.name}")
		existing_item=frappe.get_value("Item", {"item_name": order.menu_item}, "name")

		if existing_item:
			item = frappe.get_doc('Item', existing_item)
			print(f"Updating existing item: {item.item_code}")
			item.item_group = "Consumable"
			try:
				item.save(ignore_permissions=True)
				frappe.db.commit()
				print("Committed item changes")
			except Exception as e:
				frappe.log_error(f"Error saving item: {e}")
				continue 
		else:
			item = frappe.new_doc("Item")
			item.item_code = order.name
			item.item_name = order.menu_item
			item.item_group = "Consumable"
			try:
				item.insert(ignore_permissions=True)
				frappe.db.commit()
				print(f"Inserted new item: {item.item_code}")
			except Exception as e:
				frappe.log_error(f"Error inserting item: {e}")
				continue
			# ({
			# 	"doctype": "Item",
			# 	"item_code": order.name,
			# 	"item_name": order.menu_item,
			# 	"item_group": "Consumable"
			# })
		if order.name not in existing_item_codes:
			print(f"Adding item to invoice: {order.name}")
			invoice.append("items", {
				"item_code": order.menu_item,
				"rate": order.price,
				"amount": order.price * (order.quantity if order.quantity and order.quantity > 0 else 1),
				"qty": order.quantity if order.quantity and order.quantity > 0 else 1  # Ensure quantity is set and greater than zero
			})
	try:
		invoice.save(ignore_permissions=True)
		frappe.db.commit()
		print("Committed invoice changes")
	except Exception as e:
		frappe.log_error(f"Error saving invoice: {e}")
		raise  # Raise the exception to be caught in the calling function
    
    # Return success message
	return invoice