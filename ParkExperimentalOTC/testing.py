import numpy

a = "540234f865d1e29c13ab9d723520ea6a".encode('utf-8')
b = "7cf83529eaf086507b85f5a483b5ba3b".encode('utf-8')

a = int(a, 16)
b = int(b, 16)
print(a | b)