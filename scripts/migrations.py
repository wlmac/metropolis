from django.contrib.auth.models import Group

from core.models import User


def migrate_groups():
    owner_group, _ = Group.objects.get_or_create(name="Org Owners")
    execs_group, _ = Group.objects.get_or_create(name="Execs")
    supervisor_group, _ = Group.objects.get_or_create(name="Supervisors")
    count = {
        "exec": {"added": 0, "removed": 0},
        "supervisor": {"added": 0, "removed": 0},
        "owner": {"added": 0, "removed": 0},
        "staff": {"added": 0, "removed": 0},
    }
    for user in User.objects.all():
        if user.is_teacher:
            if not user.is_staff:
                user.is_staff = True
                user.save()
                count["staff"]["added"] += 1
            if user.organizations_supervising.count() >= 1:
                if not user.groups.filter(name="Supervisors").exists():
                    user.groups.add(supervisor_group)
                    count["supervisor"]["added"] += 1
            else:
                if user.groups.filter(name="Supervisors").exists():
                    user.groups.remove(supervisor_group)
                    count["supervisor"]["removed"] += 1
        else:
            if user.groups.filter(name="Supervisors").exists():
                user.groups.remove(supervisor_group)
                count["supervisor"]["removed"] += 1
        if user.organizations_leading.count() >= 1:
            if not user.is_staff:
                user.is_staff = True
                user.save()
                count["staff"]["added"] += 1
            if not user.groups.filter(name="Execs").exists():
                user.groups.add(execs_group)
                count["exec"]["added"] += 1
        else:
            if all([user.is_staff, not user.is_superuser, not user.is_teacher]):
                user.is_staff = False
                user.save()
                count["staff"]["removed"] += 1
            if user.groups.filter(name="Execs").exists():
                user.groups.remove(execs_group)
                count["exec"]["removed"] += 1
        if user.organizations_owning.count() >= 1:
            if not user.is_staff:
                user.is_staff = True
                user.save()
                count["staff"]["added"] += 1
            if not user.groups.filter(name="Org Owners").exists():
                user.groups.add(owner_group)
                count["owner"]["added"] += 1
        else:
            if user.organizations_leading.count() == 0:
                if all([user.is_staff, not user.is_superuser, not user.is_teacher]):
                    user.is_staff = False
                    user.save()
                    count["staff"]["removed"] += 1
            if user.groups.filter(name="Org Owners").exists():
                user.groups.remove(owner_group)
                count["owner"]["removed"] += 1
    print(f"Added {count['exec']['added']} users to execs group")
    print(f"Removed {count['exec']['removed']} users from execs group")
    print(f"Added {count['owner']['added']} users to owners group")
    print(f"Removed {count['owner']['removed']} users from owners group")
    print(f"Added {count['supervisor']['added']} users to supervisors group")
    print(f"Removed {count['supervisor']['removed']} users from supervisors group")
    print(f"Added {count['staff']['added']} users to staff")
    print(f"Removed {count['staff']['removed']} users from staff")

    print("total in execs group: " + str(execs_group.user_set.count()))
    print("total in owners group: " + str(owner_group.user_set.count()))
    print("total in supervisors group: " + str(supervisor_group.user_set.count()))
    print("total staff: " + str(User.objects.filter(is_staff=True).count()) + "\n")
