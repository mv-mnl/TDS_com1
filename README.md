# Herramienta Universal de Teoría de Colas

Un script interactivo en Python diseñado para resolver problemas y calcular métricas de diversos modelos de la **Teoría de Colas**.

## Descripción

El programa permite seleccionar entre múltiples modelos de líneas de espera para calcular métricas como:
- Utilización del sistema (rho)
- Probabilidad de sistema vacío (P0)
- Número esperado de clientes en el sistema (L) y en la cola (Lq)
- Tiempo esperado en el sistema (W) y en la cola (Wq)

Además, cuenta con una opción de **Análisis de Costos** integrada para todos los modelos, la cual permite calcular el costo total del sistema ingresando el costo por servidor y el costo por tiempo de espera.

## Modelos Soportados

1. **Modelo M/M/1**: Un solo servidor, llegadas y servicios con distribución exponencial.
2. **Modelo M/M/s**: Múltiples servidores en paralelo.
3. **Modelo M/G/1**: Tiempos de servicio variables (fórmula de Pollaczek-Khinchine).
4. **Modelo M/M/1/K**: Sistema con capacidad finita o límite de clientes permitidos.
5. **Modelo con Prioridades**: Dos clases de clientes (Críticos y Normales), modelo no preemptivo.

## Requisitos

- **Python 3.x**: El script utiliza la biblioteca estándar `math`, por lo que no requiere módulos externos.

## Cómo Usar el Programa

1. Abre una terminal.
2. Navega al directorio donde se encuentra el archivo `ejer.py`.
3. Ejecuta el script con el siguiente comando:

   ```bash
   python ejer.py
   ```
   *(También puedes usar `python3 ejer.py` dependiendo de tu sistema)*

4. El programa mostrará un menú interactivo. Ingresa el número de la opción deseada (del 1 al 6):
   - Se te solicitará ingresar los datos correspondientes como **Tasa de Llegada ($\lambda$)**, **Tasa de Servicio ($\mu$)**, número de servidores ($s$), etc.
   - Utiliza **puntos** (.) para los números decimales.

5. Tras ver los resultados de las métricas principales, el programa te preguntará si deseas calcular los costos totales del sistema `(s/n)`.
   - Si eliges `s`, deberás ingresar el *Costo por Servidor ($C_e$)* y el *Costo de Espera ($C_q$)*.

6. Finalizada la ejecución de un modelo, el menú volverá a aparecer. Selecciona `6` para salir de la herramienta.

## Manejo de Errores
- Si el sistema ingresado es **inestable** (por ejemplo, si la tasa de llegada es mayor o igual a la capacidad de servicio, $\rho \ge 1$), el programa mostrará una advertencia y no calculará resultados irreales.
- Si ingresas un valor no numérico inválido, el programa te pedirá que introduzcas uno válido.
