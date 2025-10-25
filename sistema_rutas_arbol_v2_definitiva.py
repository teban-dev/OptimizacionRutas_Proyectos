# ---------------------------------------------------------
# SISTEMA DE OPTIMIZACIÓN DE RUTAS EN ENVÍOS - VERSIÓN 2 DEFINITIVA
# Implementación con Árboles (BigTree)
#
# Integrantes del grupo:
# - Juan David Ortiz Ochoa (2242038)
# - Juan Esteban Gomez Ayala (2243465)
# - Ángel Sierra (2242007)
# Profesora: Nury Farelo
# Fecha: 24/10/2025
# ---------------------------------------------------------

# Instalación automática para Google Colab
#!pip install -U bigtree

from bigtree import Node, print_tree

# =========================================================
# CLASE PRINCIPAL DE LA RED DE RUTAS
# =========================================================
class RedDeRutasTree:
    def __init__(self):
        # Nodo raíz de la red
        self.raiz = Node("Centro_Distribucion")

    # Método auxiliar: buscar nodo por nombre (recursivo)
    def buscar_nodo(self, nodo, nombre):
        if nodo.name == nombre:
            return nodo
        for hijo in nodo.children:
            encontrado = self.buscar_nodo(hijo, nombre)
            if encontrado:
                return encontrado
        return None

    # 1. Se verifica si la red está vacía
    def esta_vacia(self):
        return len(self.raiz.children) == 0

    # 2. Se cuenta las ubicaciones (excluyendo la raíz)
    def contar_ubicaciones(self):
        return len(list(self.raiz.descendants))

    # 3. Se muestra la red completa
    def mostrar_red(self):
        print("\n--- Red de Rutas de Envío ---")
        print_tree(
            self.raiz,
            attr_list=["distancia"],
            all_attrs=False
        )
        print("-----------------------------------\n")

    # 4. Se Agrega una ubicación (sin conexión todavía)
    def agregar_ubicacion(self, nombre):
        existente = self.buscar_nodo(self.raiz, nombre)
        if existente:
            print(f"La ubicación '{nombre}' ya existe en la red.")
            return
        Node(nombre, parent=self.raiz)
        print(f"Ubicación '{nombre}' agregada al árbol principal.")

    # 5. Se Agrega una ruta entre ubicaciones
    def agregar_ruta(self, origen, destino, distancia):
        nodo_origen = self.buscar_nodo(self.raiz, origen)
        nodo_destino = self.buscar_nodo(self.raiz, destino)

        if not nodo_origen:
            print(f"No existe la ubicación de origen '{origen}'.")
            return

        if nodo_destino:
            print(f"La ubicación destino '{destino}' ya existe en la red.")
            return

        Node(destino, parent=nodo_origen, distancia=distancia)
        print(f"Ruta agregada: {origen} → {destino} ({distancia} Km)")

    # 6️. Se busca una ubicación
    def buscar_ubicacion(self, nombre):
        nodo = self.buscar_nodo(self.raiz, nombre)
        if nodo:
            print(f"Ubicación encontrada: {nodo.name}")
            if hasattr(nodo, "distancia") and nodo.distancia is not None:
                print(f"Distancia desde el origen: {nodo.distancia} Km")
        else:
            print("Ubicación no encontrada en la red.")

    # 7️. Se muestran ubicaciones ordenadas alfabéticamente
    def ordenar_ubicaciones(self):
        ubicaciones = sorted([n.name for n in self.raiz.descendants])
        print("\nUbicaciones ordenadas alfabéticamente:")
        for nombre in ubicaciones:
            print(f" - {nombre}")
        print()
    # 8. Encontrar la ruta más corta entre dos ubicaciones
    def ruta_mas_corta(self, origen, destino):
        nodo_origen = self.buscar_nodo(self.raiz, origen)
        nodo_destino = self.buscar_nodo(self.raiz, destino)

        if not nodo_origen or not nodo_destino:
            print("Una o ambas ubicaciones no existen en la red.")
            return

        # Obtener rutas desde la raíz hasta cada nodo
        camino_origen = list(nodo_origen.ancestors) + [nodo_origen]
        camino_destino = list(nodo_destino.ancestors) + [nodo_destino]

        # Encontrar el ancestro común más cercano
        ancestro_comun = None
        for n1, n2 in zip(camino_origen, camino_destino):
            if n1 == n2:
                ancestro_comun = n1
            else:
                break

        # Ruta total = origen - ancestro_común - destino
        ruta = []
        distancia_total = 0

        # Subir desde el origen hasta el ancestro común
        nodo_actual = nodo_origen
        while nodo_actual != ancestro_comun:
            ruta.append(nodo_actual.name)
            distancia_total += getattr(nodo_actual, "distancia", 0)
            nodo_actual = nodo_actual.parent

        ruta.append(ancestro_comun.name)
        ruta.reverse()

        # Bajar desde el ancestro común hasta el destino
        nodo_actual = nodo_destino
        distancia_descenso = 0
        camino_descenso = []
        while nodo_actual != ancestro_comun:
            camino_descenso.append(nodo_actual.name)
            distancia_descenso += getattr(nodo_actual, "distancia", 0)
            nodo_actual = nodo_actual.parent

        ruta.extend(camino_descenso)
        distancia_total += distancia_descenso

        print(f"\nRuta más corta entre '{origen}' y '{destino}':")
        print(" → ".join(ruta))
        print(f"Distancia total aproximada: {distancia_total} Km\n")



# =========================================================
# MENÚ PRINCIPAL
# =========================================================
def menu():
    red = RedDeRutasTree()

    while True:
        print("""\
--- Sistema de Rutas de Envío (Versión 2 - Árboles) ---
1. Agregar ubicación (nodo suelto)
2. Agregar ruta entre ubicaciones
3. Mostrar red de rutas
4. Verificar si la red está vacía
5. Contar ubicaciones
6. Buscar ubicación
7. Mostrar ubicaciones ordenadas
8. Calcular ruta mas corta
9. Salir
""")

        opcion = input("Por favor seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre de la nueva ubicación: ")
            red.agregar_ubicacion(nombre)

        elif opcion == "2":
            origen = input("Ingrese el nombre de la ubicación de origen: ")
            destino = input("Ingrese el nombre de la ubicación de destino: ")
            try:
                distancia = float(input("Ingrese la distancia entre las ubicaciones (Km): "))
            except ValueError:
                print("La distancia debe ser un número válido.")
                continue
            red.agregar_ruta(origen, destino, distancia)

        elif opcion == "3":
            red.mostrar_red()

        elif opcion == "4":
            if red.esta_vacia():
                print("La red está vacía (solo el centro de distribución).")
            else:
                print("La red contiene ubicaciones registradas.")

        elif opcion == "5":
            print(f"Cantidad total de ubicaciones: {red.contar_ubicaciones()}")

        elif opcion == "6":
            nombre = input("Ingrese el nombre de la ubicación a buscar: ")
            red.buscar_ubicacion(nombre)

        elif opcion == "7":
            red.ordenar_ubicaciones()

        elif opcion == "8":
            origen = input("Ingrese la ubicación de origen: ")
            destino = input("Ingrese la ubicación de destino: ")
            red.ruta_mas_corta(origen, destino)


        elif opcion == "9":
            print("¡Bye bye!")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

# =========================================================
# EJECUCIÓN DEL PROGRAMA
# =========================================================
if __name__ == "__main__":
    menu()