# idade1 = int(input())
# idade2 = int(input())
# idade3 = int(input())
# # Coloca as idades numa lista
# idades = [idade1, idade2, idade3]
# # Se todas forem iguais, qualquer uma serve como idade de Camila
# if idade1 == idade2 == idade3:
#     camila = idade1
# else:
#     # Ordena para descobrir a idade do meio
#     idades.sort()
#     camila = idades[1]
# print(camila)

idade1 = int(input())
idade2 = int(input())
idade3 = int(input())

# Verifica qual é a idade do meio
if (idade1 >= idade2 and idade1 <= idade3) or (idade1 <= idade2 and idade1 >= idade3):
    camila = idade1
else:
    if (idade2 >= idade1 and idade2 <= idade3) or (idade2 <= idade1 and idade2 >= idade3):
        camila = idade2
    else:
        camila = idade3

print(camila)
