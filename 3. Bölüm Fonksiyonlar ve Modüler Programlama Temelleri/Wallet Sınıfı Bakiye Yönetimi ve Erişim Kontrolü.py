class Wallet:
    def __init__(self, balance=0):
        self._balance = balance

    def deposit(self, miktar):
        # miktar pozitifse bakiyeye ekle
        if miktar > 0:
            self._balance += miktar

    def withdraw(self, miktar):
        # miktar negatifse veya bakiyeden fazlaysa "İşlem başarısız" yazdır
        if miktar < 0 or miktar > self._balance:
            print("İşlem başarısız")
        else:
            # aksi halde bakiyeden düş
            self._balance -= miktar

    def get_balance(self):
        return self._balance

baslangic = int(input())
w = Wallet(baslangic)

w.deposit(100)
w.deposit(100)
w.withdraw(50)

print(w.get_balance())