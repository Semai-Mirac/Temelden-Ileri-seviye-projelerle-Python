class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.name}: {self.price} TL"


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product: Product):
        self.items.append(product)

    def total(self) -> float:
        return sum(item.price for item in self.items)


class Order:
    def __init__(self, cart: Cart, status: str = "Beklemede"):
        self.cart = cart
        self.status = status

    def summarize(self):
        print(f"Sipariş toplamı: {self.cart.total()} TL - Durum: {self.status}")


if __name__ == "__main__":
    # Ürünleri tanımlıyoruz
    product1 = Product("Laptop", 300.0)
    product2 = Product("Mouse", 50.0)

    # Sepeti oluşturup ürünleri ekliyoruz
    cart = Cart()
    cart.add(product1)
    cart.add(product2)

    # Siparişi oluşturarak özetini yazdırıyoruz
    order = Order(cart)
    order.summarize()