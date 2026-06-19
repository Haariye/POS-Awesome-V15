import frappe
from frappe import _
from frappe.utils import flt
from posawesome.posawesome.api.item_processing.barcode import _parse_scale_barcode_data


@frappe.whitelist()
def update_price_list_rate(item_code, price_list, rate, uom=None):
    """Create or update Item Price for the given item and price list."""
    if not item_code or not price_list:
        frappe.throw(_("Item Code and Price List are required"))

    rate = flt(rate)
    filters = {"item_code": item_code, "price_list": price_list}
    if uom:
        filters["uom"] = uom
    else:
        filters["uom"] = ["in", ["", None]]

    name = frappe.db.exists("Item Price", filters)
    if name:
        doc = frappe.get_doc("Item Price", name)
        doc.price_list_rate = rate
        doc.save(ignore_permissions=True)
    else:
        doc = frappe.get_doc(
            {
                "doctype": "Item Price",
                "item_code": item_code,
                "price_list": price_list,
                "uom": uom,
                "price_list_rate": rate,
                "selling": 1,
            }
        )
        doc.insert(ignore_permissions=True)

    frappe.db.commit()
    return _("Item Price has been added or updated")


@frappe.whitelist()
def get_price_for_uom(item_code, price_list, uom, customer=None):
    """Return the correct Item Price rate for an item + price list + UOM.

    Price priority fix
    ------------------
    The cart UOM-change path calls this when a line's UOM changes. The old
    implementation used ``frappe.db.get_value`` which, when several Item Price
    rows share the same item/price_list/uom (e.g. one customer-specific and one
    general), returned an arbitrary row (effectively the last-saved one). That
    broke customer pricing on UOM change.

    We now select deterministically:
        1. customer-specific row   (Item Price.customer == customer)
        2. customer-group row      (Item Price.customer == customer's group)
        3. general row             (Item Price.customer is blank)
    Rate is never decided by creation/modified date.

    ``customer`` is optional to preserve backward compatibility with existing
    frontend callers; when omitted, only general rows are considered (matching
    the previous default behaviour) but still chosen deterministically.
    """
    if not (item_code and price_list and uom):
        return None

    customer_group = ""
    if customer:
        customer_group = frappe.db.get_value("Customer", customer, "customer_group") or ""

    # Fetch every candidate row for this item/price_list/uom that could apply
    # to the customer context, then rank in Python.
    rows = frappe.get_all(
        "Item Price",
        filters={
            "item_code": item_code,
            "price_list": price_list,
            "uom": uom,
            "selling": 1,
        },
        fields=["price_list_rate", "customer"],
    )

    if not rows:
        return None

    def _rank(row_customer):
        rc = (row_customer or "").strip()
        if not rc:
            return 1
        if customer and rc == customer:
            return 3
        if customer_group and rc == customer_group:
            return 2
        return 0  # belongs to another customer/group -> ignore

    best_rank = -1
    best_rate = None
    for row in rows:
        rank = _rank(row.get("customer"))
        if rank == 0:
            continue
        if rank > best_rank:
            best_rank = rank
            best_rate = row.get("price_list_rate")

    return best_rate
