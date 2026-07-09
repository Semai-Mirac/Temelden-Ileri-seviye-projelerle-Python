class Payment:
    def pay(self, amount):
        print("Ödeme yöntemi belirsiz")

class CardPayment(Payment):
    def pay(self, amount):
        print(f"Kart ile {amount} TL ödendi")

class TransferPayment(Payment):
    def pay(self, amount):
        print(f"Havale ile {amount} TL ödendi")

if __name__ == "__main__":
    try:
        amount_input = int(input())
    except ValueError:
        amount_input = 250

    card_pay = CardPayment()
    transfer_pay = TransferPayment()

    card_pay.pay(amount_input)
    transfer_pay.pay(amount_input)