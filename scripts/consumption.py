import json
from pathlib import Path

PANTRY_FILE = Path("/root/grocerymind/data/pantry.json")


def calculate_days_left():
    with open(PANTRY_FILE) as f:
        pantry = json.load(f)

    low_items = []
    print("\n🧺 GroceryMind Pantry Check")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━")

    for key, item in pantry["items"].items():
        days = round(item["quantity"] / item["daily_consumption"], 1)
        item["days_left"] = days

        if days <= 1:
            status = "🔴 CRITICAL"
            low_items.append({"key": key, **item})
        elif days <= item["threshold_days"]:
            status = "🟡 LOW"
            low_items.append({"key": key, **item})
        else:
            status = "🟢 OK"

        print(f"{status} {item['name']}: {days} days left")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"⚠️  {len(low_items)} item(s) need restocking\n")

    with open(PANTRY_FILE, "w") as f:
        json.dump(pantry, f, indent=2)

    return low_items


if __name__ == "__main__":
    items = calculate_days_left()
    print("Items to restock:")
    for item in items:
        print(f"  → {item['name']} ({item['days_left']} days left)")
