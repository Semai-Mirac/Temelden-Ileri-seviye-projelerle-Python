class Task:
    def __init__(self, title: str, completed: bool = False):
        """
        Task sınıfı başlatıcı metodu.
        
        :param title: Görev başlığı
        :param completed: Tamamlanma durumu (varsayılan: False)
        """
        self.title = title
        self.completed = completed

    def __str__(self) -> str:
        """
        Görevi okunabilir bir dize formatında döndürür.
        """
        status = "✅" if self.completed else "⬜"
        return f"{status} {self.title}"


# 2 adet Task nesnesi oluşturma
task1 = Task("Kodu yaz", completed=True)
task2 = Task("Testi geç", completed=False)

# Nesnelerin print() ile yazdırılması
print(task1)
print(task2)