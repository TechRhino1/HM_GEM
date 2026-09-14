# BTCUSD# — 6-Month Backtest and Trade-Failure Analysis

**Instrument:** BTCUSD# (canonical `BTCUSD`), CRYPTO, broker `XMGlobal-MT5 5`
**Window:** 2026-03-14 07:00:00+00:00 → 2026-09-13 06:00:00+00:00  (183 days, 4392 H1 bars)
**Data:** MT5_TERMINAL_REAL — real MT5 history, structural validation passed
**Configuration:** uncalibrated baseline (legacy 29-gate stack)  
**Account:** $10,000, 0.5% risk per trade, median spread 2250.0 pips, slippage 0.5 pips

## 1. Headline result

| Metric | Value |
|---|---:|
| Trades | 89 |
| Wins / Losses | 27 / 62 |
| Win rate | 30.34% |
| Expectancy | -0.2031 R per trade |
| Total R | -18.07 R |
| Average win / loss | +1.627 R / -1.000 R |
| Payoff ratio | 1.627 |
| Profit factor | 0.750 |
| Net profit | $-402.45 |
| Max drawdown | 5.73% |
| Average bars held | 18.1 |

**Verdict.** Losing system: -0.2031 R per trade over 89 trades. The losses are analysed below.

### The calibrated edge test on this window

| Stage | Trades | Win rate | Expectancy (R) |
|---|---:|---:|---:|
| In-sample (training folds) | 146 | 66.4% | +0.0329 |
| Purged out-of-sample | 100 | 63.0% | -0.0159 |

**The calibrated system refuses to trade this symbol.** Its out-of-sample expectancy is non-positive (-0.0159 R over 100 trades) despite a positive in-sample figure (+0.0329 R) — i.e. the edge did not survive the walk-forward split. The entry policy declines the symbol rather than trading it at a smaller size, so the engine takes **zero** trades when the calibrated profile is active.

> win rate - best achievable in-sample with positive expectancy is 67.5% (tp0.6_beoff_pc0.5x0.5_troff@2_mb48_s0@thr0.747), below the 75% target

This is the single most important result on this page: the strategy *as configured by the legacy gates* does trade, and those trades are analysed below — but the calibrated configuration judges the symbol unprofitable and stands aside. The two are not in conflict; the second is what the evidence says about the first.

## 2. How trades ended

| Exit | Count | Share | Avg R | Total R | Win rate |
|---|---:|---:|---:|---:|---:|
| STOP | 80 | 89.9% | -0.501 | -40.07 | 22.5% |
| TARGET | 9 | 10.1% | +2.444 | +22.00 | 100.0% |

## 3. Why the losing trades lost

Of 62 losing trades, every one is attributed to a primary cause by explicit measurable rules (no discretion). A trade can trip several conditions; the table counts *primary* cause and lists all contributing flags separately.

| Primary cause | Trades | Share of losses | Total R lost | Avg R |
|---|---:|---:|---:|---:|
| GAVE_BACK_FAVOURABLE_MOVE | 35 | 56.5% | -35.00 | -1.000 |
| IMMEDIATE_ADVERSE_MOVE | 14 | 22.6% | -14.00 | -1.000 |
| STOPPED_AFTER_MINOR_PROGRESS | 10 | 16.1% | -10.00 | -1.000 |
| STOPPED_WITHOUT_PROGRESS | 3 | 4.8% | -3.00 | -1.000 |

- **GAVE_BACK_FAVOURABLE_MOVE** — Gave back a favourable move: the trade ran into profit, then reversed all the way to the stop. Exit management, not entry selection.
- **IMMEDIATE_ADVERSE_MOVE** — Entry timing: price moved straight against the position and never recovered. The entry was taken into immediate adverse flow.
- **STOPPED_AFTER_MINOR_PROGRESS** — Stopped out after a small favourable move that fell short of the target.
- **STOPPED_WITHOUT_PROGRESS** — Stopped out with essentially no favourable excursion — the entry had no immediate follow-through.

### Contributing conditions across all losses

| Condition | Losses where it fired | Share |
|---|---:|---:|
| GAVE_BACK_FAVOURABLE_MOVE | 35 | 56.5% |
| ENTRY_AT_RANGE_EXTREME | 26 | 41.9% |
| STOPPED_WITHOUT_PROGRESS | 17 | 27.4% |
| IMMEDIATE_ADVERSE_MOVE | 14 | 22.6% |
| HIGH_VOLATILITY_REGIME | 11 | 17.7% |
| VOLATILITY_EXPANDING_AT_ENTRY | 11 | 17.7% |
| STOPPED_AFTER_MINOR_PROGRESS | 10 | 16.1% |
| COUNTER_TREND_ENTRY | 5 | 8.1% |
| TARGET_NEARLY_REACHED | 2 | 3.2% |

## 4. Trade-by-trade failure ledger

Every losing trade with the evidence that produced its label. `MFE` is the best unrealised excursion (how far the trade ever went in favour) and `MAE` the worst, both in R. `stop/ATR` below 1.0 means the stop sat inside one bar's normal range.

| # | Entry time | Side | Entry | Stop | R | MFE (R) | MAE (R) | Bars | Exit | stop/ATR | range pos | counter-trend | Primary cause |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|:--:|---|
| 1 | 2026-03-20 07:00 | BUY | 70791.9 | 69724.9 | -1.00 | 0.53 | 1.14 | 10 | STOP | 2.01 | 0.84 | yes | GAVE_BACK_FAVOURABLE_MOVE |
| 2 | 2026-03-23 03:00 | SELL | 67658.7 | 68524.5 | -1.00 | 0.15 | 1.07 | 3 | STOP | 1.78 | 0.25 | no | IMMEDIATE_ADVERSE_MOVE |
| 3 | 2026-03-23 16:00 | BUY | 71500.1 | 70005.9 | -1.00 | 0.20 | 1.02 | 24 | STOP | 1.96 | 0.92 | no | STOPPED_WITHOUT_PROGRESS |
| 4 | 2026-03-25 14:00 | BUY | 71695.5 | 70945.1 | -1.00 | 0.34 | 1.52 | 4 | STOP | 1.47 | 0.90 | no | STOPPED_AFTER_MINOR_PROGRESS |
| 5 | 2026-03-28 22:00 | BUY | 66924.5 | 66411.5 | -1.00 | 0.15 | 1.27 | 4 | STOP | 1.66 | 0.72 | no | IMMEDIATE_ADVERSE_MOVE |
| 6 | 2026-03-30 04:00 | SELL | 66265.4 | 67052.0 | -1.00 | 0.00 | 1.50 | 2 | STOP | 1.68 | 0.78 | yes | IMMEDIATE_ADVERSE_MOVE |
| 7 | 2026-04-01 11:00 | BUY | 68696.2 | 67736.5 | -1.00 | 0.49 | 1.74 | 18 | STOP | 1.68 | 0.80 | no | STOPPED_AFTER_MINOR_PROGRESS |
| 8 | 2026-04-10 06:00 | BUY | 71976.0 | 70763.0 | -1.00 | 1.50 | 1.06 | 60 | STOP | 2.25 | 0.51 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 9 | 2026-04-17 17:00 | BUY | 77352.5 | 76548.6 | -1.00 | 1.22 | 1.08 | 19 | STOP | 1.32 | 0.96 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 10 | 2026-04-20 23:00 | BUY | 76294.1 | 75211.6 | -1.00 | 0.55 | 1.16 | 22 | STOP | 2.07 | 0.90 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 11 | 2026-04-22 13:00 | BUY | 78013.6 | 77009.1 | -1.00 | 1.44 | 1.07 | 32 | STOP | 2.09 | 0.92 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 12 | 2026-04-26 23:00 | BUY | 78241.2 | 77848.7 | -1.00 | 1.71 | 1.04 | 2 | STOP | 1.66 | 0.73 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 13 | 2026-04-27 01:00 | BUY | 78421.2 | 78017.9 | -1.00 | 1.03 | 1.15 | 1 | STOP | 1.19 | 0.62 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 14 | 2026-04-27 06:00 | BUY | 79142.1 | 78248.3 | -1.00 | 0.19 | 1.75 | 3 | STOP | 2.14 | 0.82 | no | IMMEDIATE_ADVERSE_MOVE |
| 15 | 2026-04-28 00:00 | SELL | 76953.0 | 77645.7 | -1.00 | 1.88 | 1.21 | 37 | STOP | 1.75 | 0.11 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 16 | 2026-04-29 22:00 | SELL | 75496.9 | 76339.9 | -1.00 | 0.25 | 1.13 | 7 | STOP | 1.76 | 0.21 | no | STOPPED_WITHOUT_PROGRESS |
| 17 | 2026-05-04 06:00 | BUY | 80190.6 | 79464.4 | -1.00 | 0.59 | 2.74 | 8 | STOP | 1.67 | 0.94 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 18 | 2026-05-05 08:00 | BUY | 80909.2 | 79797.9 | -1.00 | 1.73 | 1.10 | 59 | STOP | 2.19 | 0.88 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 19 | 2026-05-07 19:00 | SELL | 79893.3 | 80647.5 | -1.00 | 0.94 | 1.02 | 37 | STOP | 1.73 | 0.05 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 20 | 2026-05-09 22:00 | BUY | 80919.3 | 80541.0 | -1.00 | 1.72 | 1.76 | 26 | STOP | 1.52 | 0.86 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 21 | 2026-05-11 03:00 | BUY | 82232.0 | 81464.4 | -1.00 | 0.18 | 1.26 | 1 | STOP | 1.71 | 0.54 | no | IMMEDIATE_ADVERSE_MOVE |
| 22 | 2026-05-13 19:00 | SELL | 78818.3 | 79499.4 | -1.00 | 0.10 | 1.09 | 2 | STOP | 1.58 | 0.14 | no | IMMEDIATE_ADVERSE_MOVE |
| 23 | 2026-05-18 09:00 | SELL | 76912.0 | 77655.6 | -1.00 | 0.45 | 1.19 | 7 | STOP | 2.12 | 0.16 | no | STOPPED_AFTER_MINOR_PROGRESS |
| 24 | 2026-05-18 18:00 | SELL | 76389.6 | 77182.0 | -1.00 | 0.46 | 1.00 | 7 | STOP | 1.82 | 0.15 | no | STOPPED_AFTER_MINOR_PROGRESS |
| 25 | 2026-05-23 12:00 | SELL | 74665.8 | 75397.9 | -1.00 | 0.08 | 1.40 | 6 | STOP | 2.13 | 0.12 | no | IMMEDIATE_ADVERSE_MOVE |
| 26 | 2026-05-24 19:00 | SELL | 76363.3 | 76920.1 | -1.00 | 0.49 | 1.15 | 7 | STOP | 1.61 | 0.61 | yes | STOPPED_AFTER_MINOR_PROGRESS |
| 27 | 2026-05-28 07:00 | SELL | 73248.3 | 74122.0 | -1.00 | 0.86 | 1.08 | 36 | STOP | 1.84 | 0.13 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 28 | 2026-06-01 00:00 | SELL | 73738.8 | 74123.1 | -1.00 | 0.63 | 1.19 | 3 | STOP | 1.79 | 0.57 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 29 | 2026-06-04 04:00 | SELL | 63333.6 | 64538.2 | -1.00 | 1.64 | 1.18 | 4 | STOP | 1.53 | 0.01 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 30 | 2026-06-05 20:00 | SELL | 61377.9 | 63274.5 | -1.00 | 1.19 | 1.51 | 54 | STOP | 1.93 | 0.24 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 31 | 2026-06-08 04:00 | BUY | 63652.6 | 62463.4 | -1.00 | 0.00 | 1.06 | 5 | STOP | 1.73 | 0.66 | no | IMMEDIATE_ADVERSE_MOVE |
| 32 | 2026-06-09 21:00 | SELL | 61687.2 | 62634.2 | -1.00 | 1.00 | 1.23 | 22 | STOP | 1.79 | 0.33 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 33 | 2026-06-14 14:00 | BUY | 64537.1 | 64163.6 | -1.00 | 0.26 | 1.82 | 4 | STOP | 1.73 | 0.75 | no | STOPPED_AFTER_MINOR_PROGRESS |
| 34 | 2026-06-14 20:00 | SELL | 63933.0 | 64330.3 | -1.00 | 0.65 | 4.38 | 5 | STOP | 1.66 | 0.04 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 35 | 2026-06-15 19:00 | BUY | 67306.2 | 66632.5 | -1.00 | 0.00 | 1.43 | 4 | STOP | 1.72 | 0.96 | no | IMMEDIATE_ADVERSE_MOVE |
| 36 | 2026-06-16 00:00 | BUY | 66535.4 | 65822.4 | -1.00 | 0.03 | 1.20 | 6 | STOP | 1.93 | 0.61 | no | IMMEDIATE_ADVERSE_MOVE |
| 37 | 2026-06-18 20:00 | SELL | 62672.1 | 63464.1 | -1.00 | 0.53 | 1.25 | 31 | STOP | 1.52 | 0.09 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 38 | 2026-06-20 10:00 | BUY | 63754.9 | 63234.3 | -1.00 | 0.74 | 1.09 | 8 | STOP | 1.76 | 0.84 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 39 | 2026-06-23 13:00 | SELL | 62368.8 | 63133.2 | -1.00 | 0.56 | 1.12 | 26 | STOP | 1.84 | 0.10 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 40 | 2026-06-25 20:00 | SELL | 59298.0 | 60653.1 | -1.00 | 0.72 | 1.07 | 15 | STOP | 1.78 | 0.41 | yes | GAVE_BACK_FAVOURABLE_MOVE |
| 41 | 2026-06-27 18:00 | BUY | 60627.3 | 60185.1 | -1.00 | 0.69 | 1.26 | 5 | STOP | 1.24 | 0.93 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 42 | 2026-06-29 04:00 | SELL | 59654.5 | 60410.5 | -1.00 | 1.02 | 1.50 | 12 | STOP | 1.76 | 0.33 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 43 | 2026-06-30 22:00 | SELL | 58671.4 | 59392.2 | -1.00 | 1.20 | 1.09 | 10 | STOP | 1.76 | 0.26 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 44 | 2026-07-04 22:00 | BUY | 63175.3 | 62787.8 | -1.00 | 0.71 | 1.00 | 7 | STOP | 1.42 | 0.87 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 45 | 2026-07-06 04:00 | BUY | 63761.8 | 63226.1 | -1.00 | 0.27 | 1.20 | 3 | STOP | 1.65 | 0.73 | no | STOPPED_AFTER_MINOR_PROGRESS |
| 46 | 2026-07-06 07:00 | BUY | 63309.2 | 62712.4 | -1.00 | 0.13 | 1.16 | 6 | STOP | 1.88 | 0.53 | no | IMMEDIATE_ADVERSE_MOVE |
| 47 | 2026-07-07 04:00 | BUY | 64211.9 | 63190.3 | -1.00 | 0.00 | 1.05 | 3 | STOP | 2.30 | 0.74 | no | IMMEDIATE_ADVERSE_MOVE |
| 48 | 2026-07-10 18:00 | BUY | 63929.4 | 63274.4 | -1.00 | 0.88 | 1.08 | 60 | STOP | 1.74 | 0.70 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 49 | 2026-07-17 12:00 | SELL | 62872.5 | 63424.0 | -1.00 | 0.64 | 1.15 | 6 | STOP | 1.73 | 0.14 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 50 | 2026-07-21 12:00 | BUY | 66243.7 | 65656.4 | -1.00 | 1.21 | 1.20 | 28 | STOP | 1.72 | 0.97 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 51 | 2026-07-24 18:00 | SELL | 64045.0 | 64662.2 | -1.00 | 0.41 | 1.16 | 48 | STOP | 1.77 | 0.17 | no | STOPPED_AFTER_MINOR_PROGRESS |
| 52 | 2026-07-27 03:00 | BUY | 65417.4 | 65091.2 | -1.00 | 0.00 | 1.12 | 1 | STOP | 1.63 | 0.66 | no | IMMEDIATE_ADVERSE_MOVE |
| 53 | 2026-07-27 04:00 | BUY | 65149.9 | 64793.9 | -1.00 | 1.65 | 1.97 | 14 | STOP | 1.71 | 0.71 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 54 | 2026-07-28 08:00 | SELL | 63339.0 | 64083.0 | -1.00 | 0.81 | 1.02 | 12 | STOP | 2.29 | 0.15 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 55 | 2026-07-30 01:00 | SELL | 63841.2 | 64706.2 | -1.00 | 0.29 | 1.20 | 14 | STOP | 1.91 | 0.45 | yes | STOPPED_AFTER_MINOR_PROGRESS |
| 56 | 2026-07-30 15:00 | BUY | 64809.0 | 64258.9 | -1.00 | 1.08 | 1.13 | 15 | STOP | 1.63 | 0.94 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 57 | 2026-07-31 20:00 | SELL | 62855.9 | 63472.6 | -1.00 | 0.96 | 1.11 | 34 | STOP | 1.76 | 0.27 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 58 | 2026-08-03 11:00 | SELL | 62607.7 | 63091.4 | -1.00 | 0.67 | 1.61 | 6 | STOP | 2.05 | 0.17 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 59 | 2026-08-08 19:00 | BUY | 65087.2 | 64943.7 | -1.00 | 0.34 | 1.09 | 7 | STOP | 1.16 | 0.84 | no | STOPPED_AFTER_MINOR_PROGRESS |
| 60 | 2026-08-09 06:00 | SELL | 64809.3 | 64984.5 | -1.00 | 0.53 | 1.03 | 9 | STOP | 1.75 | 0.13 | no | GAVE_BACK_FAVOURABLE_MOVE |
| 61 | 2026-08-09 18:00 | BUY | 65278.7 | 65110.4 | -1.00 | 0.00 | 1.27 | 6 | STOP | 1.65 | 0.87 | no | IMMEDIATE_ADVERSE_MOVE |
| 62 | 2026-08-10 11:00 | BUY | 65219.4 | 64798.7 | -1.00 | 0.23 | 1.70 | 6 | STOP | 2.21 | 0.66 | no | STOPPED_WITHOUT_PROGRESS |

## 5. Market conditions

### By market regime

| Regime | Trades | Win rate | Avg R | Total R |
|---|---:|---:|---:|---:|
| TREND_BEAR | 39 | 41.0% | +0.115 | +4.50 |
| TREND_BULL | 39 | 20.5% | -0.502 | -19.57 |
| BREAKOUT | 10 | 20.0% | -0.500 | -5.00 |
| COMPRESSION | 1 | 100.0% | +2.000 | +2.00 |

### By volatility at entry (ATR percentile over the trailing 200 bars)

| ATR percentile | Trades | Win rate | Avg R | Total R |
|---|---:|---:|---:|---:|
| Q1 lowest vol | 19 | 42.1% | -0.004 | -0.07 |
| Q2 | 28 | 17.9% | -0.589 | -16.50 |
| Q3 | 13 | 38.5% | +0.038 | +0.50 |
| Q4 highest vol | 29 | 31.0% | -0.069 | -2.00 |

### By direction and trend alignment

| Group | Trades | Win rate | Avg R | Total R |
|---|---:|---:|---:|---:|
| BUY | 45 | 24.4% | -0.390 | -17.57 |
| SELL | 44 | 36.4% | -0.011 | -0.50 |
| with-trend | 84 | 32.1% | -0.156 | -13.07 |
| counter-trend | 5 | 0.0% | -1.000 | -5.00 |

## 6. Parameter counterfactuals (same entries, different parameters)

Each row re-simulates the **identical entries** — same entry price, same entry bar, same original stop — changing only the parameter named. This separates 'the entries were bad' from 'the parameters were wrong'.

### 6a. Target distance (`tp_r`, in multiples of initial risk)

| tp_r | Trades | Win rate | Expectancy (R) | Total R | Avg win | Avg loss | PF |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0.25 | 89 | 75.3% | -0.0975 | -8.68 | +0.213 | -1.042 | 0.62 |
| 0.3 | 89 | 73.0% | -0.0890 | -7.93 | +0.264 | -1.045 | 0.68 |
| 0.4 | 89 | 67.4% | -0.0947 | -8.43 | +0.366 | -1.047 | 0.72 |
| 0.5 | 89 | 61.8% | -0.1115 | -9.93 | +0.466 | -1.045 | 0.72 |
| 0.75 | 89 | 52.8% | -0.1143 | -10.18 | +0.716 | -1.043 | 0.77 |
| 1 | 89 | 48.3% | -0.0789 | -7.02 | +0.952 | -1.042 | 0.85 |
| 1.5 | 89 | 38.2% | -0.1165 | -10.36 | +1.334 | -1.013 | 0.81 |
| 2 | 89 | 33.7% | -0.1248 | -11.11 | +1.627 | -1.015 | 0.81 |
| 3 | 89 | 27.0% | -0.1904 | -16.94 | +2.029 | -1.010 | 0.74 |

### 6b. Stop distance (multiple of the original stop, target held fixed in R:R)

The target widens with the stop, so this scales the whole trade envelope to a different volatility band while keeping reward:risk unchanged.

| Stop × | Trades | Win rate | Expectancy (R) | Total R |
|---|---:|---:|---:|---:|
| 0.75× | 89 | 27.0% | -0.1940 | -17.27 |
| 1× | 89 | 28.1% | -0.2158 | -19.20 |
| 1.5× | 89 | 34.8% | -0.0989 | -8.80 |
| 2× | 89 | 37.1% | -0.1652 | -14.70 |
| 3× | 89 | 40.5% | -0.1252 | -11.15 |

### 6c. Stop distance with the target held at its ORIGINAL price

Here only the stop moves — the target stays exactly where the strategy put it. If expectancy improves, the stop was genuinely too tight rather than the target too close. This is the cleanest test of 'are we being stopped out by noise?'.

| Stop × | Trades | Win rate | Expectancy (R) | Total R |
|---|---:|---:|---:|---:|
| 0.75× | 89 | 20.2% | -0.3276 | -29.15 |
| 1× | 89 | 28.1% | -0.2157 | -19.20 |
| 1.5× | 89 | 38.2% | -0.0770 | -6.85 |
| 2× | 89 | 41.6% | -0.1155 | -10.28 |
| 3× | 89 | 46.1% | -0.1113 | -9.90 |

## 7. What is actually wrong

**Dominant failure mode: `GAVE_BACK_FAVOURABLE_MOVE`** — 35 of 62 losses (56%), costing -35.00 R. Gave back a favourable move: the trade ran into profit, then reversed all the way to the stop. Exit management, not entry selection.

**62 of 62 losses are stop-outs** and 0 are time stops — so the loss mix is dominated by premature stop-outs.

**The stop is too tight for this instrument.** Holding the target at exactly the price the strategy chose and moving only the stop, expectancy rises from -0.2157 R at 1× to -0.0770 R at 1.5× (win rate 28.1% → 38.2%). Because only the stop moved, this is noise stop-out, not a target that was set too close.

**5 losses were taken against the 24-bar trend** and went at least 0.75R against immediately afterwards.

**26 losses were entered at the extreme of the 24-bar range** (bought in the top 15% / sold in the bottom 15%) — chasing.

**11 losses occurred in the highest-volatility quartile** (ATR ≥ 85th percentile of the trailing 200 bars).

## 8. Method and limitations

* Real MT5 H1 bars for `BTCUSD` (BTCUSD#), 4392 bars, 2026-03-14 07:00:00+00:00 → 2026-09-13 06:00:00+00:00; provenance `MT5_TERMINAL_REAL`.
* Execution is the production `BacktestEngine`: entry at the next bar's open, spread paid on the traded side, stop tested before target within a bar (conservative — a bar spanning both is booked as a loss).
* Costs: median spread 2250.00 pips from the data plus 0.5 pips slippage per side. Swap/financing on crypto positions is NOT modelled, so a real long-held BTC position would carry additional financing cost.
* Failure attribution uses only the engine's own outputs (exit reason, MFE, MAE, bars held) plus market context computed from the same bars. Each rule is a numeric predicate; the ledger shows the numbers.
* MFE/MAE are bar-resolution excursions, so they understate true intra-bar extremes on a volatile instrument like BTC.
* One instrument, one window. 89 trades is a small sample: per-bucket win rates below carry wide confidence intervals.
