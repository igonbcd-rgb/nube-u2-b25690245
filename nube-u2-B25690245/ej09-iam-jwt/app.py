import os, time, jwt # pip install pyjwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRETO = os.environ["JWT_SECRET"] # nunca en el código
app, bearer = FastAPI(), HTTPBearer()

def emitir(usuario: str, roles: list[str], minutos=30) -> str:
    return jwt.encode({"sub": usuario, "roles": roles,"exp": int(time.time()) + minutos * 60}, SECRETO, algorithm="HS256")

def requiere(rol: str):
    def verificar(cred: HTTPAuthorizationCredentials = Depends(bearer)):
        try:
            datos = jwt.decode(cred.credentials, SECRETO, algorithms=["HS256"])
        except jwt.PyJWTError:
            raise HTTPException(401, "Token inválido o expirado")
        if rol not in datos["roles"]:
            raise HTTPException(403, "Permiso insuficiente")
        return datos
    return verificar

@app.post("/api/ia/predict")
def predecir(entrada: dict, usuario=Depends(requiere("analista"))):
    return {"usuario": usuario["sub"], "demanda_estimada": 42.0}