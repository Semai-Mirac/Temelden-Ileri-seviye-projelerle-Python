email = input().strip()

# 1) '@' karakteri var mı? (True/False)
# TODO: bool değerini üret (ipucu: 'in' operatörü)
has_at = "@" in email
print(has_at)

# 2) Domain kısmını yazdır ('@' karakterinden sonrası)
# TODO: '@' yoksa domain'i boş yazdırmayı düşünebilirsin
domain = email.split("@", 1)[1] if has_at else ""
print(domain)

# 3) E-postayı küçük harfe çevirip yazdır
# TODO: email'i küçük harfe çevir (örn: lower()) ve yazdır
print(email.lower())
