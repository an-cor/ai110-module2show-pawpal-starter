# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest tests/
```

The tests cover:

Scheduling logic — tasks are sorted by time, and ties are broken by priority (high → medium → low)
Recurring tasks — completing a daily or weekly task automatically queues the next occurrence
Filtering & conflict detection — tasks can be filtered by pet or completion status, and overlapping time windows are flagged
Confidence Level: 4/5 — Core scheduling and task management behaviors are well covered. Edge cases like removing tasks and back-to-back conflict boundaries are tested too. The main gap is around the AI explanation features, which are harder to unit test.

## Smarter Scheduling

The scheduler does more than just list tasks — it organizes them in a way that makes sense for a real day:

- Tasks are sorted by time so the schedule runs in order from morning to night
- When two tasks are scheduled at the same time, the higher priority task goes first (high → medium → low)
- Conflict detection checks every pair of tasks and warns you if their time windows overlap
- Recurring tasks (daily or weekly) automatically create the next occurrence when marked complete

## UML representation of code

classDiagram
    class Owner {
        +str name
        +dict preferences
        +list pets
        +add_pet(pet)
        +get_pet(name)
        +get_all_tasks()
    }

    class Pet {
        +str name
        +str species
        +int age
        +str notes
        +list tasks
        +add_task(task)
        +remove_task(task_title)
        +get_tasks()
    }

    class Task {
        +str title
        +int duration_minutes
        +str priority
        +str time
        +str frequency
        +bool completed
        +mark_complete()
        +is_recurring()
    }

    class Scheduler {
        +build_daily_schedule(owner)
        +sort_tasks_by_time(tasks)
        +filter_tasks(tasks, completed, pet_name)
        +detect_conflicts(tasks)
        +explain_schedule(tasks)
    }

    Owner "1" --> "*" Pet : has
    Pet "1" --> "*" Task : has
    Scheduler --> Owner : reads from
    Scheduler --> Task : organizes