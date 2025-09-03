import pandas as pd

def choose_instance(row, instances, metrics, alpha):
    for inst in sorted(instances, key=lambda x: x['cost_per_hour']):
        ok = all(row[m] <= alpha * inst['cap'][m] for m in metrics)
        if ok:
            return inst['name'], inst['cost_per_hour']
    # if nothing fits, take the biggest
    big = max(instances, key=lambda x: x['cost_per_hour'])
    return big['name'], big['cost_per_hour']

def build_schedule(forecast_df, catalog):
    metrics = catalog['metrics']
    alpha = float(catalog['alpha'])
    insts = catalog['instances']
    rows = []
    for _, r in forecast_df.iterrows():
        name, cost = choose_instance(r, insts, metrics, alpha)
        rows.append({ 'ts': r['ts'], 'instance': name, 'cost_per_hour': cost, **{m: r[m] for m in metrics}})
    return pd.DataFrame(rows)
