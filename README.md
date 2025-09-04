# Cloud Database Capacity Forecasting

A demo project that forecasts cloud database workloads and **automatically chooses the cheapest instance size** while still keeping performance reliable.

---

## 📌 Problem

* If we **over-provision** cloud databases → money is wasted.
* If we **under-provision** → the system risks downtime and SLA violations.
* Cloud teams need a way to balance **cost vs. reliability** automatically.

---

## 💡 Our Solution

1. **Forecast demand**

   * For each hour of the week, we predict workload (CPU, IOPS, Credits).
   * We use **P90 forecast** → a high but not extreme value, covering 90% of cases.

2. **Choose instances**

   * We define instance types in a catalog:

     * `db.small` = cheap but low capacity
     * `db.medium` = more capacity, more expensive
     * `db.large` = high capacity, highest price
   * The system picks the **cheapest instance** that can safely handle the forecast.

3. **Control risk**

   * Add a safety margin (α).
   * Limit under-provisioning risk to ≤ ε% (example: ≤ 8%).

---

## 📂 Project Structure

```
project/
 ├─ app.py                # CLI entrypoint
 ├─ core/
 │   ├─ forecast.py        # Builds P90 forecast
 │   ├─ plan.py            # Chooses cheapest instance
 │   └─ __init__.py
 ├─ data/
 │   └─ metrics.csv        # Sample hourly workload data
 ├─ config/
 │   └─ catalog.yaml       # Instance types, capacities, costs
 └─ requirements.txt       # Dependencies
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

👉 Generates **forecast.csv** with predicted hourly workload (P90).

### 2. Plan instance schedule

```bash
python app.py plan forecast.csv config/catalog.yaml
```

👉 Generates **schedule.csv** with cheapest instance per hour.

### 3. Backtest on history

```bash
python app.py backtest data/metrics.csv config/catalog.yaml
```

👉 Prints under-provision rate, e.g.:

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

## 📝 Code Explanation

* **`forecast.py`** → Calculates **P90 forecast per hour** using historical data.
* **`plan.py`** → Contains `build_schedule()`, which picks the cheapest instance that satisfies demand with safety margin α.
* **`app.py`** → CLI with 3 commands: `forecast`, `plan`, `backtest`.
* **`catalog.yaml`** → Defines instance sizes (`db.small`, `db.medium`, `db.large`), their capacities, and hourly cost.

---

## ✅ Results

* The system automatically adjusted **α = 1.3**, keeping under-provision risk ≈ **8.3%**.
* This means **cheaper scaling** while still keeping SLA reliability.
