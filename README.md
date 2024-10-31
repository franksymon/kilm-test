# kilm-test

Este proyecto expone, a través del lenguaje **Python versión 3.11**, framework **fastapi**, ORM **sqlmodel**, las apis necesarias para cumplimiento de test 

Para la arquitectura del proyecto, se implementa una estructura API REST con las siguientes capas:
* **Controller**: Carpeta que contiene los controladores o routers.
* **Services**: Carpeta que contiene la capa lógica de los controladores.
* **Model**: Carpeta que contiene la capa lógica de los Modelos en Base de datos.
* **Schema**: Carpeta que contiene la capa lógica de los Modelos para la serializacion de los datos de los servicios.

* **Config**: Carpeta que contiene archivos de definiciones de variables de entorno por parte del cliente.
* **Util**: Carpeta que contiene funciones comunes.
* **Tools**: Carpeta que contiene la librería proporcionada por el fabricante de la impresora fiscal Tfhka V-8.5 (**integration@thefactoryhka.com**).

### Entorno Virtual

Es recomendable utilizar un entorno virtual para ejecutar el proyecto. Para crear un entorno virtual en Windows, ejecute el siguiente comando en el directorio del proyecto clonado:

```sh
python -m venv .venv
```
Activacion del entorno virtual, terminal bash:

```sh
source .venv/script/activate
```

### Run project

Para ejecutar el proyecto se requiere inicialmente tener las librerías necesarias para la ejecución. Para realizar la instalación ejecutar el siguiente comando en el directorio del proyecto clonado: 

```sh
pip install -r requirements.txt
```

### Development
```sh
fastapi dev
```

### Produccion
```sh
fastapi run 
```

Se utiliza **Swagger** para la documentación de las API, para consultar la documentación de los servicios:
* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 


## Lógica de Negocios

### 1. Creación de Operaciones
- **Operador**: Un usuario con el rol de operador puede crear una nueva operación financiera especificando el monto requerido, el interés anual ofrecido y la fecha límite para recibir ofertas.
- **Estado Inicial**: La operación se crea con un estado inicial (por ejemplo, “Pendiente”) y se marca como abierta (`is_closed = False`).

### 2. Realización de Ofertas
- **Inversor**: Un usuario con el rol de inversor puede realizar ofertas sobre operaciones activas. Cada oferta incluye el monto que desea invertir y la tasa de interés a la que está dispuesto a invertir.
- **Registro de Ofertas**: Las ofertas se registran en la lista de `bids` de la operación correspondiente.

### 3. Cierre de Operaciones
- **Fecha Límite**: Una operación se cierra automáticamente cuando se alcanza la fecha límite o cuando se completa el monto requerido.
- **Actualización de Estado**: Al cerrarse, la operación se marca como cerrada (`is_closed = True`) y su estado se actualiza (por ejemplo, “Completada”).

### 4. Transacciones
- **Registro de Transacciones**: Las transacciones financieras relacionadas con la operación (como desembolsos o pagos) se registran en la lista de `transactions` de la operación.
- **Detalles de Transacciones**: Cada transacción incluye el monto, la fecha y una descripción opcional.

## Ejemplo de Flujo de Trabajo

1. **Creación de una Operación**:
   - Un operador crea una operación con un monto requerido de \$10,000, un interés anual del 5%, y una fecha límite del 31 de diciembre de 2024.

2. **Realización de Ofertas**:
   - Un inversor realiza una oferta de \$5,000 a una tasa de interés del 4.5%.
   - Otro inversor realiza una oferta de \$5,000 a una tasa de interés del 4.8%.

3. **Cierre de la Operación**:
   - La operación se cierra automáticamente al alcanzar el monto requerido de \$10,000 antes de la fecha límite.
   - El estado de la operación se actualiza a “Completada”.

4. **Registro de Transacciones**:
   - Se registran transacciones para reflejar los desembolsos a los inversores y cualquier otro movimiento financiero relacionado con la operación.

## Conclusión

Estos modelos y la lógica de negocios proporcionan una estructura robusta para gestionar un sistema de subastas de operaciones financieras, permitiendo la creación, oferta y cierre de operaciones, así como el registro de transacciones financieras asociadas.