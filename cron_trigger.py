import sys

sys.path.insert(0, "/root/grocerymind")

from scripts.consumption import calculate_days_left
from scripts.scraper import search_price
from scripts.purchaser import mock_purchase
from scripts.notifier import notify


def run_grocery_check():
    print("\n" + "=" * 50)
    print("🤖 GroceryMind Agent Starting...")
    print("=" * 50)

    # Step 1: Check pantry
    print("\n📦 STEP 1: Checking pantry levels...")
    low_items = calculate_days_left()

    if not low_items:
        print("✅ All items well stocked! Nothing to buy.")
        return

    # Step 2: Find best prices
    print(f"\n🔍 STEP 2: Finding best prices for {len(low_items)} items...")
    shopping_list = []

    for item in low_items:
        best_deal = search_price(item["name"])
        if best_deal:
            shopping_list.append(
                {
                    "key": item["key"],
                    "item": item["name"],
                    "price": best_deal["price"],
                    "store": best_deal["store"],
                }
            )
        else:
            # fallback to avg_price if scraper fails
            shopping_list.append(
                {
                    "key": item["key"],
                    "item": item["name"],
                    "price": item["avg_price"],
                    "store": item["preferred_store"],
                }
            )

    # Step 3: Mock purchase all items
    print(f"\n🛒 STEP 3: Purchasing {len(shopping_list)} items...")
    purchases = []
    final_budget = 400

    for s in shopping_list:
        result = mock_purchase(s["key"], s["item"], s["price"], s["store"])
        purchases.append(
            {
                "item": s["item"],
                "price": s["price"],
                "store": s["store"],
            }
        )
        final_budget = result["budget_remaining"]

    # Step 4: Send Telegram notification
    print("\n📱 STEP 4: Sending Telegram receipt...")
    notify(purchases, budget_remaining=final_budget)

    # Summary
    total = sum(p["price"] for p in purchases)
    print("\n" + "=" * 50)
    print("✅ GroceryMind Run Complete!")
    print(f"   Items purchased: {len(purchases)}")
    print(f"   Total spent: €{total:.2f}")
    print(f"   Budget remaining: €{final_budget:.2f}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_grocery_check()
