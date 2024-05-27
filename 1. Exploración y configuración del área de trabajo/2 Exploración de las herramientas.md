# Exploración de las herramientas de desarrollo para la interacción de áreas de trabajo

> Actualmente, hay dos versiones del SDK de Python: versión 1 (v1) y versión 2 (v2). En el caso de los nuevos proyectos, debe usar v2 y, por lo tanto, el contenido de esta unidad solo cubre la versión 2.

## ¿Cuándo usar v2?

Debe usar v2 si va a iniciar un nuevo proyecto o flujo de trabajo de aprendizaje automático. Debe usar v2 si quiere usar las nuevas características que se ofrecen en v2. Las características incluyen:

- Inferencia administrada
- Componentes reutilizables en canalizaciones
- Programación mejorada de canalizaciones
- Panel de inteligencia artificial responsable
- Registro de recursos

Algunas de las carencias de la v2 incluyen:

- Compatibilidad con Spark en trabajos: actualmente se encuentra en versión preliminar en v2.
- Publicación de trabajos (canalizaciones en v1) como puntos de conexión. Sin embargo, puede programar canalizaciones sin publicarlos.
- Compatibilidad con almacenes de datos de SQL y bases de datos.
- Posibilidad de usar componentes precompilados clásicos en el diseñador con v2.

[Actualización a v2](https://learn.microsoft.com/es-es/azure/machine-learning/how-to-migrate-from-v1?view=azureml-api-2)
[Actualiación de la admon. del area de trabajo a la v2 del SDK](https://learn.microsoft.com/es-es/azure/machine-learning/migrate-to-v2-resource-workspace?view=azureml-api-2)

## Instalación del SDK para Python

Para instalar el SDK de Python en el entorno de Python, necesita Python 3.7 o superior.

```Python
pip install azure-ai-ml
```

## Conexión a un área de trabajo

Una vez instalado debera conectarse al area de trabajo. Al conectarse, va a autenticar el entorno para interactuar con el área de trabajo con el objetivo de crear y administrar recursos y activos.
Para autenticarse, necesita los valores en tres parámetros necesarios:

- `subscription_id`: el identificador de suscripción
- `resource_group`: el nombre del grupo de recursos
- `workspace_name`: el nombre del área de trabajo

A continuación, puede definir la autenticación mediante el código siguiente:

```Python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)
```

Después de definir la autenticación, debe llamar al método `MLClient` del entorno para conectarse al área de trabajo. Llamará a `MLClient` cada vez que quiera crear o actualizar un recurso o un recurso en el área de trabajo.

Por ejemplo, se conectará al área de trabajo al crear un nuevo trabajo para entrenar un modelo:

```Python
from azure.ai.ml import command

# configure job
job = command(
    code="./src",
    command="python train.py",
    environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest",
    compute="aml-cluster",
    experiment_name="train-model"
)

# connect to workspace and submit job
returned_job = ml_client.create_or_update(job)
```

## Documentación de referencia

- [La documentación de referencia de la claseMLClient](https://learn.microsoft.com/es-es/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python)
- [La documentación de referencia también incluye una lista de las clases de todas las entidades](https://learn.microsoft.com/es-es/python/api/azure-ai-ml/azure.ai.ml.entities?view=azure-python)
- [AMLCompute](https://learn.microsoft.com/es-es/python/api/azure-ai-ml/azure.ai.ml.entities.amlcompute?view=azure-python)

## Exploración de la CLI

Otro enfoque basado en código para interactuar con el área de trabajo de Azure Machine Learning es la interfaz de la línea de comandos (CLI). Como científico de datos, es posible que no trabaje con la CLI tanto como lo hace con Python. Los administradores e ingenieros suelen usar la CLI de Azure para automatizar tareas en Azure.

Hay muchas ventajas en el uso de la CLI de Azure con Azure Machine Learning. La CLI de Azure le permite:

- Automatizar la creación y configuración de activos y recursos para que sean repetibles
- Garantizar la coherencia de activos y recursos que se deben replicar en varios entornos (por ejemplo, desarrollo, prueba y producción)
- Incorporar la configuración de activos de aprendizaje automático en flujos de trabajo de operaciones de desarrollador (DevOps), como las canalizaciones de integración continua e implementación continua (CI/CD).

## Instalación de la CLI de Azure

Puede instalar la CLI de Azure en un equipo Linux, Mac o Windows. Con la CLI de Azure, podrá ejecutar comandos o scripts para administrar los recursos de Azure. También puede usar la CLI de Azure desde un explorador mediante Azure Cloud Shell.

## Instalación de la extensión de Azure Machine Learning

Después de instalar la CLI de Azure o configurar Azure Cloud Shell, debe instalar la extensión de Azure Machine Learning para administrar los recursos de Azure Machine Learning mediante la CLI de Azure.

Puede instalar la extensión Azure Machine Learning `ml` con el siguiente comando:

```Azure CLI
az extension add -n ml -y
```

Luego, puede ejecutar el comando de ayuda `-h` para comprobar que la extensión está instalada y obtener una lista de comandos disponibles con esta extensión. La lista proporciona información general sobre las tareas que puede ejecutar con la extensión CLI de Azure para Azure Machine Learning:

```Azure CLI
az ml -h
```

## Trabajo con la CLI de Azure

Si desea usar la CLI de Azure para interactuar con el área de trabajo de Azure Machine Learning, usará comandos. Cada comando tiene el prefijo az ml. Puede encontrar la [lista de comandos en la documentación de referencia de la CLI](https://learn.microsoft.com/es-es/cli/azure/ml?view=azure-cli-latest).

Por ejemplo, para crear un destino de proceso, puede usar este comando:

```Azure CLI
az ml compute create --name aml-cluster --size STANDARD_DS3_v2 --min-instances 0 --max-instances 5 --type AmlCompute --resource-group my-resource-group --workspace-name my-workspace
```

Para explorar todos los parámetros posibles que puede usar con un comando, puede revisar la [documentación de referencia del comando específico](https://learn.microsoft.com/es-es/cli/azure/ml/compute?view=azure-cli-latest).

A medida que defina los parámetros de un activo o recurso que desea crear, es posible que prefiera usar archivos **YAML** para definir la configuración en su lugar. Al almacenar todos los valores de parámetro en un archivo YAML, resulta más fácil organizar las tareas y automatizarlas.

Por ejemplo, también puede crear el mismo destino de proceso al definir primero la configuración en un archivo YAML:

```yml
$schema: https://azuremlschemas.azureedge.net/latest/amlCompute.schema.json
name: aml-cluster
type: amlcompute
size: STANDARD_DS3_v2
min_instances: 0
max_instances: 5
```

Todos los parámetros posibles que puede incluir en el archivo YAML se pueden encontrar en la [documentación de referencia del activo o recurso específico que desea crear como un clúster de proceso](https://learn.microsoft.com/es-es/azure/machine-learning/reference-yaml-compute-aml?view=azureml-api-2).

Al guardar el archivo YAML como compute.yml, puede crear el destino de proceso con este comando:

```Azure CLI
az ml compute create --file compute.yml --resource-group my-resource-group --workspace-name my-workspace
```

Puede encontrar [información general de todos los esquemas de YAML en la documentación de referencia](https://learn.microsoft.com/es-es/azure/machine-learning/reference-yaml-overview?view=azureml-api-2).

## Exercise

Remover las versiones de extensión 1 y 2 de `ML CLI`

```Azure Cloud Shell
 az extension remove -n azure-cli-ml
 az extension remove -n ml
```

[Ejemplo SDK Python](https://github.com/MicrosoftLearning/mslearn-azure-ml/blob/main/Labs/02/Run%20training%20script.ipynb)
