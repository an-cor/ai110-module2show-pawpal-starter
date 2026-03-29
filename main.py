from pawpal_system import Task, Pet, Owner, Scheduler


def print_schedule(tasks):
    """Prints the daily schedule in a readable format."""
    WIDTH = 50
    print()
    print("=" * WIDTH)
    print("PAWPAL+  —  TODAY'S SCHEDULE".center(WIDTH))
    print("=" * WIDTH)

    if not tasks:
        print("  No tasks scheduled for today.")
        print("=" * WIDTH)
        return

    for task in tasks:
        status  = "DONE" if task.completed else "TODO"
        repeat  = f"repeats {task.frequency}" if task.is_recurring() else "one-time"
        pet     = task.pet_name or "Unknown"

        print(f"  {task.time}   {task.title}")
        print(f"         Pet      : {pet}")
        print(f"         Duration : {task.duration_minutes} min")
        print(f"         Priority : {task.priority}")
        print(f"         Repeat   : {repeat}")
        print(f"         Status   : {status}")
        print("-" * WIDTH)

    print()


def main():
    """Sets up sample data, builds a schedule, and prints it."""

    # --- Create owner ---
    owner = Owner(name="Alex")

    # --- Create pets ---
    mochi = Pet(name="Mochi", species="Dog", age=3)
    luna = Pet(name="Luna", species="Cat", age=5, notes="Shy around strangers")

    # --- Add tasks to Mochi ---
    mochi.add_task(Task(
        title="Morning Walk",
        duration_minutes=30,
        priority="high",
        time="07:30",
        frequency="daily",
    ))
    mochi.add_task(Task(
        title="Feed Breakfast",
        duration_minutes=10,
        priority="high",
        time="08:00",
    ))

    # --- Add tasks to Luna ---
    luna.add_task(Task(
        title="Feed Breakfast",
        duration_minutes=5,
        priority="high",
        time="08:00",
    ))
    luna.add_task(Task(
        title="Clean Litter Box",
        duration_minutes=10,
        priority="medium",
        time="09:30",
        frequency="daily",
    ))
    luna.add_task(Task(
        title="Vet Appointment",
        duration_minutes=60,
        priority="high",
        time="14:00",
        frequency="once",
    ))

    # --- Register pets with owner ---
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # --- Build schedule ---
    scheduler = Scheduler()
    schedule = scheduler.build_daily_schedule(owner)

    # --- Print schedule ---
    print_schedule(schedule)

    # --- Conflict check ---
    conflicts = scheduler.detect_conflicts(schedule)
    if conflicts:
        print("  CONFLICTS DETECTED:")
        for warning in conflicts:
            print(f"  !! {warning}")
        print("=" * 50)
        print()


if __name__ == "__main__":
    main()
