import pandas as pd

from core.plan import build_schedule

def underprov_rate(actuals: pd.DataFrame, schedule_like: pd.DataFrame, catalog) -> float:
    # map instance -> caps
    cap = {i['name']: i['cap'] for i in catalog['instances']}
    metrics = catalog['metrics']
    # align on hour
    df = actuals.merge(schedule_like[['ts','instance']], on='ts', how='inner')
    def under(row):
        caps = cap[row['instance']]
        return any(row[m] > caps[m] for m in metrics)  # headroom already in selection when schedule_like was created
    return df.apply(under, axis=1).mean()

def tune_alpha(actuals, forecast_builder, catalog, max_steps=10, step=0.02):
    for _ in range(max_steps):
        fc = forecast_builder()           # closure returns p90 forecast with current data
        sched = build_schedule(fc, catalog)
        hist_sched = build_schedule(actuals[['ts']+catalog['metrics']], catalog)  # same picker over history
        rate = underprov_rate(actuals, hist_sched, catalog)
        if rate <= catalog['epsilon']:
            return sched, rate
        catalog['alpha'] = round(float(catalog['alpha']) + step, 3)
    return sched, rate
