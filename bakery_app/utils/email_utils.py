import os
import threading
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class EmailThread(threading.Thread):
    """
    使用多執行緒發送郵件，避免讓使用者在結帳頁面等待太久
    """
    def __init__(self, subject, body, from_email, recipient_list, html_message=None, attachment_path=None):
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.html_message = html_message
        self.attachment_path = attachment_path
        threading.Thread.__init__(self)

    def run(self):
        try:
            msg = EmailMultiAlternatives(
                self.subject,
                self.body,
                self.from_email,
                self.recipient_list
            )
            if self.html_message:
                msg.attach_alternative(self.html_message, "text/html")
            if self.attachment_path and os.path.exists(self.attachment_path):
                msg.attach_file(self.attachment_path)
            msg.send(fail_silently=True)
        except Exception as e:
            print(f"郵件發送失敗: {e}")

def send_order_confirmation(order):
    """
    發送訂單確認信
    """
    if not order.customer_email:
        return

    payment_status = "未付款"
    if order.payment_method == 'cod':
        payment_status = "貨到付款 (尚未付款)"
    elif order.payment_method == 'linepay':
        if order.paid_at:
            payment_status = "LINE Pay (已付款)"
        else:
            payment_status = "LINE Pay (待付款)"

    if hasattr(order, 'items'):
        items = order.items.all()
    else:
        items = order.orderitem_set.all()

    items_text_list = ""
    items_html_rows = ""

    for item in items:
        original_price = item.product.price
        deal_price = item.price
        
        price_display_text = f"NT${deal_price}"
        if deal_price < original_price:
            price_display_text = f"NT${deal_price} (原價 NT${original_price})"
            
        items_text_list += f"• {item.product.name} x {item.quantity} - {price_display_text}\n"

        price_display_html = f"NT${deal_price}"
        if deal_price < original_price:
            price_display_html = f"""
                <span style="text-decoration: line-through; color: #999; font-size: 0.9em;">NT${original_price}</span><br>
                <span style="color: #d63031; font-weight: bold;">NT${deal_price}</span>
            """
        
        items_html_rows += f"""
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 8px;">{item.product.name}</td>
            <td style="padding: 8px; text-align: center;">{item.quantity}</td>
            <td style="padding: 8px; text-align: right;">{price_display_html}</td>
        </tr>
        """
    
    items_html_table = f"""
    <table style="width: 100%; border-collapse: collapse; max-width: 600px; margin-top: 10px;">
        <tr style="background-color: #f3e5dc; color: #7b6a63;">
            <th style="padding: 10px; text-align: left;">商品名稱</th>
            <th style="padding: 10px; text-align: center;">數量</th>
            <th style="padding: 10px; text-align: right;">金額</th>
        </tr>
        {items_html_rows}
        <tr>
            <td colspan="2" style="padding: 10px; text-align: right; font-weight: bold;">運費</td>
            <td style="padding: 10px; text-align: right;">NT${int(order.total_price) - sum(item.price * item.quantity for item in items)}</td>
        </tr>
        <tr>
            <td colspan="2" style="padding: 10px; text-align: right; font-weight: bold; color: #d63031;">總金額</td>
            <td style="padding: 10px; text-align: right; font-weight: bold; color: #d63031;">NT${int(order.total_price)}</td>
        </tr>
    </table>
    """

    subject = f"訂單確認：您在 宏農手工之家 的訂單 #{order.id} 已受理"
    
    text_content = f"""
{order.customer_name} 您好，
感謝您的訂購！我們已收到您的訂單，目前正準備處理中。

【訂單內容摘要】
• 訂單編號：#{order.id}
• 付款狀態：{payment_status}
• 訂單明細：
{items_text_list}
• 總金額：NT${int(order.total_price)}

【配送安排】
• 預計寄送地址：{order.shipping_store}
• 預計出貨天數：約 5～7個工作天（視手工製作週期而定）

如有修改需求，請於出貨前到官方 LINE 通知我們。

宏農手工之家 感謝您的光臨。
"""

    html_content = f"""
    <div style="font-family: sans-serif; line-height: 1.6; color: #333;">
        <p>{order.customer_name} 您好，</p>
        <p>感謝您的訂購！我們已收到您的訂單，目前正準備處理中。</p>
        
        <h3 style="border-left: 4px solid #7b6a63; padding-left: 10px; color: #7b6a63;">【訂單內容摘要】</h3>
        <ul style="list-style: none; padding: 0;">
            <li><strong>訂單編號：</strong>#{order.id}</li>
            <li><strong>付款狀態：</strong>{payment_status}</li>
            <li><strong>訂單明細：</strong></li>
        </ul>
        {items_html_table}
        
        <h3 style="border-left: 4px solid #7b6a63; padding-left: 10px; color: #7b6a63; margin-top: 20px;">【配送安排】</h3>
        <ul style="list-style: none; padding: 0;">
            <li><strong>預計寄送地址：</strong>{order.shipping_store}</li>
            <li><strong>預計出貨天數：</strong>約 5～7個工作天（視手工製作週期而定）</li>
        </ul>
        
        <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="font-size: 0.9em; color: #666;">如有修改需求，請於出貨前到官方 LINE 通知我們。</p>
        <p style="font-weight: bold; color: #7b6a63;">宏農手工之家 感謝您的光臨。</p>
    </div>
    """
    qr_code_path = os.path.join(settings.BASE_DIR, 'static/images', 'line_qr.jpg')

    EmailThread(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.customer_email],
        html_message=html_content,
        attachment_path=qr_code_path
    ).start()