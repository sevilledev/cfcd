import pandas as pd
import numpy as np

def hour_of_week(s):
    # Monday=0..Sunday=6 => 0..167
    return s.dt.dayofweek * 24 + s.dt.hour

def p90_hourly_forecast(df: pd.DataFrame, metrics, horizon_hours=168, lookback_weeks=6):
    df = df.copy()
    df['ts'] = pd.to_datetime(df['ts'])
    df = df.sort_values('ts')
    df['how'] = hour_of_week(df['ts'])

    # use last K weeks
    cutoff = df['ts'].max() - pd.Timedelta(weeks=lookback_weeks)
    hist = df[df['ts'] > cutoff]

    # p90 per hour-of-week
    p90_by_how = (
        hist.groupby('how')[metrics]
        .quantile(0.90)
        .reindex(range(168))          # fill all 0..167
        .interpolate()
        .bfill()
        .ffill()
    )

    # build next-week horizon by repeating hour-of-week template
    future_idx = pd.date_range(df['ts'].max() + pd.Timedelta(hours=1),
                               periods=horizon_hours, freq='H')
    out = pd.DataFrame({'ts': future_idx})
    out['how'] = hour_of_week(out['ts'])
    for m in metrics:
        out[m] = out['how'].map(p90_by_how[m])
    return out.drop(columns=['how'])
