from django.contrib.auth.models import Group

from core.models import User


def migrate_groups():
    owner_group, _ = Group.objects.get_or_create(name="Org Owners")
    execs_group, _ = Group.objects.get_or_create(name="Execs")
    count_exec = {"added": 0, "removed": 0}
    count_leading = {"added": 0, "removed": 0}
    staffs = {"added": 0, "removed": 0}
    for user in User.objects.all():
        if user.is_teacher and not user.is_staff:
            user.is_staff = True
            user.save()
            staffs["added"] += 1
        if user.organizations_leading.count() >= 1:
            if not user.is_staff:
                user.is_staff = True
                user.save()
                staffs["added"] += 1
            if not user.groups.filter(name="Execs").exists():
                user.groups.add(execs_group)
                count_exec["added"] += 1
        else:
            if all([user.is_staff, not user.is_superuser, not user.is_teacher]):
                user.is_staff = False
                user.save()
                staffs["removed"] += 1
            if user.groups.filter(name="Execs").exists():
                user.groups.remove(execs_group)
                count_exec["removed"] += 1
        if user.organizations_owning.count() >= 1:
            if not user.is_staff:
                user.is_staff = True
                user.save()
                staffs["added"] += 1
            if not user.groups.filter(name="Org Owners").exists():
                user.groups.add(owner_group)
                count_leading["added"] += 1
        else:
            if user.organizations_leading.count() == 0:
                if all([user.is_staff, not user.is_superuser, not user.is_teacher]):
                    user.is_staff = False
                    user.save()
                    staffs["removed"] += 1
            if user.groups.filter(name="Org Owners").exists():
                user.groups.remove(owner_group)
                count_leading["removed"] += 1
    print(f"Added {count_exec['added']} users to execs group")
    print(f"Removed {count_exec['removed']} users from execs group")
    print(f"Added {count_leading['added']} users to owners group")
    print(f"Removed {count_leading['removed']} users from owners group")
    print(f"Added {staffs['added']} users to staff")
    print(f"Removed {staffs['removed']} users from staff")

    print("total in execs group: " + str(execs_group.user_set.count()))
    print("total in owners group: " + str(owner_group.user_set.count()))
    print("total staff: " + str(User.objects.filter(is_staff=True).count()) + "\n")
