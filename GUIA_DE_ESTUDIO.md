# Guía de lectura y defensa del laboratorio

El notebook es la entrega; esta guía señala qué parte conviene leer cuando aparece una duda. Para entenderlo no basta con recordar el nombre de una función: hay que poder decir qué recibe, qué calcula y cómo se comprueba su resultado.

## Ruta rápida para presentar el trabajo

**Primero:** explicar qué se pretende predecir. **Después:** mostrar los datos y cómo se evita utilizar información futura. **Luego:** comparar las arquitecturas y los métodos sencillos. **Finalmente:** presentar los errores y concluir qué método funcionó mejor.

| Si preguntan… | Dónde buscar | Qué debe explicarse |
| --- | --- | --- |
| ¿Cuál era el objetivo? | Inicio del [notebook ejecutado](./stock_forecasting_executed.ipynb), sección introductoria | Predecir el cierre siguiente de AAPL y contrastarlo con dos referencias sencillas. |
| ¿De dónde vienen los datos? | **1. Obtención y conservación de los datos** | Descarga de Yahoo Finance, campos OHLCV y almacenamiento en CSV. |
| ¿Qué datos entran al modelo? | **2. Preparación de variables** y **3. Ventanas de observación** | Historial anterior al día buscado; seis variables en el caso multivariado. |
| ¿Qué significa evitar fuga de información? | **2. Preparación de variables** | División cronológica y normalización ajustada solo con entrenamiento. |
| ¿En qué se diferencian RNN, LSTM y GRU? | **4. Arquitecturas recurrentes** | Las tres procesan secuencias; LSTM y GRU incorporan mecanismos de compuertas para manejar la información temporal. |
| ¿Cómo se entrenaron? | **4. Arquitecturas recurrentes** y curvas de **7. Resultados** | Optimizador Adam, validación, parada anticipada y pesos guardados. |
| ¿Por qué hay ocho configuraciones? | **5. Experimentos** y **6. Longitud de la ventana** | Seis combinaciones entre arquitectura y número de variables, más dos LSTM de 30 y 90 sesiones. |
| ¿Por qué el modelo ganador se elige con validación? | **5. Experimentos** y **12. Resumen ejecutivo** | Para no usar la prueba final como criterio de selección. |
| ¿Qué representan MAE, RMSE y MAPE? | **3. Ventanas de observación** y tablas de resultados | Errores absoluto medio, cuadrático medio y porcentual absoluto medio. Valores menores son mejores. |
| ¿Qué significa el gráfico de residuos? | **7. Curvas, predicciones y residuos** | La diferencia entre precio real y estimado y posibles patrones que el modelo no captó. |
| ¿Qué se hizo con walk-forward? | **8. Esquema de validación** y **10. Validación temporal** | Tres reentrenamientos con más historial y validación posterior, sin incluir la prueba final. |
| ¿Se puede reutilizar el modelo? | **9. Recuperación de pesos** | Se recargan los pesos y se estiman nuevos valores a partir de las últimas 60 sesiones. |
| ¿Cuál fue la conclusión? | **12. Resumen ejecutivo** y [resumen externo](./notebooks/reports/executive_summary.md) | La RNN seleccionada por validación tuvo peor RMSE de prueba que el método de repetir el último cierre. |

## Qué decisiones vale la pena explicar

**Por qué Apple:** tiene un historial público diario suficiente para el ejercicio y permite obtener los campos OHLCV desde Yahoo Finance. No se eligió por una promesa de rentabilidad.

**Por qué conservar el CSV:** si la fuente cambia, ejecutar el código mañana podría producir otras cifras. El archivo guardado fija la muestra usada en las gráficas y las métricas.

**Por qué comparar con el último cierre:** un pronóstico más complejo solo resulta útil en esta prueba si mejora una referencia muy fácil de calcular.

**Qué error se corrigió:** una ejecución falló al recargar el modelo por incompatibilidad entre `float64` y `float32`. Revise la función de recarga y la conversión de tipos antes de probarla por su cuenta.

## Tres distinciones importantes

**Entrenamiento, validación y prueba no son lo mismo.** El entrenamiento modifica los pesos. La validación orienta la elección de arquitectura y el momento de detener el aprendizaje. La prueba se utiliza después para medir el resultado sobre fechas que no intervinieron en esa elección.

**Un buen resultado de validación no garantiza uno bueno en prueba.** En este experimento la RNN elegida tuvo un RMSE de validación de aproximadamente **5.67 USD**, pero en prueba llegó a **33.31 USD**. El precio de cierre anterior, sin red neuronal, obtuvo aproximadamente **4.44 USD** en esa misma prueba.

**La predicción siguiente no es una garantía.** El modelo puede producir una cifra a partir de las últimas 60 sesiones y aun así cometer errores grandes en etapas históricas distintas.

## Para reconstruirlo manualmente desde cero

Cuando se retome el trabajo como ejercicio de aprendizaje, conviene crear un notebook vacío y avanzar en este orden, **escribiendo y ejecutando cada parte**, no copiando todo el proyecto terminado:

1. Descargar los cierres de AAPL y comprobar fechas, faltantes y tipos de datos.
2. Dibujar la serie y separar las fechas de entrenamiento, validación y prueba.
3. Construir una ventana de 60 días y comprobar a mano cuál es su objetivo.
4. Calcular el pronóstico del último cierre y el de la media móvil para tener referencias.
5. Programar una LSTM pequeña y aprender qué recibe y devuelve cada tensor.
6. Entrenarla y graficar su pérdida; después comparar con RNN y GRU.
7. Añadir indicadores sin utilizar valores futuros; repetir el entrenamiento.
8. Medir MAE, RMSE y MAPE, revisar los residuos y explicar por qué una referencia sencilla puede resultar mejor.

**Criterio para estudiar:** en cada bloque se debe poder responder «¿qué entra?», «¿qué sale?» y «¿por qué se hace así?». Cuando alguna respuesta no sea clara, ese es el siguiente concepto que conviene practicar.

**Nota:** el repositorio actual es la entrega reproducible. Esta guía propone el orden de estudio, pero el aprendizaje manual será una actividad separada y no requiere modificar la entrega.
