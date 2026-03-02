import json
from datetime import date
from pathlib import Path

PANTRY_FILE = Path("/root/grocerymind/data/pantry.json")
BUDGET_FILE = Path("/root/grocerymind/data/budget.json")


def mock_purchase(item_key: str, item_name: str, price: float, store: str):
    print(f"\n🛒 Purchasing: {item_name} from {store} at €{price:.2f}")

    # Update pantry - restock to 14 days
    with open(PANTRY_FILE) as f:
        pantry = json.load(f)

    if item_key in pantry["items"]:
        item = pantry["items"][item_key]
        item["days_left"] = 14
        item["quantity"] = round(item["daily_consumption"] * 14, 2)
        item["preferred_store"] = store

    with open(PANTRY_FILE, "w") as f:
        json.dump(pantry, f, indent=2)

    # Update budget
    with open(BUDGET_FILE) as f:
        budget = json.load(f)

    budget["spent_this_month"] = round(budget["spent_this_month"] + price, 2)
    budget["remaining"] = round(
        budget["monthly_budget"] - budget["spent_this_month"], 2
    )

    budget["transactions"].append(
        {
            "date": str(date.today()),
            "items": [item_name],
            "total": price,
            "store": store,
            "auto_purchased": True,
        }
    )

    with open(BUDGET_FILE, "w") as f:
        json.dump(budget, f, indent=2)

    print(f"  ✅ Pantry restocked to 14 days")
    print(
        f"  💰 Budget remaining: €{budget['remaining']:.2f} / €{budget['monthly_budget']}"
    )

    return {
        "item": item_name,
        "price": price,
        "store": store,
        "budget_remaining": budget["remaining"],
    }


if __name__ == "__main__":
    result = mock_purchase("milk", "Milk", 1.50, "Rewe")
    print(f"\n✅ Purchase complete: {result}")
