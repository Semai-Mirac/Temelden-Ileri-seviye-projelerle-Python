import time

n = int(input())

# Başlangıç zamanını kaydet.
baslangic = time.time()

# n x n boyutunda, elemanları 1 olan iki matris oluştur.
A = [[1] * n for _ in range(n)]
B = [[1] * n for _ in range(n)]

# Üçlü döngü ile matris çarpımını hesapla.
C = [[0] * n for _ in range(n)]
for satir in range(n):
    for sutun in range(n):
        for ortak_indeks in range(n):
            C[satir][sutun] += A[satir][ortak_indeks] * B[ortak_indeks][sutun]

# Geçen süreyi hesapla ve dört ondalık basamakla yazdır.
sure = time.time() - baslangic
print(f"{sure:.4f}")
