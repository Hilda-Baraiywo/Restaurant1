// Copyright (c) 2024, Hilda Chepkirui and contributors
// For license information, please see license.txt

frappe.ui.form.on("Order", {
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
    onload: function(frm) {
        frappe.call({
            method: 'restaurant1.restaurant1.doctype.order.order.calculate_default_value',
            callback: function(r)  {
                if (r.message){
                    frm.set_value('default_value_field', r.message);
                }
            },
        });
    },
    // validate: function(frm) {
    //     frappe.call({
    //         method: 'restaurant1.restaurant1.doctype.order.order.validate_order',
    //         args: {
    //             order_data: frm.doc
    //         },
    //         callback: function(r) {
    //             if (!r.message.valid) {
    //                 frappe.msgprint(__('Order validation failed: ' + r.message.error));
    //                 frappe.validated = false;
    //             }
    //         }
    //     });
    // },
        
    validate(frm) {
        frappe.call({
            method: 'restaurant1.Services.rest.create_or_update_invoice',
            args: {
                'order': frm.doc
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint('Invoice has been created/updated.');
                }
            }
        });
    },

    before_save(frm) {
        frappe.call({
            method: 'restaurant1.Services.rest.calculate_total',
            args: {
                order_data: frm.doc
            },
            callback: function (r) {
                if (r.message) {
                    frm.set_value('total_price', r.message.total_price);
                }
            }
        });
    },
}); 

frappe.ui.form.on('Order Item', {
    menu_item(frm,cdt, cdn) {
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
    quantity(frm, cdt, cdn){
        let item = locals[cdt][cdn];
        calculate_total_price(frm, item);
    },
    price(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        calculate_total_price(frm, item);
    }
})


