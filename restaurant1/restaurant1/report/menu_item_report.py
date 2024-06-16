# Copyright (c) 2024, Hilda Chepkirui and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_data(filters):
    conditions = "1=1"
    if filters.get("start_date"):
        conditions += f" AND `tabMenu Item`.`creation` >= '{filters.get('start_date')}'"
    if filters.get("end_date"):
        conditions += f" AND `tabMenu Item`.`creation` <= '{filters.get('end_date')}'"

    SQL = f"""
        SELECT
            `tabMenu Item`.`name` AS `menu_item`,
            COUNT(`tabOrder Item`.`name`) AS `total_orders`,
            SUM(`tabOrder Item`.`quantity`) AS `total_quantity_sold`,
            SUM(`tabOrder Item`.`price` * `tabOrder Item`.`quantity`) AS `total_sales_amount`
        FROM 
            `tabMenu Item`
        LEFT JOIN 
            `tabOrder Item` ON `tabMenu Item`.`name` = `tabOrder Item`.`menu_item`
        LEFT JOIN
            `tabOrder` ON `tabOrder Item`.`parent` = `tabOrder`.`name`
        WHERE
            {conditions}
        GROUP BY 
            `tabMenu Item`.`name`
        ORDER BY 
            `total_sales_amount` DESC
    """
    data = frappe.db.sql(SQL, as_dict=True)
    return data

def get_columns():
    return [
        {"fieldname": "menu_item", "label": "Menu Item", "fieldtype": "Link", "options": "Menu Item", "width": 200},
        {"fieldname": "total_orders", "label": "Total Orders", "fieldtype": "Int", "width": 150},
        {"fieldname": "total_quantity_sold", "label": "Total Quantity Sold", "fieldtype": "Float", "width": 150},
        {"fieldname": "total_sales_amount", "label": "Total Sales Amount", "fieldtype": "Currency", "width": 150}
    ]
