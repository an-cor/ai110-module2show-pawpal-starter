from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care activity."""
    title: str
    duration_minutes: int
    priority: str
    time: str
    frequency: str = "once"
    completed: bool = False
    pet_name: str = ""  # set when collected from an Owner; useful for filtering

    def mark_complete(self) -> None:
        """Sets the task as completed."""
        self.completed = True

    def is_recurring(self) -> bool:
        """Returns True if this task repeats (i.e. frequency is not 'once')."""
        return self.frequency != "once"


@dataclass
class Pet:
    """Stores a pet's details and its list of care tasks."""
    name: str
    species: str
    age: int = 0
    notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a task to this pet's task list and records which pet owns it."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> None:
        """Removes the first task whose title matches the given string."""
        self.tasks = [t for t in self.tasks if t.title != task_title]

    def get_tasks(self) -> List[Task]:
        """Returns all tasks belonging to this pet."""
        return self.tasks


@dataclass
class Owner:
    """Manages a collection of pets and their tasks."""
    name: str
    preferences: dict = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's pet list."""
        self.pets.append(pet)

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Returns the pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Collects and returns every task from every pet."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Builds and explains daily schedules for a pet owner."""

    def build_daily_schedule(self, owner: Owner) -> List[Task]:
        """Gathers all tasks from the owner and returns them sorted by time."""
        all_tasks = owner.get_all_tasks()
        return self.sort_tasks_by_time(all_tasks)

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts a list of tasks in ascending order by their 'HH:MM' time string."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(
        self,
        tasks: List[Task],
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filters tasks by completion status and/or pet name.

        Note: pet_name filtering works because Owner.get_all_tasks() stamps
        each task with its pet's name in the task.pet_name field.
        """
        result = tasks
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        if pet_name is not None:
            result = [t for t in result if t.pet_name == pet_name]
        return result

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Returns a warning for every pair of tasks whose time windows overlap.

        Two tasks conflict when one starts before the other finishes.
        Back-to-back tasks (one ends exactly when the next starts) are fine.
        """
        def to_minutes(time_str: str) -> int:
            """Convert 'HH:MM' to total minutes since midnight."""
            h, m = time_str.split(":")
            return int(h) * 60 + int(m)

        warnings = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                a, b = tasks[i], tasks[j]
                a_start = to_minutes(a.time)
                a_end   = a_start + a.duration_minutes
                b_start = to_minutes(b.time)
                b_end   = b_start + b.duration_minutes
                # Overlap exists when each interval starts before the other ends
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"Conflict: '{a.title}' ({a.pet_name}, {a.time}, {a.duration_minutes} min)"
                        f" overlaps '{b.title}' ({b.pet_name}, {b.time}, {b.duration_minutes} min)"
                    )
        return warnings

    def explain_schedule(self, tasks: List[Task]) -> List[str]:
        """Returns a plain-English explanation for why each task is in the schedule."""
        explanations = []
        for task in tasks:
            pet_label = f"for {task.pet_name}" if task.pet_name else ""
            recurrence = f"repeats {task.frequency}" if task.is_recurring() else "one-time"
            status = "already done" if task.completed else "pending"
            line = (
                f"{task.time} — '{task.title}' {pet_label} "
                f"({task.priority} priority, {task.duration_minutes} min, {recurrence}, {status})"
            )
            explanations.append(line)
        return explanations
