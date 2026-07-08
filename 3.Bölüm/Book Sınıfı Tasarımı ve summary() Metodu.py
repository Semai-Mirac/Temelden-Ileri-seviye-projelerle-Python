class Book:
    def __init__(self, title, author):
        # TODO: title ve author'u kaydet
        self.title = title
        self.author = author

    def summary(self):
        # TODO: "title - author" formatında string döndür
        return f"{self.title} - {self.author}"

# TODO: 2 kitap nesnesi oluştur ve summary() metodlarını yazdır
book1 = Book("Sefiller", "Victor Hugo")
book2 = Book("Suç ve Ceza", "Fyodor Dostoyevski")

print(book1.summary())
print(book2.summary())