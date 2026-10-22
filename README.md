# Lab 2 — Time-Series Stock Forecasting with RNNs, LSTMs and GRUs

[![GitHub Actions](https://github.com/gaballs05/Time-Series-Stock-Forecasting-with-RNNs-LSTMs-GRUs/actions/workflows/validate.yml/badge.svg)](https://github.com/gaballs05/Time-Series-Stock-Forecasting-with-RNNs-LSTMs-GRUs/actions/workflows/validate.yml)

**Status: end-to-end execution passed.** [Verified workflow run #15](https://github.com/gaballs05/Time-Series-Stock-Forecasting-with-RNNs-LSTMs-GRUs/actions/runs/39701664697), executed on 2026-10-22. Notebook, data cache, model weights and reports were committed to this repository automatically.

## Start here (all within GitHub)

1. **[Open the fully executed notebook](./stock_forecasting_executed.ipynb)** — the actual submission artifact with cell outputs, charts, metrics and dynamically generated executive summary.
2. **[Read the executive summary](./notebooks/reports/executive_summary.md)** — concise methodology, selected model, actual comparisons, limitations and conclusions.
3. **[Inspect model metrics](./notebooks/reports/model_metrics.csv)** and **[baseline metrics](./notebooks/reports/baseline_metrics.csv)**.
4. **[See the passing GitHub Actions execution](https://github.com/gaballs05/Time-Series-Stock-Forecasting-with-RNNs-LSTMs-GRUs/actions/runs/39701664697)** (the run also includes a downloadable artifact, but downloading is not necessary to view the deliverables here).

The editable source notebook is [notebooks/stock_forecasting.ipynb](./notebooks/stock_forecasting.ipynb). You do not need Google Colab or a desktop computer to view the outputs; GitHub renders notebooks directly.

## Research question

Do recurrent neural networks (vanilla RNN, LSTM, GRU) beat naïve historical-price forecasts for **next-trading-day AAPL closing prices**?

- **Data:** Yahoo Finance AAPL daily OHLCV, raw cache from **2019-10-22 through 2026-10-20**, with 1,709 usable rows after feature engineering (from 2020-01-02).
- **Prediction target:** next trading day's adjusted closing price, using the preceding observations only.
- **Chronological holdout:** approximately 70% training, 15% validation, 15% test. Scalers are fitted on training observations exclusively.
- **Feature sets:** univariate Close and multivariate Close, Volume, MA20, MA50, rolling volatility, and intraday range.
- **Architectures:** RNN, LSTM, GRU; 60-day windows for six primary comparisons, with a 30-day/90-day univariate-LSTM sensitivity analysis.
- **Training:** PyTorch, early stopping, best-checkpoint saves, ReduceLROnPlateau, fixed seed 42 and training/validation curves.
- **Validation:** expanding-window, 3-fold LSTM walk-forward refitting, with aggregate errors and a schematic.
- **Evaluation:** MAE, RMSE, guarded MAPE, last-value and 20-day moving-average baselines, prediction plots and residual diagnostics.

## Verified outcome

The recurrent model chosen **by validation RMSE** was **RNN_6features_L60**: validation RMSE **5.673 USD**; held-out test MAE **27.013 USD**, RMSE **33.314 USD**, MAPE **8.83%**.

The **last-value baseline** was substantially better on that test segment: RMSE **4.440 USD** and MAE **3.139 USD**. **The experiment does not establish that recurrent models outperform simple baselines.** Selection used the validation segment, *not* test scores. See the full metrics CSV for all eight experiments and the executive summary for limitations.

An independent saved-weight reload demonstrated a next-step estimate from the final **60 historical observations**; see the notebook for its output. These are educational forecasts, **not investment advice**.

## Repository map

| File or directory | Purpose |
| --- | --- |
| [stock_forecasting_executed.ipynb](./stock_forecasting_executed.ipynb) | Final notebook, executed and containing charts/outputs |
| [notebooks/stock_forecasting.ipynb](./notebooks/stock_forecasting.ipynb) | Editable reproducible notebook |
| [notebooks/data/AAPL_ohlcv.csv](./notebooks/data/AAPL_ohlcv.csv) | Cached daily raw OHLCV data |
| [notebooks/checkpoints/](./notebooks/checkpoints/) | Eight trained best-checkpoint weight files |
| [notebooks/reports/executive_summary.md](./notebooks/reports/executive_summary.md) | Evidence-based one-page executive summary |
| [notebooks/reports/model_metrics.csv](./notebooks/reports/model_metrics.csv) | Validation and held-out test metrics by architecture |
| [notebooks/reports/baseline_metrics.csv](./notebooks/reports/baseline_metrics.csv) | Test metrics for simple baselines |
| [notebooks/reports/test_predictions.csv](./notebooks/reports/test_predictions.csv) | Dates, observations, predictions and residuals |
| [notebooks/reports/environment.txt](./notebooks/reports/environment.txt) | Actual Python, PyTorch, CUDA, NumPy and pandas versions |
| [requirements.txt](./requirements.txt) | Dependency specification |
| [.github/workflows/validate.yml](./.github/workflows/validate.yml) | Runs notebook, validates outputs, archives and commits artifacts |

## Reproducing in GitHub (without local setup)

Open **Actions → Stock forecasting — execute and publish results → Run workflow**. The job installs CPU-only PyTorch and dependencies, validates the source notebook, executes every cell, checks that all required outputs exist, and commits a new executed notebook, CSV results, cached prices and weights if successful. Data is cached after the first successful run, so repeated runs use the committed snapshot unless you intentionally replace the CSV.

GitHub Actions has execution/runtime quotas. Changing the dataset or package versions may change results; consult the recorded [environment](./notebooks/reports/environment.txt).

## Source and field dictionary

- **Source:** Yahoo Finance, [Apple Inc. (AAPL) historical prices](https://finance.yahoo.com/quote/AAPL/history/), retrieved using the Python [yfinance](https://pypi.org/project/yfinance/) package (`auto_adjust=True`).
- **Date:** trading-session date; **Open**, **High**, **Low**, **Close:** adjusted USD prices; **Volume:** shares traded.
- **MA20/MA50:** 20- and 50-day trailing averages; **VOL20:** 20-day rolling standard deviation of daily returns; **Range:** daily (High-Low)/Close.
- Predictions are conditioned only on preceding observations. Scalers and recurrent model weights are learned on chronological training data.

## Notes on interpretation

Closing-price levels are nonstationary, residual intervals plotted in the notebook are descriptive rather than calibrated, and walk-forward folds assess validation robustness but do not replace the untouched test set. The lab is educational and should not be used to place trades.
