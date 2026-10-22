# Resumen ejecutivo: predicción del cierre de Apple

El objetivo fue estimar el cierre de AAPL para el día bursátil siguiente y comprobar
si las redes recurrentes ofrecen una ventaja frente a dos referencias sencillas:
repetir el último cierre y usar el promedio de los 20 anteriores.

Se utilizaron datos diarios de Yahoo Finance desde 2020-01-02 hasta
2026-10-20 (1709 sesiones después de preparar los indicadores).
Los datos se separaron en orden cronológico: 70 % para entrenar, 15 % para validar
y 15 % para la prueba final. La normalización se ajustó solo con entrenamiento.
Se probaron RNN, LSTM y GRU, con entradas de una y seis variables. El modelo
recurrente se eligió por su RMSE de validación, sin consultar la prueba final.

La elección fue **RNN_6features_L60**, con RMSE de validación de
**5.673 USD**. En prueba obtuvo MAE de **27.013 USD**,
RMSE de **33.314 USD** y MAPE de **8.83 %**.
La referencia más precisa fue **Último cierre observado**
(RMSE de **4.440 USD**). Por tanto, la red seleccionada
**no superó** a la referencia sencilla. La diferencia entre validación y
prueba indica que su rendimiento no se mantuvo en el periodo posterior.

La LSTM evaluada en tres particiones temporales obtuvo un RMSE medio de
validación de **12.798 USD**. También se comprobaron la recuperación
de los pesos guardados y una estimación con las últimas 60 sesiones: **276.27 USD**.
Esa cifra es una salida del modelo, no un precio confirmado ni una recomendación
de inversión.

La comparación es válida para esta muestra, no para todos los periodos del
mercado. Cambios de régimen y volatilidad pueden alterar el error; además,
la franja alrededor de las predicciones describe residuos observados y no
constituye un intervalo de confianza calibrado. La semilla utilizada fue 42.
