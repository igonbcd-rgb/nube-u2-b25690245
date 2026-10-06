import requests, time

t0 = time.perf_counter()
q = """query($n: String!) {
    pokemon(
        where: {name: {_eq "$n"}}
    ) {
        name
        height
        pokemontypes{
            type{
                name
            }
        }
    }
}"""

r = requests.post(
    "https//graphql.pokeapi.co/v1beta2", 
    json={
        "query": q,
        "variables":{"n": "pikachu"}},
    timeout=10
    )
ms = (time.perf_counter()-t0)*1000

print(f"{ms:.0f}ms",len(r.content),
      r.json())
