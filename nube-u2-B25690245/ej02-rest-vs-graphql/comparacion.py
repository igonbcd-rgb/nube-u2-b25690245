import requests
import time


# ============================================================
# CONFIGURACIÓN
# ============================================================

POKEMONES = [
    "pikachu",
    "charizard",
    "bulbasaur",
    "squirtle",
    "gengar",
    "eevee",
    "snorlax",
    "lucario",
    "greninja",
    "mewtwo"
]

REST_URL = "https://pokeapi.co/api/v2/pokemon"

GRAPHQL_URL = "https://graphql.pokeapi.co/v1beta2"


# ============================================================
# REST
# ============================================================

def consumir_rest(pokemones):
    resultados = []
    bytes_total = 0

    t0 = time.perf_counter()

    for nombre in pokemones:

        r = requests.get(
            f"{REST_URL}/{nombre}",
            timeout=10
        )

        r.raise_for_status()

        datos = r.json()

        resultados.append({
            "nombre": datos["name"],
            "altura": datos["height"],
            "peso": datos["weight"]
        })

        bytes_total += len(r.content)

    tiempo_ms = (time.perf_counter() - t0) * 1000

    return resultados, tiempo_ms, bytes_total


# ============================================================
# GRAPHQL
# ============================================================

def consumir_graphql(pokemones):

    # Se construye una consulta con los 10 Pokémon
    campos = []

    for i, nombre in enumerate(pokemones):
        campos.append(f"""
        p{i}: pokemon(where: {{name: {{_eq: "{nombre}"}}}}) {{
            name
            height
            weight
        }}
        """)

    query = """
    query {
        """ + "\n".join(campos) + """
    }
    """

    t0 = time.perf_counter()

    r = requests.post(
        GRAPHQL_URL,
        json={"query": query},
        timeout=10
    )

    tiempo_ms = (time.perf_counter() - t0) * 1000

    r.raise_for_status()

    datos = r.json()

    bytes_total = len(r.content)

    resultados = []

    for i in range(len(pokemones)):
        pokemon = datos["data"][f"p{i}"]

        if pokemon:
            resultados.extend(pokemon)

    return resultados, tiempo_ms, bytes_total


# ============================================================
# EJECUCIÓN
# ============================================================

print("=" * 60)
print("COMPARACIÓN REST vs GRAPHQL")
print("=" * 60)

print(f"\nPokémon consultados: {len(POKEMONES)}")

# REST
rest_datos, rest_ms, rest_bytes = consumir_rest(POKEMONES)

# GraphQL
graphql_datos, graphql_ms, graphql_bytes = consumir_graphql(POKEMONES)


# ============================================================
# RESULTADOS
# ============================================================

print("\n" + "-" * 60)
print("REST")
print("-" * 60)

print(f"Peticiones HTTP: {len(POKEMONES)}")
print(f"Tiempo total:    {rest_ms:.0f} ms")
print(f"Tamaño total:    {rest_bytes} bytes")


print("\n" + "-" * 60)
print("GRAPHQL")
print("-" * 60)

print("Peticiones HTTP: 1")
print(f"Tiempo total:    {graphql_ms:.0f} ms")
print(f"Tamaño total:    {graphql_bytes} bytes")


# ============================================================
# COMPARACIÓN
# ============================================================

print("\n" + "=" * 60)
print("COMPARACIÓN")
print("=" * 60)

print(f"REST:    {rest_ms:.0f} ms")
print(f"GraphQL: {graphql_ms:.0f} ms")

print()

if rest_ms < graphql_ms:
    print("REST fue más rápido.")
elif graphql_ms < rest_ms:
    print("GraphQL fue más rápido.")
else:
    print("Ambos tuvieron el mismo tiempo.")

print()

print(f"REST:    {rest_bytes} bytes")
print(f"GraphQL: {graphql_bytes} bytes")