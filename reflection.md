# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design takes into account the pet, the owner, what's important for both of them and a structure to map this to a schedule.

- What classes did you include, and what responsibilities did you assign to each?

Classes:
- Pet: contains needs and attributes of pet
- Owner: needs to know pet. contains attributes of owner
- Calendar: Tracks dates and repetitions for pet. Tracks tasks and constraints for owner.
- Care Tasks: Pet tasks related to calendar like walks, feeding, meds, enrichment, grooming, etc.

Three core actions a user should be able to perform:
- Add a pet with pet care info
- Add events to a calendar with contraints and filter info
- View pet, personal and calendar info

**b. Design changes**

- Did your design change during implementation?

Yes.

- If yes, describe at least one change and why you made it.

Changed the classes "Calendar" to "Scheduler" and "Care Tasks" to "Tasks". 

I made this because I noticed that complexity was a lot higher by having the name "Calendar" as the class to handle scheduling. AI kept wanting to implement everything a calendar has to offer like a full date/time system but is not necessary for the scope of this project. Also having "Care Tasks" to just "Tasks" made this easier to implement. It a more well rounded term for its use case.

**Final Building Blocks**
**Owner**
- attributes: name, preferences, pets
- methods: add_pet(), get_pet(), get_all_tasks()

**Pet**
- attributes: name, species, age, notes, tasks
- methods: add_task(), remove_task(), get_tasks()

**Task**
- attributes: title, duration_minutes, priority, time, frequency, completed
- methods: mark_complete(), is_recurring()

**Scheduler**
- methods: build_daily_schedule(), sort_tasks_by_time(), filter_tasks(), detect_conflicts(), explain_schedule()


**UML representation of code**

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

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

My scheduler considers time and priority as its main goals. Everything is sorted from first to last in a day and highest priority to lowest. 

- How did you decide which constraints mattered most?

The outcome is what mattered most. The generated schedule had to make sense to a user. If the dates are all over the place, lower priority things are being shown first, the name of the pets are not showing or what a task is, then it doesn't make sense how to use this tool. Usability from a user perspective I think is what mattered most and drove my decisions. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

My original scheduler only checked for exact matching task times. Then filtered from highest priority to lowest. It had overlapping conflicts but the code did not have a conflict warning appear after generating a schedule. 

This was simpler to implement and explain but during testing, this missed overlapping tasks with different start times. So I improved the conflict detection to compare task durations as well.

This is the edge case that made it obvious.
Here is your schedule for today:
- 11:00 — 'Shower' for Mochi (medium priority, 61 min, repeats daily, pending)
- 11:30 — 'nap time' for Claus (medium priority, 60 min, repeats daily, pending)
- 12:00 — 'Morning walk' for Stinker (high priority, 60 min, repeats daily, pending)

- Why is that tradeoff reasonable for this scenario?

The simplicity is the trade off. A more understable scheduler adds complexity to the tool and the code but is far more usable and understable for a user. This tradeoff is reasonable because it is a small fix that has a large improvement on usability.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
