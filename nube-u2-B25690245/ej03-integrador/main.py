import os
import time
from typing import Optional, Dict, Any
import requests
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno (.env)
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Faltan las variables SUPABASE_URL o SUPABASE_KEY en el archivo .env")

# Cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Instancia principal de FastAPI (ESTA ES LA VARIABLE QUE BUSCA UVICORN)
app = FastAPI(title="Servicio Integrador - Ejercicio 03", version="1.0.0")

# Sistema de Caché en memoria con TTL (5 min)
CACHE: Dict[str, Dict[str, Any]] = {}
TTL_SECONDS = 300

def get_from_cache(key: str) -> Optional[Any]:
    if key in CACHE:
        data, timestamp = CACHE[key]["data"], CACHE[key]["timestamp"]
        if time.time() - timestamp < TTL_SECONDS:
            return data
        else:
            del CACHE[key]
    return None

def set_in_cache(key: str, data: Any):
    CACHE[key] = {"data": data, "timestamp": time.time()}

# Petición HTTP con Timeout y 1 Reintento
def fetch_with_retry(url: str, method: str = "GET", json_data: dict = None, headers: dict = None, timeout: int = 5):
    for attempt in range(2):
        try:
            if method.upper() == "POST":
                response = requests.post(url, json=json_data, headers=headers, timeout=timeout)
            else:
                response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            if attempt == 1:
                raise HTTPException(status_code=504, detail=f"504 Gateway Timeout al conectar con {url}")
        except requests.exceptions.RequestException as e:
            if attempt == 1:
                raise HTTPException(status_code=502, detail=f"502 Bad Gateway: {str(e)}")
        time.sleep(1)

class RecomendacionInput(BaseModel):
    usuario_id: str
    categoria_preferida: str
    presupuesto_max: float

# --- ENDPOINTS ---

@app.get("/clima")
def obtener_clima(ciudad: str = Query(..., description="Nombre de la ciudad")):
    """1. REST - Clima (Open-Meteo)"""
    cache_key = f"clima:{ciudad.lower()}"
    cached_res = get_from_cache(cache_key)
    if cached_res:
        return {"origen": "cache", "data": cached_res}

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}&count=1&language=es&format=json"
    geo_data = fetch_with_retry(geo_url)
    
    if not geo_data.get("results"):
        raise HTTPException(status_code=404, detail=f"Ciudad '{ciudad}' no encontrada.")
    
    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]
    nombre_oficial = geo_data["results"][0]["name"]

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_data = fetch_with_retry(weather_url)
    
    resultado = {
        "ciudad": nombre_oficial,
        "coordenadas": {"latitud": lat, "longitud": lon},
        "clima_actual": weather_data.get("current_weather", {})
    }
    
    set_in_cache(cache_key, resultado)
    return {"origen": "api", "data": resultado}

@app.get("/paises/{codigo}")
def obtener_pais(codigo: str):
    """2. GraphQL - País (Countries API)"""
    codigo_upper = codigo.upper()
    cache_key = f"pais:{codigo_upper}"
    cached_res = get_from_cache(cache_key)
    if cached_res:
        return {"origen": "cache", "data": cached_res}

    query = """
    query GetCountry($code: ID!) {
      country(code: $code) {
        code
        name
        native
        capital
        currency
        emoji
        continent { name }
      }
    }
    """
    url = "https://countries.trevorblades.com/"
    respuesta = fetch_with_retry(url, method="POST", json_data={"query": query, "variables": {"code": codigo_upper}})
    
    pais_data = respuesta.get("data", {}).get("country")
    if not pais_data:
        raise HTTPException(status_code=404, detail=f"País con código '{codigo}' no encontrado.")
        
    set_in_cache(cache_key, pais_data)
    return {"origen": "api", "data": pais_data}

@app.post("/recomendacion")
def crear_recomendacion(datos: RecomendacionInput):
    """3. Guardar en Supabase"""
    recomendaciones_simuladas = [
        {"producto": "Laptop Gamer", "precio": 1500.0},
        {"producto": "Audífonos Bluetooth", "precio": 50.0}
    ]
    
    payload_insert = {
        "tipo": "recomendacion",
        "input_data": datos.model_dump_json(),
        "respuesta": str(recomendaciones_simuladas)
    }

    try:
        db_response = supabase.table("historial_consultas").insert(payload_insert).execute()
        return {
            "mensaje": "Recomendación guardada con éxito",
            "db_registro": db_response.data,
            "recomendaciones": recomendaciones_simuladas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar en Supabase: {str(e)}")

@app.get("/historial")
def obtener_historial():
    """4. Consultar Supabase"""
    try:
        db_response = supabase.table("historial_consultas").select("*").order("id", desc=True).limit(10).execute()
        return {"historial": db_response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar Supabase: {str(e)}")