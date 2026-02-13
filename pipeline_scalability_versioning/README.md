# 🔁 Actualización y Escalabilidad de Pipelines

Este proyecto demuestra estrategias modernas para **actualización y
escalabilidad de pipelines de datos**, incluyendo:

-   Escalado horizontal de workers.
-   Versionado de datos y esquemas.
-   Actualizaciones sin downtime (blue/green deployment).
-   Validación y pruebas automatizadas.

El objetivo es simular prácticas usadas en entornos reales de **Data
Engineering y plataformas analíticas productivas**.

------------------------------------------------------------------------

## 🎯 Objetivos de Aprendizaje

1.  Entender estrategias de escalado horizontal y vertical.
2.  Aprender actualización de pipelines sin downtime.
3.  Comprender gestión de versiones de datos.
4.  Conocer optimizaciones avanzadas de performance.

------------------------------------------------------------------------

## 📁 Estructura del Proyecto

``` bash
pipeline_scalability_versioning/
│
├─ docker-compose.scale.yml
├─ pytest.ini
├─ requirements-dev.txt
│
├─ src/
│  └─ data_version_manager.py
│
├─ tests/
│  └─ test_data_version_manager.py
│
├─ scripts/
│  └─ deploy-zero-downtime.sh
│
└─ k8s/
   ├─ blue-environment.yml
   ├─ green-environment.yml
   └─ airflow-service.yml
```

------------------------------------------------------------------------

## ⚙️ Escalado Horizontal de Workers

Se utiliza Docker Compose para ejecutar múltiples workers.

### Levantar servicios

``` bash
docker compose -f docker-compose.scale.yml up -d
```

### Escalar workers

``` bash
docker compose -f docker-compose.scale.yml up -d --scale airflow-worker=5
```

### Verificar estado

``` bash
docker compose ps
```

El escalado horizontal permite procesar múltiples tareas en paralelo.

------------------------------------------------------------------------

## 🗂️ Versionado de Datos

El módulo `DataVersionManager` permite:

-   Validar datos según versión de esquema.
-   Actualizar datos antiguos a nuevas versiones.
-   Mantener compatibilidad con versiones previas.
-   Generar scripts de migración.

### Ejecutar demo

``` bash
python src/data_version_manager.py
```

------------------------------------------------------------------------

## 🧪 Pruebas Automatizadas

### Instalar dependencias

``` bash
pip install -r requirements-dev.txt
```

### Ejecutar tests

``` bash
pytest -q
```

Esto valida que las migraciones y esquemas funcionen correctamente.

------------------------------------------------------------------------

## 🚀 Deployment sin Downtime (Blue/Green)

El script de despliegue implementa estrategia **blue-green**:

1.  Crear nueva versión del entorno.
2.  Validar funcionamiento.
3.  Cambiar tráfico hacia nueva versión.
4.  Eliminar versión anterior.

### Ejecutar deployment

``` bash
chmod +x scripts/deploy-zero-downtime.sh
./scripts/deploy-zero-downtime.sh v2
```

Esto permite actualizar pipelines sin interrumpir servicios activos.

------------------------------------------------------------------------

## ✅ Verificación Conceptual

### ¿Cuándo usar escalado vertical vs horizontal?

**Escalado vertical** (más CPU/RAM en un servidor):

-   Sistemas pequeños o monolíticos.
-   Infraestructura simple.
-   Bajo volumen de procesamiento.
-   Implementación inicial sencilla.

**Escalado horizontal** (más nodos/workers):

-   Alto volumen de datos.
-   Procesamiento distribuido.
-   Sistemas críticos con alta disponibilidad.
-   Arquitecturas modernas de microservicios y pipelines paralelos.

En pipelines productivos, el escalado horizontal suele preferirse por su
resiliencia y capacidad de crecimiento.

------------------------------------------------------------------------

### ¿Cómo asegurar compatibilidad backward al cambiar esquemas?

Buenas prácticas:

-   No eliminar campos antiguos inmediatamente.
-   Permitir valores nulos en nuevos campos.
-   Mantener soporte para versiones previas.
-   Implementar migraciones progresivas.
-   Versionar explícitamente esquemas y datos.
-   Ejecutar pruebas antes de migraciones productivas.

Esto permite actualizar pipelines sin romper sistemas consumidores de
datos.

------------------------------------------------------------------------

## 🧠 Conclusión

Este proyecto demuestra conceptos clave para pipelines productivos:

-   Escalabilidad
-   Versionado
-   Migración segura
-   Despliegue sin interrupciones
-   Validación automatizada

Simula prácticas utilizadas en plataformas modernas de datos en
producción.
