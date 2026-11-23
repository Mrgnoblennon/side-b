"""Optional SMTP confirmation for SIDE B.'s simulated orders.

Set SIDE_B_SMTP_HOST, SIDE_B_SMTP_PORT, SIDE_B_SMTP_USER,
SIDE_B_SMTP_PASSWORD and SIDE_B_EMAIL_FROM to enable delivery.
Set SIDE_B_SMTP_SECURITY to "ssl" for implicit TLS (port 465)
or "starttls" for explicit TLS (default, port 587).
"""
import os
import smtplib
import ssl
from email.message import EmailMessage


def send_order_confirmation(order, items):
    """Send a confirmation; return False when SMTP is not configured."""
    keys = ("SIDE_B_SMTP_HOST", "SIDE_B_SMTP_USER", "SIDE_B_SMTP_PASSWORD", "SIDE_B_EMAIL_FROM")
    if not all(os.environ.get(key) for key in keys):
        return False

    security = os.environ.get("SIDE_B_SMTP_SECURITY", "starttls").lower()
    if security not in ("starttls", "ssl"):
        raise ValueError("SIDE_B_SMTP_SECURITY must be 'starttls' or 'ssl'.")
    port = int(os.environ.get("SIDE_B_SMTP_PORT", "465" if security == "ssl" else "587"))

    message = EmailMessage()
    message["Subject"] = f"SIDE B. — Order #{order['id']} confirmation"
    message["From"] = os.environ["SIDE_B_EMAIL_FROM"]
    message["To"] = order["email"]

    lines = [
        f"Hi {order['customer_name']},",
        "",
        f"Thanks for your SIDE B. order! Your simulated order #{order['id']} has been recorded.",
        "This is a student project. No payment was taken and no items will be shipped.",
        "",
        "Your order:",
    ]
    for item in items:
        label = item["product_name"]
        if item.get("variant_label"):
            label += f" ({item['variant_label']})"
        line_total = item["unit_price_cents"] * item["quantity"] / 100
        lines.append(f"- {label} x {item['quantity']} — AUD ${line_total:.2f}")
    lines.extend(["", f"Total: AUD ${order['total_cents'] / 100:.2f}", "", "SIDE B."])
    message.set_content("\n".join(lines))

    context = ssl.create_default_context()
    host = os.environ["SIDE_B_SMTP_HOST"]
    if security == "ssl":
        with smtplib.SMTP_SSL(host, port, timeout=12, context=context) as server:
            server.login(os.environ["SIDE_B_SMTP_USER"], os.environ["SIDE_B_SMTP_PASSWORD"])
            server.send_message(message)
    else:
        with smtplib.SMTP(host, port, timeout=12) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(os.environ["SIDE_B_SMTP_USER"], os.environ["SIDE_B_SMTP_PASSWORD"])
            server.send_message(message)
    return True
