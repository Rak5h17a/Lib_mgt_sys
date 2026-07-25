from app.domain.items import LibraryItem,Book,Magazine,DVD

def item_from_dict(data: dict) -> LibraryItem:
    item_type=data.get("type")

    if item_type =="book":
        item = Book(
            title=data["title"],
            total_copies=data["total_copies"],
            author=data["author"],
            isbn=data["isbn"],
        )
    elif item_type=="magazine":
        item= Magazine(
            title=data["title"],
            total_copies=data["total_copies"],
            issue_number=data["issue_number"],
        )
    elif item_type=="dvd":
        item=DVD(
            title=data["title"],
            total_copies=data["total_copies"],
            runtime_minutes=data["runtime_minutes"],
        )
    else:
        raise ValueError(f"Unknown item type: {item_type}")

    item._available_copies=data["available_copies"]
    return item