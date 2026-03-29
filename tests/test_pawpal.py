from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_sets_completed_to_true():
    task = Task(title="Morning Walk", duration_minutes=30, priority="high", time="07:30")

    # Task should start as not completed
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="Dog")
    task = Task(title="Feed Breakfast", duration_minutes=10, priority="high", time="08:00")

    assert len(pet.get_tasks()) == 0

    pet.add_task(task)

    assert len(pet.get_tasks()) == 1


def test_build_daily_schedule_sorts_tasks_by_time():
    owner = Owner(name="Alex")
    pet = Pet(name="Mochi", species="Dog")

    # Add tasks out of order
    pet.add_task(Task(title="Evening Walk",  duration_minutes=30, priority="medium", time="18:00"))
    pet.add_task(Task(title="Feed Breakfast", duration_minutes=10, priority="high",   time="08:00"))
    pet.add_task(Task(title="Midday Check",  duration_minutes=5,  priority="low",    time="12:00"))

    owner.add_pet(pet)

    schedule = Scheduler().build_daily_schedule(owner)

    assert schedule[0].time == "08:00"
    assert schedule[1].time == "12:00"
    assert schedule[2].time == "18:00"


def test_detect_conflicts_flags_overlapping_tasks():
    """Tasks whose windows overlap (but don't share an exact start time) are flagged."""
    scheduler = Scheduler()
    tasks = [
        # Shower runs 11:00 – 12:01 (61 min)
        Task(title="Shower",   duration_minutes=61, priority="high", time="11:00", pet_name="Mochi"),
        # nap time runs 11:30 – 12:30 — starts before Shower ends
        Task(title="nap time", duration_minutes=60, priority="low",  time="11:30", pet_name="Claus"),
    ]
    conflicts = scheduler.detect_conflicts(tasks)
    assert len(conflicts) == 1
    assert "Shower" in conflicts[0]
    assert "nap time" in conflicts[0]


def test_detect_conflicts_same_start_time():
    """Two tasks with the identical start time always overlap."""
    scheduler = Scheduler()
    tasks = [
        Task(title="Feed", duration_minutes=10, priority="high",   time="08:00", pet_name="Mochi"),
        Task(title="Walk", duration_minutes=20, priority="medium", time="08:00", pet_name="Mochi"),
    ]
    conflicts = scheduler.detect_conflicts(tasks)
    assert len(conflicts) == 1


def test_detect_conflicts_no_overlap():
    """Back-to-back tasks (one ends exactly when the next starts) are not a conflict."""
    scheduler = Scheduler()
    tasks = [
        # Morning walk: 08:00 – 09:00
        Task(title="Morning walk", duration_minutes=60, priority="high",   time="08:00", pet_name="Mochi"),
        # Lunch starts exactly at 09:00 — no overlap
        Task(title="Lunch",        duration_minutes=15, priority="medium", time="09:00", pet_name="Mochi"),
    ]
    conflicts = scheduler.detect_conflicts(tasks)
    assert len(conflicts) == 0
