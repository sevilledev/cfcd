# Cloud Database Capacity Forecasting

A minimal demo project for forecasting cloud database workloads and automatically planning instance schedules to **reduce costs while maintaining SLA compliance**.

---

## 🚀 Problem

Cloud databases are expensive:

* **Over-provisioning** wastes money.
* **Under-provisioning** risks downtime and SLA violations.

We need a system that balances cost and reliability automatically.

---

## 💡 Solution

This project implements a **forecasting + scheduling service**:

1. **Forecast** hourly workload (CPU%, IOPS, Credits) using historical data.
2. **Plan** cheapest instance per hour, based on P90 demand and safety headroom (α).
3. **Backtest** against history to ensure under-provision ≤ ε%.

---

## 📂 Project Structure

```
project/
 ├─ app.py                # CLI entrypoint
 ├─ core/
 │   ├─ forecast.py        # P90 forecasting from history
 │   ├─ plan.py            # Schedule builder (choose instances)
 │   └─ __init__.py
 ├─ data/
 │   └─ metrics.csv        # Sample input data (24h workload)
 ├─ config/
 │   └─ catalog.yaml       # Instance types, costs, α, ε
 └─ requirements.txt       # Python dependencies
```

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### 1. Forecast workload

```bash
python app.py forecast data/metrics.csv config/catalog.yaml
```

→ Outputs **`forecast.csv`** with hourly P90 predictions.

### 2. Plan instance schedule

```bash
python app.py plan forecast.csv config/catalog.yaml
```

→ Outputs **`schedule.csv`** with cheapest instance per hour.

### 3. Backtest reliability

```bash
python app.py backtest data/metrics.csv config/catalog.yaml
```

→ Prints under-provision risk, e.g.:

```
Approximate under-provision rate on history: 0.083
```

---

## 📊 Example Outputs

**forecast.csv (first 3 rows):**

```
ts,cpu_pct,iops,credits
2025-08-02 00:00,54.0,1350.0,3.6
2025-08-02 01:00,40.0,900.0,2.4
2025-08-02 02:00,25.0,600.0,1.7
```

**schedule.csv (first 3 rows):**

```
ts,instance,cost_per_hour
2025-08-02 00:00,db.medium,0.19
2025-08-02 01:00,db.small,0.10
2025-08-02 02:00,db.small,0.10
```

---

## 📝 Code Overview

* **`app.py`**
  CLI with 3 commands: `forecast`, `plan`, `backtest`.
* **`core/forecast.py`**
  Groups historical metrics by hour-of-week, computes **90th percentile forecast**.
* **`core/plan.py`**
  Contains `build_schedule()` that picks cheapest instance per hour given α.
* **`backtest` logic (in app.py)**
  Reuses `build_schedule()` on historical data, measures **under-provision rate**.

---

## ✅ What We Achieved

* Automatic workload forecasting.
* Cost-aware scheduling under SLA constraints.
* Risk control: system tuned α = 1.3 to reach under-provision ≈ 8%.
