// Copyright (c) 2024, Hilda Chepkirui and contributors
// For license information, please see license.txt

frappe.ui.form.on("Table", {
	refresh: function(frm) {
        if (frm.doc.status === "Reserved") {
            frm.add_custom_button(__('Check-in Reservation'), function() {
                frappe.call({
                    method: 'restaurant1.Services.rest.check_in_reservation',
                    args: {
                        table_id: frm.doc.name
                    },
                    callback: function(response) {
                        if (response.message.success) {
                            frm.reload_doc();
                        } else {
                            frappe.msgprint(__('Failed to check-in reservation: ') + response.message.error);
                        }
                    }
                });
            }).addClass('btn-primary');
        }

        frm.add_custom_button(__('Group Tables'), function() {
            frappe.call({
                method: 'restaurant1.Services.rest.get_available_tables',
                callback: function(response) {
                    if (response.message) {
                        var table_number = response.message;
        
                        frappe.prompt([
                            {
                                fieldname: 'table_to_group',
                                fieldtype: 'Select',
                                options: table_number,
                                label: 'Select Table to Group',
                                reqd: 1
                            }
                        ], function(values) {
                            frappe.call({
                                method: 'restaurant1.Services.rest.group_tables',
                                args: {
                                    tables: JSON.stringify([values.table_to_group])
                                },
                                callback: function(response) {
                                    if (response.message.success) {
                                        frm.reload_doc();
                                    } else {
                                        frappe.msgprint(__('Failed to group tables: ') + response.message.error);
                                    }
                                }
                            });
                        }, __('Group Tables'), __('Group'));
                    } else {
                        frappe.msgprint(__('Error fetching available tables.'));
                    }
                }
            });
        }).addClass('btn-primary');
    }
});
        