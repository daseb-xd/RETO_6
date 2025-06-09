def son_anagramas(lista) -> set:
    # Diccionario para agrupar palabras según sus letras ordenadas
    grupos = {}

    for palabra in lista:
        if palabra is None or palabra == "":
            raise ValueError("La palabra no puede ser None o una cadena vacía")
        else:
            palabra = palabra.lower()  # Convertir a minúsculas para comparar sin distinguir mayúsculas
            orden = "".join(sorted(palabra))  # Ordenar las letras de la palabra
            if orden in grupos:
                grupos[orden].append(palabra)  # Agregar palabra al grupo correspondiente
            else:
                grupos[orden] = [palabra]  # Crear nuevo grupo con la palabra

    anagramas = set()  # Conjunto para almacenar palabras que tienen al menos un anagrama

    for grupo in grupos.values():
        if len(grupo) > 1:  # Si hay más de una palabra en el grupo, son anagramas
            for i in grupo:
                anagramas.add(i)  # Agregar cada palabra del grupo al conjunto de anagramas

    return anagramas

if __name__ == "__main__":
    
    lista = input("Ingrese las palabras a evaluar, separadas por espacios:\n").split()
    print("Estos son los anagramas encontrados:\n", son_anagramas(lista))
