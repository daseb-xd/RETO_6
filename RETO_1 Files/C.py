def listar_primos(lista) -> list:
    lista_p = []
    for i in lista:
        try:
            n = int(i)
        except ValueError:
            raise ValueError(f"{i} no es un número válido.")
        if n < 2:
            continue
        es_primo = True 
        for j in range(2, int(n ** 0.5 + 1)):
            if n % j == 0:
                es_primo = False
                break
        if es_primo:
            lista_p.append(n)
    return lista_p

if __name__=="__main__":
    lista = input("Ingrese la lista de números a evaluar, separados por espacios:").split()
    print("Primos:",listar_primos(lista))
    
