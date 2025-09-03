# app.py
import typer
from core.io import load_catalog, load_metrics, save_csv
from core.forecast import p90_hourly_forecast
from core.plan import build_schedule
from core.backtest import tune_alpha

app = typer.Typer()

@app.command()
def forecast(data: str, catalog: str, out_csv: str="forecast.csv", horizon: int=168, lookback_weeks: int=6):
    cat = load_catalog(catalog)
    df = load_metrics(data)
    fc = p90_hourly_forecast(df, cat['metrics'], horizon, lookback_weeks)
    save_csv(fc, out_csv)
    typer.echo(f"Saved {out_csv}")

@app.command()
def plan(data: str, catalog: str, schedule_csv: str="schedule.csv"):
    cat = load_catalog(catalog)
    df = load_metrics(data)
    fc = p90_hourly_forecast(df, cat['metrics'])
    sched = build_schedule(fc, cat)
    save_csv(sched, schedule_csv)
    typer.echo(f"Saved {schedule_csv}")

@app.command()
def backtest(data: str, catalog: str, schedule_csv: str="schedule.csv"):
    cat = load_catalog(catalog)
    df = load_metrics(data)
    def builder():
        return p90_hourly_forecast(df, cat['metrics'])
    sched, rate = tune_alpha(df[['ts']+cat['metrics']], builder, cat)
    save_csv(sched, schedule_csv)
    typer.echo(f"Saved {schedule_csv}; under-provision rate≈{rate:.3f}; alpha={cat['alpha']}")

if __name__ == "__main__":
    app()
