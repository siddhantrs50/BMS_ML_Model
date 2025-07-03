import pandas as pd

def prepare_vehicle_daily_summary(df):
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["date"] = df["created_at"].dt.date

    summary = df.groupby(["vehicleid", "date"]).agg({
        "total_pack_voltage": "mean",
        "total_pack_current": "mean",
        "state_of_charge": "mean",
        "state_of_health": "mean",
        "total_energy_throughput": "mean",
        "max_cell_voltage": "max",
        "max_cell_temp": "max",
        "max_cell_reading": "max",
        "min_cell_reading": "min",
        "average_cell_temp": "mean",
        "internal_resistance": "mean",
        "estimated_range": "mean"
    }).reset_index()

    return summary