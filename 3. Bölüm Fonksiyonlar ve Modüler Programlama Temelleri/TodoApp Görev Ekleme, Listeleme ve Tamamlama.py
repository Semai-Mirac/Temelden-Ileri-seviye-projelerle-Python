class TodoApp:
    def __init__(self):
        self.tasks = []

    def add_task(self, title):
        # TODO: {"title": title, "completed": False} sözlüğü ekle
        self.tasks.append({"title": title, "completed": False})

    def complete_task(self, title):
        # TODO: title'a uyan görevi bul ve completed=True yap
        # bulunamazsa "Görev bulunamadı" yazdır
        for task in self.tasks:
            if task["title"] == title:
                task["completed"] = True
                return
        print("Görev bulunamadı")

    def list_tasks(self):
        # TODO: her görev için "✅ title" veya "⬜ title" yazdır
        for task in self.tasks:
            status = "✅" if task["completed"] else "⬜"
            print(f"{status} {task['title']}")

app = TodoApp()
app.add_task("Kod yaz")
app.add_task("Test yaz")
app.add_task("Dokümantasyon hazırla")
app.complete_task("Kod yaz")
app.list_tasks()