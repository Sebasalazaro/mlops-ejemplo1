# UNIVERSIDAD EAFIT
# 2025-2
# PROFESOR: EDWIN MONTOYA – emontoya@eafit.edu.co

MLOps – ejemplo 1.

Contexto: 1. Automatizar la subida de modelos a producción

## Problema: 

Se desea poner en producción un modelo predictivo mediante una API REST, que ingresando los datos:

    sepal_length
    sepal_width
    petal_length
    petal_width

### se predice el tipo de flor como una lista [12] o [45]

ej: send: 
    
    https://server/get-iris-type?sepal_length=1&sepal_width=1&petal_length=1&petal_width=1

    receive: [12]

1.Datos Fuente: datasets de entrenamiento: (train.py)

    from sklearn.datasets import load_iris
    # Load data
    iris = load_iris(as_frame = True)

2.Ingesta: no necesaria

3.Almacenamiento: no necesario

4.Procesamiento: data_prep & training [LOCAL]: Workstation científico de datos

* Modelos: model.pickle y transformer.pickle

6.Aplicación: API REST en nube GCP

 
## ETAPAS CICLO DE VIDA DATOS:

1.	DATOS DE ENTRENAMIENTO – LOCAL
2.	ENTRENAMIENTO – LOCAL
3.	MODELOS ENVIADOS A GITHUB (LOCAL -> GITHUB:main)

4.	PIPELINE 1 PARA DESPLEGAR EL MODELO (cloudbuild.yml)

a.	Paso 1: build del docker API REST con el modelo

    docker build

b.	Paso 2: Registro de la imagen del docker en el Docker Registry

    docker push

c.	Paso 3: Deploy de la imagen docker en un servicio en nube API REST

    docker run en Google Run

## TECNOLOGIAS:

LOCAL:
 
- Python 3.9
- Visual Studio Code
- Git

NUBE:

- Cuenta github
- Cuenta GCP (se envio por email instrucciones de activación)

    * Cloud Build
    * Cloud Run
    * Cloud Storage (buckets)
    * IAM & Admin (service account con permisos: Storage Object Viewer & Storage Object Admin)


 
PROCEDIMIENTO:

1.	Clonar repo de clase:

https://github.com/edwinm67/mlops-ejemplo1.git

2.	Crear su propio repo `mlops-ejemplo1.git` en tu cuenta github y seguir trabajando en esta para todos los cambios.
3.	Activar la cuenta GCP, crear un projecto base a llamar: `username-mlops`, reemplace username por el suyo propio.
4.	Realizar los ajustes respectivos en tu propio código, cada vez haga ‘git push’
5.	En Cloud Build, cree un Trigger configurando el link al repositorio asociado, y compruebe que desplega una app API REST en Cloud Run.
6.	Pruebe con postman
7.	Cambien alguna característica del modelo local.
8.	git push
9.	compruebe que `cloud build` se reejecutan cada vez que hay cambios en la rama main de tu repo del projecto mlops-ejemplo1
10.	ESTE LABORATORIO TIENE UNA INCONSISTENCIA O UN BUG QUE NO VA EN LA LINEA DE ESTE PRIMER MODELO DE MLOPS, CUAL ES? DESCRIBALO EN DETALLE Y PORQUE SE DA.
11.	documente todas las anteriores actividades
12.	entregue el lab
