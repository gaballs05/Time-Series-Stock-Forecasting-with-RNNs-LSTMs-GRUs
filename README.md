# Laboratorio 2 — Predicción de precios bursátiles con redes recurrentes

[![Estado de GitHub Actions](https://github.com/gaballs05/Time-Series-Stock-Forecasting-with-RNNs-LSTMs-GRUs/actions/workflows/validate.yml/badge.svg)](https://github.com/gaballs05/Time-Series-Stock-Forecasting-with-RNNs-LSTMs-GRUs/actions/workflows/validate.yml)

**Materia:** laboratorio de series de tiempo.  
**Caso de estudio:** Apple Inc. (AAPL).  
**Herramientas:** Python, PyTorch, pandas, scikit-learn y Matplotlib.

## Qué se investigó

La pregunta principal es sencilla: **¿es posible predecir el precio de cierre de Apple para el día bursátil siguiente con mayor precisión que si se toma el último precio observado?**

Se compararon tres tipos de redes neuronales recurrentes: RNN, LSTM y GRU. Cada una se evaluó con una sola variable (cierre) y con seis variables (cierre, volumen, medias móviles de 20 y 50 sesiones, volatilidad y rango intradía). También se probaron ventanas de observación de 30, 60 y 90 sesiones para una LSTM.

El trabajo no pretende construir una herramienta de inversión. Se trata de comprobar qué funciona en una muestra histórica y reconocer, con los errores medidos, qué tan limitada puede ser una predicción bursátil.

## Por dónde comenzar

El archivo principal de entrega es el **[notebook ejecutado](./stock_forecasting_executed.ipynb)**. Contiene el código, las explicaciones, las tablas y las gráficas resultantes de la ejecución. GitHub permite verlo desde el navegador, sin instalar programas.

Si se necesita un recorrido más corto, conviene abrir primero el **[resumen ejecutivo](./notebooks/reports/executive_summary.md)** y después consultar las figuras y tablas del notebook.

El [notebook fuente](./notebooks/stock_forecasting.ipynb) es la versión que GitHub Actions ejecuta. La diferencia es importante: el archivo fuente contiene los pasos reproducibles; el ejecutado también conserva sus resultados. Para estudiar cada bloque con calma, está la [guía de lectura y defensa](./GUIA_DE_ESTUDIO.md).

## Datos utilizados

Las cotizaciones se obtuvieron de **Yahoo Finance**, mediante `yfinance`, y se conservaron en [`notebooks/data/AAPL_ohlcv.csv`](./notebooks/data/AAPL_ohlcv.csv). La muestra descargada abarca del **22 de octubre de 2019 al 20 de octubre de 2026**. Después de calcular los indicadores y eliminar los registros iniciales sin historial suficiente, quedaron **1,709 sesiones**, desde el 2 de enero de 2020.

| Campo | Significado |
| --- | --- |
| Date | Fecha de la sesión bursátil. |
| Open | Precio de apertura ajustado. |
| High | Precio máximo ajustado. |
| Low | Precio mínimo ajustado. |
| Close | Precio de cierre ajustado; es la variable que se busca anticipar. |
| Volume | Número de acciones negociadas. |
| MA20 y MA50 | Promedios móviles de los 20 y 50 cierres anteriores, respectivamente. |
| VOL20 | Desviación estándar móvil de los rendimientos diarios en 20 sesiones. |
| Range | Diferencia entre máximo y mínimo, dividida entre el cierre. |

Fuente: [historial de Apple en Yahoo Finance](https://finance.yahoo.com/quote/AAPL/history/). Se descargaron precios ajustados (`auto_adjust=True`). Estos datos pueden variar si Yahoo Finance revisa su histórico.

## Cómo se evitó usar información del futuro

Las observaciones se ordenaron por fecha. Se reservó aproximadamente el **70 % para entrenamiento**, el **15 % para validación** y el **15 % final para prueba**, sin mezclarlas aleatoriamente.

Cada predicción utiliza una ventana de sesiones anteriores. Los parámetros de normalización se calcularon exclusivamente con el tramo de entrenamiento. La elección de la arquitectura se hizo usando el **RMSE de validación**, no el de prueba. La evaluación de prueba se mantuvo para comprobar el comportamiento fuera de la muestra utilizada para elegir el modelo.

Se entrenó con el optimizador Adam, parada anticipada cuando dejaba de mejorar la pérdida de validación y un programador para reducir la tasa de aprendizaje. Se guardaron los mejores pesos de cada configuración. También se realizó validación temporal *walk-forward* con tres reentrenamientos de una LSTM univariada sobre ventanas de entrenamiento expansivas.

## Resultados del experimento

El modelo recurrente elegido por validación fue **RNN multivariada con 60 sesiones de historial** (`RNN_6features_L60`).

| Evaluación | Resultado |
| --- | ---: |
| RMSE de validación del modelo seleccionado | **5.673 USD** |
| MAE de prueba del modelo seleccionado | 27.013 USD |
| RMSE de prueba del modelo seleccionado | **33.314 USD** |
| MAPE de prueba del modelo seleccionado | 8.83 % |
| RMSE de prueba al repetir el último cierre | **4.440 USD** |
| RMSE de prueba con media móvil de 20 sesiones | 11.759 USD |
| RMSE promedio de validación *walk-forward* (LSTM, 3 particiones) | 12.798 USD |

**La principal conclusión es que el modelo recurrente elegido no superó al método de repetir el último cierre.** El resultado no invalida el experimento: muestra por qué es necesario comparar redes neuronales con alternativas sencillas y separar validación de prueba. Las series de precios también pueden cambiar de comportamiento con el tiempo.

Las cifras anteriores corresponden a la [ejecución completa en español de GitHub Actions](https://github.com/gaballs05/Time-Series-Stock-Forecasting-with-RNNs-LSTMs-GRUs/actions/runs/39705897168). Al volver a ejecutar el laboratorio, las métricas pueden variar ligeramente según las versiones instaladas y el entorno, aunque la muestra de precios permanezca guardada.

## Archivos de entrega y evidencias

| Archivo | Para qué sirve |
| --- | --- |
| [`stock_forecasting_executed.ipynb`](./stock_forecasting_executed.ipynb) | **Entrega principal**: código ejecutado, tablas, gráficas y conclusiones. |
| [`notebooks/stock_forecasting.ipynb`](./notebooks/stock_forecasting.ipynb) | Código y explicación listos para una nueva ejecución. |
| [`notebooks/reports/executive_summary.md`](./notebooks/reports/executive_summary.md) | Resumen ejecutivo de los resultados. También se integra en el notebook. |
| [`notebooks/reports/model_metrics.csv`](./notebooks/reports/model_metrics.csv) | MAE, RMSE y MAPE de cada configuración. |
| [`notebooks/reports/baseline_metrics.csv`](./notebooks/reports/baseline_metrics.csv) | Métricas de los dos métodos de referencia. |
| [`notebooks/reports/test_predictions.csv`](./notebooks/reports/test_predictions.csv) | Fechas, cierres reales, estimaciones y residuos. |
| [`notebooks/checkpoints/`](./notebooks/checkpoints/) | Pesos entrenados de RNN, LSTM y GRU. |
| [`notebooks/data/AAPL_ohlcv.csv`](./notebooks/data/AAPL_ohlcv.csv) | Copia de las cotizaciones usadas en el experimento. |
| [`requirements.txt`](./requirements.txt) | Bibliotecas necesarias. |
| [`notebooks/reports/environment.txt`](./notebooks/reports/environment.txt) | Versiones de Python, PyTorch, CUDA y bibliotecas principales. |
| [`.github/workflows/validate.yml`](./.github/workflows/validate.yml) | Ejecución automática y conservación de resultados. |
| [`GUIA_DE_ESTUDIO.md`](./GUIA_DE_ESTUDIO.md) | Ruta para estudiar y explicar el trabajo manualmente. |

Los nombres de bibliotecas, columnas originales del proveedor y archivos se conservan en su formato técnico para no romper las dependencias ni impedir reproducir el experimento. **La explicación del trabajo y la interpretación de los resultados están en español.**

## Cómo repetir la ejecución desde GitHub

En la pestaña [**Actions**](https://github.com/gaballs05/Time-Series-Stock-Forecasting-with-RNNs-LSTMs-GRUs/actions), seleccione el flujo **«Pronóstico bursátil — ejecutar y publicar resultados»** y la opción **Run workflow / Ejecutar flujo de trabajo**. El sistema instala las dependencias, valida el notebook, ejecuta sus celdas y conserva sus archivos resultantes si todas las comprobaciones concluyen correctamente.

GitHub Actions tiene límites de tiempo y recursos. El archivo de datos se reutiliza para no cambiar accidentalmente la muestra al repetir el estudio. La semilla aleatoria utilizada es **42**.

## Limitaciones que deben mencionarse

- Los mercados cambian con el tiempo. Un error bajo en validación no garantiza buen desempeño en otra etapa histórica.
- El margen dibujado alrededor de las predicciones describe la dispersión observada de los residuos; **no es un intervalo de confianza calibrado**.
- Las pruebas con ventanas de 30, 60 y 90 días permiten una comparación acotada, no una optimización exhaustiva.
- Las predicciones se presentan exclusivamente para fines académicos y **no constituyen asesoría financiera**.
