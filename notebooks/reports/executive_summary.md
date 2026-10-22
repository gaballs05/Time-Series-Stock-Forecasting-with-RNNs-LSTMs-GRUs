# Executive summary — AAPL next-day forecasting

**Research question.** Can a recurrent neural network predict the next day's Apple closing price more accurately than simple historical baselines?

**Data and method.** Yahoo Finance daily OHLCV data covering 2020-01-02 to 2026-10-20 (1709 processed trading days). A strictly chronological 70%/15%/15% train/validation/test split, 60-day lookback, 1-day horizon, and training-only scaling were used. Three recurrent architectures (RNN, LSTM, GRU) were evaluated using univariate and multivariate feature sets. Checkpoints and early stopping are based on validation loss; final architecture selection is based on validation RMSE.

**Selected model.** RNN_6features_L60, validation RMSE **5.673 USD**. Its untouched final test scores were MAE **27.013 USD**, RMSE **33.314 USD**, and MAPE **8.83%**.

**Baselines.** The strongest naïve/moving-average baseline on test was Last value with RMSE **4.440 USD**. The selected recurrent model **did not outperform** this baseline on the test segment. A recurrent model should not be presumed superior to a last-value predictor.

**60-day reload demonstration.** RNN_6features_L60 successfully reloaded using only the last 60 observed trading days to estimate the following closing price (**276.27 USD**); the exact forecasting date depends on the latest available trading session. This is not a trade recommendation.

**Temporal robustness.** Expanding-window walk-forward LSTM refits yielded mean validation RMSE **12.798 USD** across 3 folds. These are validation folds only and are not estimates from the final test interval.

**What worked and limitations.** Sliding windows, recurrent training, checkpoint reload, and comparisons are implemented. Financial prices are nonstationary: regime shifts, volatility and persistent residual structure may erode generalization. Residual spread is descriptive, not a calibrated prediction interval. Hyperparameter search is limited. Past prices and indicators do not establish causal forecastability.

**Reproducibility.** Seed 42; the workflow caches the original OHLCV CSV, exports metrics and prediction CSVs, archives PyTorch weights, and preserves the executed notebook. Results apply to the downloaded data snapshot and package versions captured by the runner. Not financial advice.
