
# numero_inteiro = 10

# string1 = 'ola'
# string2 = "ola"

# n = input("Digite algo:")
# print(n)  # saída: tipo string (mesmo se forem números)


# print(type(n))
a = 5
b = 5
# n = int(input("Qual a sua idade:"))
# #Capturar um número e convertê-lo para um inteiro

# altura = float(input("Digite sua altura: "))
# print(f"Sua altura é {altura} metros.")

# altura = float(input("Digite sua altura: "))
# print(f"Sua altura é {altura} metros.")
# #Capturar um número e convertê-lo para um ponto flutuante


print("Operadores Aritméticos")
print("a + b =", a + b)  # Adição
print("a - b =", a - b)  # Subtração
print("a * b =", a * b)  # Multiplicação
print("a / b =", a / b)  # Divisão
print("a % b =", a % b)  # Módulo
print("a ** b =", a ** b)  # Exponenciação
print("a // b =", a // b)  # Divisão inteira


# Operadores de Comparação


print("=" * 20) 

a = 10
b = 20
# Igualdade
print("a == b ->", a == b)  # False, porque 10 não é igual a 20

# Diferença
print("a != b ->", a != b)  # True, porque 10 é diferente de 20

# Maior que
print("a > b ->", a > b)  # False, porque 10 não é maior que 20

# Menor que
print("a < b ->", a < b)  # True, porque 10 é menor que 20



a = 20
b = 20

if a < b: 
    print("a é menor que b")
elif a == b:
    print("a é igual a b")  
    # Este bloco será executado porque 20 é igual a 20
else:
    print("a é maior que b")


idade = 25

if (idade < 13):
    print("Você é uma criança.")
elif idade < 20:
    print("Você é um adolescente.")
elif idade < 60:
    print("Você é um adulto.")
else:
    print("Você é um idoso.")

n1 = float(input("Digite a nota 1:"))
n2 = float(input("Digite a nota 2:"))
n3 = float(input("Digite a nota 3:"))
media = (n1+n2+n3) /3
print(f"Sua media é de {media:.2f}")

if media > 7:
    print("Aprovado")
elif media <= 7 and media >=4:
    print("Recuperação")
else:
    print("Reprovado")

