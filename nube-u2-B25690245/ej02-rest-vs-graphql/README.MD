## Ejercicio 2 rest vs graphql
Ambos códigos se entienden súper bien y cumplen con mostrar las diferencias clave entre REST y GraphQL usando PokéAPI.

Por un lado, REST te regresa toda la información del Pokémon completa con un buen de datos que ni necesitas, lo que termina haciendo la respuesta muy pesada. En cambio, con GraphQL tú eliges exactamente qué campos pedir (como nombre, altura, peso o tipos) y te ahorras un buen de ancho de banda.

El otro punto fuerte es la latencia: con REST tienes que hacer una petición HTTP por cada Pokémon, acumulando tiempo en cada ida y vuelta a la red. Con GraphQL mandas a traer todo en una sola petición a un único endpoint. Además, aprovechas los filtros de su esquema en Hasura usando variables para afinar las consultas.

Al final, GraphQL se lleva de gane cuando quieres optimizar datos y evitar tantas peticiones seguidas, mientras que REST sigue siendo la opción más directa y sencilla si solo ocupas hacer consultas individuales sin tanto lío.