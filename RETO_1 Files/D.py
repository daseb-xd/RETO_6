def main():
    try:
        lista = list(map(int, input("Ingrese los números ENTEROS a evaluar, separados por espacios\n").split()))
    except ValueError:
        raise ValueError("Todos los valores deben ser números enteros.")

    lista_s = []

    for i, e in enumerate(lista):
        if i == len(lista) - 1:
            continue
        lista_s.append(e + lista[i + 1])

    print("La suma mas grande entre dos numeros consecutivos es:", max(lista_s))

if __name__ == "__main__":
    main()
