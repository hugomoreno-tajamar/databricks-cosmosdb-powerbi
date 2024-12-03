
# **Análisis y Justificación de la Arquitectura**

Vamos a analizar la arquitectura planteada en este proyecto para capturar datos en tiempo real sobre la temperatura de una ciudad, almacenarlos en Azure Cosmos DB y visualizarlos en Power BI. 

## **1. Ventajas y desventajas de usar esta arquitectura**

### **Ventajas:**
- **Escalabilidad:**  
  - Azure Cosmos DB y Azure Databricks son servicios altamente escalables, permitiendo el manejo de grandes volúmenes de datos sin pérdida de rendimiento.

- **Facilidad de integración:**  
  - La integración nativa entre Azure Databricks, Cosmos DB y Power BI reduce la complejidad.

- **Seguridad:**  
  - La Virtual Network (VNet) proporciona un nivel adicional de seguridad, aislando los recursos de accesos no deseados.

- **Análisis avanzado:**  
  - Azure Databricks permite transformaciones y análisis avanzados en Python.

- **Simplicidad:**  
  - La arquitectura utiliza servicios gestionados, reduciendo la carga de administración.

#### **Desventajas:**
- **Costo elevado:**  
  - Los servicios utilizados (Databricks, Cosmos DB y Power BI) pueden ser costosos, especialmente con un alto volumen de datos.

- **No es ideal para tiempo real:**  
  - Tal y como se está usando el flujo de trabajo, no estamos permitiendo ver los datos en streaming desde PowerBi, lo que puede ser una limitación.

- **Complejidad inicial:**  
  - Configurar VNets y Service Endpoints requiere experiencia en Azure.

- **Carencia de streaming:**  
  - En la solución propuesta, se necesita descargar los datos una vez consumidos por Databricks y luego visualizarlos en PowerBi, lo que implica una falta de datos en tiempo real (o streaming)

---
## **2. ¿Por qué se usa un Service Endpoint entre Azure Cosmos DB y Databricks?**

### **Razones para usar un Service Endpoint:**
- **Seguridad:**  
  - Permite que los recursos se comuniquen a través de la red interna de Azure, evitando la exposición pública.
  
- **Rendimiento:**  
  - Minimiza la latencia, mejorando la eficiencia de las operaciones.

### **Otra opción posible:**
1. **Private Endpoint:**  
   - Conexión directa más segura y aislada que evita completamente el tráfico en redes públicas, lo cual permite una mayor seguridad entre nuestras aplicaciones.

---

## **3. ¿Por qué se usa una Virtual Network?**

### **Razones para usar una Virtual Network:**
- **Aislamiento:**  
  - La VNet asegura que los recursos dentro de ella no sean accesibles desde internet de manera predeterminada.

- **Control de tráfico:**  
  - Permite aplicar políticas de acceso específicas para cada servicio.

- **Seguridad:**  
  - Las VNets permiten el uso de Network Security Groups (NSGs) para controlar accesos a nivel de subred.

### **Otra opción posible:**
1. **Sin VNet:**  
   - Usar conexiones públicas seguras con autenticación y encriptación para simplificar la arquitectura. En este caso, considero que el uso de una VNet es  más recomendable para persistir la comunicación segura entre servicios
---

## **4. Arquitectura alternativa para consumir datos en streaming**

La arquitectura inicialmente propuesta está bien para ver un ejemplo de conectividad entre Azure Cosmos DB, Databricks y PowerBi, pero si realmente queremos consumir datos en streaming, podríamos proponer la siguiente arquitectura:

1. **Captura de los datos en streaming:**
   - Para capturar los datos, podríamos usar la herramienta de  **Azure Event Hubs**, que permite consumir datos en tiempo real. En nuestro caso, al consumirse desde una **API externa**,  podríamos añadir una función de **Function App** en Python para ingestar estos datos desde la API.

2. **Procesamiento de datos:**  
   - Para poder procesar los datos, podríamos  usar herramientas como **Azure Stream Analytics** o **Azure Databricks** que consuman los datos directamente desde **Azure Event Hubs** y procese estos datos para ser enviados posteriormente.

3. **Almacenamiento de datos:**  
   - Para el almacenamiento, podríamos enviar los datos directamente desde nuestra **herramienta de procesamiento** elegida anteriormente hacia **Azure Cosmos DB** para poder almacenar un histórico.

4. **Visualización en tiempo real:**
   - Enviar los datos procesados simultáneamente a **Power BI Streaming Dataset** para visualización en tiempo real.

---

En resumen, se poría llegar a utilizar una arquitectura mucho más completa para gestionar la visualización de datos en tiempo real, teniendo siempre en cuenta la seguridad de las conexiones entre servicios. No obstante, la arquitectura inicialmente propuesta, tendría más sentido para una solución de ingesta, transformación y visualización de datos externos.
