# Ej. 03 Servicio Integrador (Laboratorio 1)

## Objetivo
Desarrollar e integrar una API REST con FastAPI que consume servicios de clima (REST), datos de países (GraphQL) y persiste consultas en Supabase.

## Cómo ejecutarlo
```bash
cd ej03-integrador
pip install -r requirements.txt
uvicorn main:app --reload

## Resultados / mediciones

| Endpoint | Servicio | Fuente | Tiempo (ms) | Estado |
| :--- | :--- | :--- | :--- | :--- |
| /clima?ciudad=Ciudad Valles | Open-Meteo | API | ~230 ms | 200 OK |
| /clima?ciudad=Ciudad Valles | Open-Meteo | Caché | ~2 ms | 200 OK |
| /paises/MX | Countries | API | ~310 ms | 200 OK |
| /recomendacion | Supabase | DB | ~190 ms | 200 OK |
| /historial | Supabase | DB | ~150 ms | 200 OK |