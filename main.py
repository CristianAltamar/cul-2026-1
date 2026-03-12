from fastapi import FastAPI
from routes.docente_routes import router as docente_router
from routes.semestre_routes import router as semestre_router
from routes.asignacion_docente_routes import router as asignacion_docente_router
from routes.asignatura_routes import router as asignatura_router
from routes.disponibilidad_docente_routes import router as disponibilidad_docente_router
from routes.grupo_routes import router as grupo_router
from routes.horario_routes import router as horario_router
from routes.jornada_routes import router as jornada_router
from routes.salon_routes import router as salon_router
from routes.programa_routes import router as programa_router
from routes.docente_asignatura_routes import router as docente_asignatura_router
from routes.facultad_routes import router as facultad_router
from routes.auth_routes import router as auth_router
from routes.usuario_routes import router as usuario_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    #"http://localhost.tiangolo.com",
    #"https://ep-square-flower-aiq3n3y4-pooler.c-4.us-east-1.aws.neon.tech",
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docente_router)
app.include_router(semestre_router)
app.include_router(asignacion_docente_router)
app.include_router(asignatura_router)
app.include_router(disponibilidad_docente_router)
app.include_router(grupo_router)
app.include_router(horario_router)
app.include_router(jornada_router)
app.include_router(salon_router)
app.include_router(programa_router)
app.include_router(docente_asignatura_router)
app.include_router(facultad_router)
app.include_router(auth_router)
app.include_router(usuario_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)