class Task:
    def __init__(self, title, priority, completed=False):
        self.title = title
        self.priority = priority
        self.completed = completed

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Görev başlığı boş olamaz.")
        self._title = value.strip()

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError("Öncelik pozitif bir tam sayı olmalıdır.")
        self._priority = value

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, value):
        if not isinstance(value, bool):
            raise ValueError("Tamamlanma durumu True veya False olmalıdır.")
        self._completed = value

    def calculate_score(self):
        return 0 if self.completed else self.priority * 10

    def __str__(self):
        status = "Tamamlandi" if self.completed else "Tamamlanmadi"
        return f"{self.title} | Oncelik: {self.priority} | Durum: {status}"


class TaskReport:
    def __init__(self, tasks):
        if not all(isinstance(task, Task) for task in tasks):
            raise TypeError("Rapor sadece Task nesnelerinden olusmalidir.")
        self._tasks = tuple(tasks)

    def create_summary(self):
        completed_count = sum(task.completed for task in self._tasks)
        total_score = sum(task.calculate_score() for task in self._tasks)

        return {
            "total_score": total_score,
            "completed_count": completed_count,
            "incomplete_count": len(self._tasks) - completed_count,
        }

    def __str__(self):
        summary = self.create_summary()
        return (
            f"Toplam skor: {summary['total_score']}\n"
            f"Tamamlanan gorev: {summary['completed_count']}\n"
            f"Tamamlanmayan gorev: {summary['incomplete_count']}"
        )


if __name__ == "__main__":
    task_data = [
        {"title": "Rapor hazirla", "priority": 3, "completed": False},
        {"title": "Sunum yap", "priority": 5, "completed": True},
    ]

    tasks = [Task(**data) for data in task_data]
    report = TaskReport(tasks)

    for task in tasks:
        print(task)
    print(report)