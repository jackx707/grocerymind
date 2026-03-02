import os
import asyncio
from dotenv import load_dotenv
import telegram

load_dotenv("/root/.hermes/.env")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_ALLOWED_USERS")


async def send_receipt(purchases: list, budget_remaining: float, monthly_budget: float):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram env vars missing; skipping notification.")
        return

    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    total_spent = sum(p["price"] for p in purchases)

    lines = []
    lines.append("🛒 *GroceryMind Auto Purchase*")
    lines.append("━━━━━━━━━━━━━━━━━━━━")

    for p in purchases:
        lines.append(f"✅ {p['item']} — €{p['price']:.2f} ({p['store']})")

    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"💰 *Total spent:* €{total_spent:.2f}")
    lines.append(
        f"📊 *Budget remaining:* €{budget_remaining:.2f} / €{monthly_budget:.0f}"
    )
    lines.append("📦 *Pantry restocked* for 14 days")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("_Powered by GroceryMind 🤖_")

    message = "\n".join(lines)

    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown"
    )
    print("📱 Telegram notification sent!")


def notify(purchases: list, budget_remaining: float, monthly_budget: float = 400):
    asyncio.run(send_receipt(purchases, budget_remaining, monthly_budget))


if __name__ == "__main__":
    test_purchases = [
        {"item": "Milk", "price": 1.50, "store": "Rewe"},
        {"item": "Coffee", "price": 4.99, "store": "Rewe"},
        {"item": "Eggs", "price": 2.49, "store": "Aldi"},
    ]
    notify(test_purchases, budget_remaining=303.02)
