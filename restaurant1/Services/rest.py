import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta,time

class Order(Document):
    def before_save(self):
        if not self.status:
            self.status = 'Pending'

    def after_insert(self):
        if self.status == 'Confirmed':
            frappe.publish_realtime('order_confirmed', self.name, user=self.owner)

    def on_submit(self):
        self.status = 'Completed'
        # self.notify_staff()

    # def notify_staff(self):
        # pass

@frappe.whitelist(allow_guest=True)
def save_time():
    now = datetime.now()
    today_date = now.date()
    current_time = now.strftime("%H:%M:%S")
    return current_time

@frappe.whitelist(allow_guest=True)
def calculate_total(customer_id='Aloo-01'):
    items = frappe.get_all("Order Item", {"parent": customer_id}, {"price", "quantity"})
    total = 0
    for item in items:
        total += item.get("quantity", 0) * item.get("price", 0)
    return total

@frappe.whitelist(allow_guest=True)
def check_menu_item(menu_item='French Fries'):
    menu_item_doc = frappe.get_doc("Menu Item", menu_item)
    if not menu_item_doc or not menu_item_doc.is_available:
        return True
    return False

@frappe.whitelist(allow_guest=True)
def calculate_total_price(order_item='Beef Stew'):
    items = frappe.get_all("Order Item", filters={"menu_item": order_item}, fields=["price", "quantity","name"])
    total_price = 0
    for item in items:
        item_total = item.get("quantity", 0) * item.get("price", 0)
        total_price += item_total
        frappe.db.set_value("Order Item", item["name"], "total_price", item_total)
    return total_price

@frappe.whitelist(allow_guest=True)
def update_total_price(order_id='Oloo-02'):
    order_doc = frappe.get_doc("Order", order_id)
    total_amount = sum(item.quantity * item.price for item in order_doc.order_item)
    for item in order_doc.order_item:
        frappe.db.set_value("Order Item", item.name, "total_price", item.quantity * item.price)
    frappe.db.set_value("Order", order_id, "total_amount", total_amount)
    return total_amount