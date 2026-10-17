# Local input data

Place `train.csv` and `test.csv` in `data/raw/` locally, or set `STRATAWEAVE_TRAIN_CSV` and `STRATAWEAVE_TEST_CSV`. Never commit raw data or prepared model artifacts. Grouped splits and earlier model results are loaded from `STRATAWEAVE_ARTIFACT_ROOT` and must be regenerated from the upstream pipeline or supplied locally.
