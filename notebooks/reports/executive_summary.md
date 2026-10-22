# Resumen ejecutivo — predicción del cierre de AAPL

**Pregunta de investigación.** ¿Las redes neuronales recurrentes predicen el cierre bursátil del siguiente día con mayor precisión que dos métodos sencillos basados en precios históricos?

**Datos y procedimiento.** Se utilizaron cotizaciones diarias de Yahoo Finance del 2020-01-02 al 2026-10-20 (1709 sesiones después del procesamiento). Se separaron cronológicamente los datos en entrenamiento (70 %), validación (15 %) y prueba (15 %). La predicción abarca una sesión futura y utiliza, por regla general, una ventana previa de 60 sesiones. La estandarización se ajustó únicamente con datos de entrenamiento. Se evaluaron RNN, LSTM y GRU con entradas univariadas y multivariadas. La parada anticipada depende de la pérdida de validación y la selección final, del RMSE de validación.

**Modelo recurrente seleccionado.** RNN_6features_L60, con RMSE de validación de **5.673 USD**. En la prueba reservada obtuvo MAE de **27.013 USD**, RMSE de **33.314 USD** y MAPE de **8.83 %**.

**Comparación con referencias.** El método de referencia con menor RMSE de prueba fue «Último cierre observado», con **4.440 USD**. El modelo recurrente seleccionado **no superó** este método en la prueba final. En estos datos, utilizar una arquitectura más compleja no significó predecir mejor.

**Recarga de pesos.** Se recuperaron los parámetros guardados de RNN_6features_L60 y se emplearon las últimas 60 sesiones para estimar el cierre siguiente: **276.27 USD**. La fecha concreta de pronóstico depende del último registro disponible. No es una recomendación para operar en bolsa.

**Estabilidad temporal.** En la validación con ventanas expansivas se reentrenó una LSTM en 3 particiones, con RMSE promedio de validación de **12.798 USD**. Esas particiones no incluyen el conjunto final de prueba.

**Alcances y límites.** Se comprobó la formación de ventanas, el entrenamiento, la recuperación de modelos y la comparación cuantitativa. Los cambios de régimen bursátil, la volatilidad y la dependencia temporal de los residuos pueden reducir la precisión fuera de la muestra. La franja de dispersión de errores que aparece en las gráficas es descriptiva, no un intervalo probabilístico calibrado. Solo se exploraron algunas configuraciones de ventana.

**Reproducción.** Se fijó la semilla aleatoria en 42. El repositorio guarda los datos históricos en CSV, métricas, predicciones, pesos y un cuaderno ejecutado. Los resultados corresponden a esa muestra y al entorno registrado. Uso exclusivamente académico.
