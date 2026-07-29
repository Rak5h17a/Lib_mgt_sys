from app.domain.members import Member,StudentMember,FacultyMember

def member_from_dict(data:dict)-> Member:

    member_type=data.get("type")

    if member_type == "student":
        member=StudentMember(name=data["name"], member_id=data["member_id"])
    elif member_type == "faculty":
        member=FacultyMember(name=data["name"], member_id=data["member_id"])
    else:
        raise ValueError(f"Unknown member type: {member_type!r}")

    #restore borrowed list ,constructor starts as empty
    member._borrowed_item_ids = list(data.get("borrowed_item_ids", []))
    return member