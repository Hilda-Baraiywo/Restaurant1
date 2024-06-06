import frappe
from datetime import datetime, timedelta,time


@frappe.whitelist(allow_guest=True)
def save_time():
    now = datetime.now()
    today_date = now.date()
    current_time = now.strftime("%H:%M:%S")
    return current_time

@frappe.whitelist(allow_guest=True)
def calculate_default_value():
    default_value = 0.00
    return default_value

# @frappe.whitelist(allow_guest=True)
# def validate_order():
#     if not order_data.get("customer_name"):
#         return {
#             "valid": False,
#             "error": "Customer name is required"
#         }
#     return {"valid": True}

@frappe.whitelist(allow_guest=True)
def calculate_total(customer_id):
    items = frappe.get_all("Order Item", {"parent": customer_id}, {"price", "quantity"})
    total = 0
    for item in items:
        total += item.get("quantity", 0) * item.get("price", 0)
    return total

# @frappe.whitelist(allow_guest=True)
# def orderInvoice(order):
# 	customer_name = order.get('customer_name')
# 	customer_email = order.get('customer_email')

# 	existing_customer = frappe.get_all("Customer", filters={"email_id": customer_email})
# 	if existing_customer:
# 		customer = frapp.get_doc("Customer", existing_customer[0].name)
# 	else:
# 		customer = frappe.get_doc({
# 			'doctype': 'Customer',
# 			'customer_name': customer_name,
# 			'email_id': customer_email
# 		})
# 		customer.insert()

# 	existing_invoice = frappe.get_all("Sales Invoice", filters={"customer": customer.name, "status": "Draft"})
# 	if existing_invoice:
# 		invoice = frappe.get_doc("Sales Invoice", existing_invoice[0].name)
# 	else:
# 		invoice = frappe.get_doc({
# 			"doctype": "Sales Invoice",
# 			"customer": customer.name,
# 			"items": [],
# 		})

# 	for order_item in order.get('items'):
# 		menu_item = order_item.get('menu_item')
# 		quantity = order_item.get('quantity')
# 		price = order_item.get('price')

# 		item_name = menu_item
# 		existing_item = frappe.get_all("Item", {"item_name": item_name}, {'item_name', 'item_group'})
# 		if not existing_item:
# 			item = frappe.get_doc({
# 				"doctype": "Item",
# 				"item_code": item_name,
# 				"item_name": item_name,
# 				"item_group": "Menu Items",
# 				"description": "Menu items for restaurant"
# 			})
# 			item.insert()
# 			frappe.db.commit()

# 		existing_item_codes = [item.item_code for item in invoice.get("items")]

# 		if item_name not in existing_item_codes:
# 			invoice.append("items", {
# 				"item_code": item_name,
# 				"rate": price/quantity,
# 				"amount": price,
# 				"qty": quantity,
# 			})
# 		if not existing_invoice:
# 			invoice.insert()
# 		else:
# 			invoice.save()
# 		frappe.db.commit()