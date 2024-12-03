

# Integración de Azure Cosmos DB con Spark, Databricks y Power BI

Este proyecto detalla los pasos para configurar y conectar **Azure Cosmos DB (API para MongoDB)** con **Spark y Databricks**, utilizando **Power BI** para visualización de datos. El objetivo es capturar datos meteorológicos en tiempo real y almacenarlos en Cosmos DB, facilitando su análisis mediante Databricks y Power BI.

---

## Requisitos Previos
1. **Cuenta de Azure** activa.
2. **Cuenta de OpenWeather** para obtener la API Key.
3. **Databricks** configurado en Azure.
4. **Power BI Desktop** instalado en tu equipo.

---

## 1. Configuración de Azure Cosmos DB
1. **Crear un grupo de recursos** en el portal de Azure.
2. **Crear un recurso Cosmos DB:**
   - Selecciona **Azure Cosmos DB for MongoDB**.
   - Configura el modo **Serverless**.
   - Deja las opciones predeterminadas en las pestañas **Global Distribution**, **Networking**, **Backup Policy** y **Encryption**.
   - Haz clic en **Review + Create** y luego en **Create**.
3. **Crear una base de datos y colección:**
   - Ve a **Data Explorer** en tu recurso de **Cosmos DB** que has creado antes.
   - Haz clic en **+New Database**, asigna un nombre y haz clic en **OK**.
   - En los tres puntos del nombre de la base de datos, selecciona **New Collection**.
   - Configura:
     - **Collection ID:** nombre de la colección.
     - **Unsharded Collection**.
     - Haz clic en **OK**.

---

## 2. Configuración del Script Meteorológico
1. Regístrate en [OpenWeather](https://openweathermap.org/api) y copia tu API Key desde la sección **API Keys**.
2. **Editar el script `script.py`:**
    - Crea un archivo .env en el mismo directorio que tu `script.py` y añade la siguiente información:
    ```bash
    OPENWEATHER_API_KEY = <tu_api_key>  
    COSMOS_DB_NAME = <DB_NAME>
    COSMOS_COLLECTION_NAME = <COLLECTION_NAME>
    COSMOS_CONNECTION_STRING = <CONNECTION>
    ```
   - Reemplaza `tu_api_key` con la API Key que has copiado anteriormente.
   - En `DB_NAME`, coloca el nombre de tu base de datos.
   - En `COLLECTION_NAME`, coloca el nombre de la colección.
   - Copia el **Primary Connection String** desde Azure Cosmos DB > Configuración > Cadenas de Conexión y pégalo en `CONNECTION`.

3. **Ejecuta el script:**
    - Crear el entorno virtual:  `python -m venv venv`
    - Activar el entorno vitual: ` .\venv\Scripts\activate`
    - Instalar las dependencias con `pip install requirements.txt`
   - Ejecutar el script con `py script.py`
   - Cuando lo consideres, detén la captura con `CTRL + C`.

---

## 3. Configuración de Azure Databricks
1. **Crear una red virtual (VNet):**
   - Ve a **Virtual Networks** en Azure.
   - Crea una nueva red, deja las opciones predeterminadas y haz clic en **Create**.
   - En **Address Space**, agrega una subred para los servicios de Databricks.
2. **Crear un recurso de Databricks:**
   - Selecciona el plan **Premium**.
   - Configura la red virtual y desactiva las opciones de cifrado y seguridad.
   - Haz clic en **Review + Create**.
3. **Configurar un Service Endpoint:**
   - Ve a tu red virtual y selecciona la subred pública.
   - Agrega el Service Endpoint para **Microsoft.AzureCosmosDB**.
4. **Configurar un clúster en Databricks:**
   - Crea un clúster de tipo **Single Node**.
   - Configura el siguiente código en **Spark Config**:
     ```plaintext
     spark.master local[*, 4]
     spark.databricks.cluster.profile singleNode
     spark.mongodb.output.uri=TU_CADENA_DE_CONEXION
     spark.mongodb.input.uri=TU_CADENA_DE_CONEXION
     ```
   - Instala la biblioteca **MongoDB Spark Connector** desde Maven:
   Entra en tu clúster creado y pincha en la sección **Bibliotecas** en la parte superior. Una vez dentro, dale a **Instalar Nueva** > **Maven** > **Buscar paquetas**. En el buscador de arriba a la izquierda seleccionamos **Paquetes Spark** y buscamos `mongo-spark` y seleccionamos la librería.

---

## 4. Usar Databricks para Consultar Cosmos DB
1. **Abrir un notebook en Databricks:**
- Configura la URI de conexión.
   ```python
    from pyspark.sql import SparkSession

    uri =  <TU_CADENA_DE_CONEXION>

    spark = SparkSession.builder.appName("TestingApp").config('spark.jars.  packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1').getOrCreate()
    ```
- Crea un DataFrame para consultar datos desde Cosmos DB:
    ```python
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource") \
    .option("uri", uri) \
    .option("database", <tu_database>) \
    .option("collection", <tu_collection>) \
    .load()
    ```
    Sustituyendo <tu_database> por el nombre de tu base de datos de Mongo y <tu_collection> por el nombre de la colección
- Consultar los datos:
    ```python
    df.show(truncate=False)
    ```
2. **Almacenar el DataFrame en un Hive Metastore:**
- Esto permite usar los datos en Power BI.
     ```python
    df.write.saveAsTable("PowerBITable")
    ```
---

## 5. Integración con Power BI
1. **Conectar Power BI con Databricks:**
   - Ve a **Partner Connect** en Databricks y selecciona Power BI.
   - Descarga el archivo de conexión `.pbids`.
   - Ábrelo en Power BI Desktop y autentícate con tu cuenta de Azure.
2. **Visualizar los datos:**
   - Selecciona la tabla cargada desde Databricks.
   - Genera gráficos y visualizaciones interactivas.
---

## 6. Eliminación de Recursos
Para evitar costos adicionales, elimina todos los recursos creados:
- Red virtual.
- Databricks.
- Cosmos DB.

---

## Referencias
- [OpenWeather API](https://openweathermap.org/api)
- [Azure Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db/)
- [Power BI Desktop](https://powerbi.microsoft.com/)

Este README proporciona los pasos necesarios para configurar y trabajar con los recursos mencionados. Si tienes dudas, revisa la documentación oficial de Azure y Databricks.


