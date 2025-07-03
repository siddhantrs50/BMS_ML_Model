import pandas as pd

def prepare_vehicle_summary(df):
    summary = df.groupby("vehicleid").agg({
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