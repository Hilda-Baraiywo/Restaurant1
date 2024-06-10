// Copyright (c) 2024, Hilda Chepkirui and contributors
// For license information, please see license.txt

frappe.ui.form.on("Order", {
    onload: function(frm) {
        if (!frm.doc.status){
            frm.set_value('status', 'pending');
        }
    },

    validate: function (frm) {
        frappe.call({
            method: 'restaurant1.Services.rest.save_time',
            args: {
            },
            callback: function (r) {
                if (r.message) { 
                    frm.set_value('order_datetime', r.message);
                } else {
                }   
            },
        });
    },

    validate(frm) {
        let customer_id = frm.doc.name
        frappe.call({
            method: 'restaurant1.restaurant1.doctype.order.order.create_or_update_invoice',
            args: {
                'customer_id': customer_id
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint('Invoice has been created/updated.');
                }
            }
        });
        frappe.call({
            method: 'restaurant1.Services.rest.calculate_total',
            args: {
                'customer_id': customer_id
            },
            callback: function (r) {
                if (r.message) {
                    frm.set_value('total_amount', r.message);
                }
            }
        });
        frappe.call({
            method: 'restaurant1.Services.rest.update_total_price',
            args: {
                'order_id': frm.doc.name
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint(__('Order price updates to: ' + r.message));
                }
            }
        });    
    },
}); 

frappe.ui.form.on('Order Item', {

    "refresh": function(frm) {
        frm.field('price').on('change', function(e){
            calculate_total_price_on_change(frm);
        });
        frm.field('quantity').on('change', function(e){
            calculate_total_price_on_change(frm);
        });
    },
    menu_item: function(frm,cdt, cdn) {
        let item = locals[cdt][cdn];
        let menu_item = item.menu_item || '';
        let quantity = item.quantity || 0;

        frappe.call({
            method: 'restaurant1.Services.rest.check_menu_item',
            args: {
                'menu_item': menu_item
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint('This menu item is not available.');
                    frappe.model.set_value(cdt, cdn, 'menu_item', '');
                }
            }
        });
    },
    quantity: function(frm, cdt, cdn){
        let item = locals[cdt][cdn];
        let price = item.menu_item.price || 0;
        let total_price = price * item.quantity;
        frappe.model.set_value(item.doctype, item.name, 'total_price', total_price);
        frm.refresh_field('items');
        calculate_total_price(frm, item);
    },
    price: function(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        calculate_total_price(frm, item);
    }
});

function calculate_total_price(frm, item){
    frappe.call({
        method: 'restaurant1.Services.rest.calculate_total_price',
        args: {
            'order_item': item.menu_item
        },
        callback: function (r) {
            if (r.message) {
                frappe.model.set_value(item.doctype, item.name, 'total_price', r.message);
                frm.refresh_field('items');
            }
        }
    });
}

