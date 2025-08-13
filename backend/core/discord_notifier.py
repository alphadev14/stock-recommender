import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1405039879875989536/uFyIiS9uCeic4fyknzKi44NzPM-D4wZ0D_axnVE4Sg8igPdaClCO5TGXXRGFT5VTiAq8"

def send_discord_notify(ticker, price_date):
    embed = {
        "title": "📊 Stock Data Inserted Successfully",
        "description": f"Dữ liệu cổ phiếu **{ticker}** đã được lưu thành công vào database.",
        "color": 0x2ecc71,  # Màu xanh lá (hex)
        "footer": {
            "text": f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
    }

    payload = {
        "content": "",       # Nội dung text (nếu muốn kèm ngoài embed)
        "embeds": [embed]    # Embed phải nằm trong mảng
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("✅ Đã gửi thông báo Discord thành công")
    else:
        print(f"⚠️ Gửi Discord thất bại: {response.status_code} - {response.text}")
