import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_data(filters):
    conditions = "1=1"
    if filters.get("customer_name"):
        conditions += f" AND `tabCustomer`.`customer_name` = '{filters.get('customer_name')}'"

    SQL = f"""
        SELECT
            `tabOrder`.`name` AS `customer_name`,
            `tabOrder`.`order_datetime`,
            `tabCustomer`.`customer_name`,
            `tabItem`.`item_name`,
            `tabOrder Item`.`quantity`,
            `tabOrder Item`.`price`,
            `tabOrder Item`.`quantity` * `tabOrder Item`.`price` AS `total_amount`
        FROM
            `tabOrder`
        LEFT JOIN
            `tabCustomer` ON `tabOrder`.`customer` = `tabCustomer`.`name`
        LEFT JOIN
            `tabOrder Item` ON `tabOrder`.`name` = `tabOrder Item`.`parent`
        LEFT JOIN
            `tabItem` ON `tabOrder Item`.`menu_item` = `tabItem`.`name`
        WHERE
            {conditions}
        ORDER BY
            `tabOrder`.`order_datetime` DESC
    """
    data = frappe.db.sql(SQL, as_dict=True)
    return data

def get_columns():
    return [
        {"fieldname": "order_id", "label": "Customer Name", "fieldtype": "Link", "options": "Customer", "width": 60},
        {"fieldname": "order_datetime", "label": "Order DateTime", "fieldtype": "Datetime", "width": 60},
        {"fieldname": "customer_name", "label": "Customer Name", "fieldtype": "Data", "width": 80},
        {"fieldname": "item_name", "label": "Item Name", "fieldtype": "Link", "options": "Item", "width": 60},
        {"fieldname": "quantity", "label": "Quantity", "fieldtype": "Float", "width": 50},
        {"fieldname": "price", "label": "Price", "fieldtype": "Currency", "width": 60},
        {"fieldname": "total_amount", "label": "Total Amount", "fieldtype": "Currency", "width": 60}
    ]
