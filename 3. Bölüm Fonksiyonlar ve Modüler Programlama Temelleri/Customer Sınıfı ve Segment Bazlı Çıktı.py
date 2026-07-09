class Customer:
    def __init__(self, name, segment):
        self.name = name
        self.segment = segment

    def __str__(self):
        return f"Ad: {self.name} - Segment: {self.segment}"

# TODO: 2 müşteri nesnesi oluştur
# "Ad: name - Segment: segment" formatında yazdır
customer1 = Customer("Ada Yılmaz", "Bireysel")
customer2 = Customer("Mert Kaya", "Ticari")

print(f"Ad: {customer1.name} - Segment: {customer1.segment}")
print(f"Ad: {customer2.name} - Segment: {customer2.segment}")