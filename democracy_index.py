# %% [markdown]
# # Democracy Index Forecasting Notebook

# %% [markdown]
# ### Environment Setup and Data Loading

# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from prophet import Prophet
import logging
logging.getLogger('cmdstanpy').disabled = True

df = pd.read_csv("democracy-index-eiu.csv")

df = df.rename(columns={
    "Entity": "country",
    "Code": "code",
    "Year": "year",
    "Democracy score": "score"
})

df["year"] = df["year"].astype(int)
df["score"] = df["score"].astype(float)

# %% [markdown]
# ### Exploratory Data Analysis (EDA)
# - #### Data Overview

# %%
display(df.head())
print("\nInfo:")
display(df.info())

# %% [markdown]
# - #### Dataset Coverage

# %%
print("\n=== Coverage ===")
print("Number of countries:", df.country.nunique())
print("Years covered:", df.year.min(), "→", df.year.max())

country_counts = df.groupby("country").size().sort_values()
print("\n=== Observations per Country (smallest shown first) ===")
display(country_counts.head(10))

# %% [markdown]
# - #### Missing Values

# %%
print("=== Basic Missing Value Check ===")
display(df.isna().sum())

year_counts = df.groupby("year").size()

print("\n=== Counts Per Year (How many country entries each year) ===")
display(year_counts)

expected_years = list(range(df["year"].min(), df["year"].max() + 1))
actual_years = sorted(df["year"].unique())

missing_years = sorted(set(expected_years) - set(actual_years))

print("\n=== Missing Entire Years in Dataset ===")
if missing_years:
    print("Missing years:", missing_years)
else:
    print("No completely missing years.")

missing_by_country = (
    df.groupby("country")["score"]
      .apply(lambda x: x.isna().sum())
)

missing_by_country = missing_by_country[missing_by_country > 0]

print("\n=== Countries With Missing Scores ===")
if len(missing_by_country) > 0:
    display(missing_by_country.sort_values())
else:
    print("No missing country-level values.")

if "Australia" in missing_by_country.index:
    print("\n⚠️ Note: Australia is missing exactly one value (year 2009).")

START_YEAR = 2010
print(f"\n=== Filtering dataset to years >= {START_YEAR} ===")

df = df[df["year"] >= START_YEAR].reset_index(drop=True)

print(f"Data now includes years: {sorted(df['year'].unique())[:5]} … {sorted(df['year'].unique())[-5:]}")
print(f"Total rows after filtering: {len(df)}")

df.head()


# %% [markdown]
# - #### Global democracy trend over time

# %%
global_trend = (
    df.groupby("year")["score"]
      .mean()
      .reset_index()
      .sort_values("year")
)

plt.figure(figsize=(12, 5))
plt.plot(global_trend["year"], global_trend["score"], marker="o", linewidth=2)

plt.title("Global Average Democracy Score Over Time (2010–2024)", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Average Democracy Score", fontsize=12)

plt.xticks(
    ticks=global_trend["year"],
    labels=global_trend["year"].astype(str),
    rotation=45
)

plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()


# %% [markdown]
# ### Data Preparation for Prophet

# %%
all_years = pd.Series(range(df.year.min(), df.year.max() + 1))


def prepare_country_df(df, country_name):
    temp = df[df.country == country_name].copy()

    full_df = pd.DataFrame({"year": all_years})

    merged = full_df.merge(temp, on="year", how="left")

    merged["ds"] = pd.to_datetime(merged["year"], format="%Y")

    merged["y"] = merged["score"]

    prophet_df = merged[["ds", "y"]].sort_values("ds").reset_index(drop=True)
    
    return prophet_df


# %% [markdown]
# ### Prophet Forecasting Function

# %%
def forecast_country(df, country_name, periods=6):

    country_df = prepare_country_df(df, country_name)

    model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.7
    )

    model.fit(country_df)

    future = model.make_future_dataframe(periods=periods, freq='YE')

    future["ds"] = future["ds"].dt.to_period("Y").dt.to_timestamp("Y")

    forecast = model.predict(future)

    forecast["yhat"] = forecast["yhat"].clip(0, 10)
    forecast["yhat_lower"] = forecast["yhat_lower"].clip(0, 10)
    forecast["yhat_upper"] = forecast["yhat_upper"].clip(0, 10)

    return forecast, model, country_df

# %%
# =============================================
# QUICK SANITY CHECK: sample countries
# =============================================

sample_countries = ["Afghanistan", "Zimbabwe", "Australia", "United States", "China"]

for country in sample_countries:
    country_df = df[df["country"] == country].sort_values("year")
    print(f"\n=== {country} ===")
    print(country_df[["year", "score"]])


# %% [markdown]
# ### Multi-Country Forecasting Loop (2025–2030)

# %%
all_forecasts = []

FORECAST_YEARS = 7   # 2025–2030

countries = df.country.unique()

print(f"Forecasting {len(countries)} countries...")

for country in countries:
    try:
        forecast, model, country_df = forecast_country(df, country, periods=FORECAST_YEARS)

        forecast["country"] = country

        future_rows = forecast[forecast["ds"].dt.year >= df.year.max() + 1]

        future_rows = future_rows[[
            "country",
            "ds",
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ]]
        
        all_forecasts.append(future_rows)
    
    except Exception as e:
        print(f"⚠️ Error forecasting {country}: {e}")
        continue

final_forecast_df = pd.concat(all_forecasts, ignore_index=True)

print("\nForecasting completed!")
display(final_forecast_df.head())
display(final_forecast_df.tail())


# %% [markdown]
# ### Combine Historical + Forecast

# %%
historical_df = df.rename(columns={"year": "ds", "score": "y"})
historical_df["ds"] = pd.to_datetime(historical_df["ds"], format="%Y")

combined = pd.concat([
    historical_df[["country", "ds", "y"]].rename(columns={"y": "value"}),
    final_forecast_df.rename(columns={"yhat": "value"})[["country", "ds", "value"]]
], ignore_index=True)

# %% [markdown]
# ### Regime Classification for Historical + Forecasted Scores

# %%
def classify_regime(score):

    if pd.isna(score):
        return None
    if score >= 8.01:
        return "Full Democracy"
    elif score >= 6.01:
        return "Flawed Democracy"
    elif score >= 4.01:
        return "Hybrid Regime"
    else:
        return "Authoritarian"

combined["regime"] = combined["value"].apply(classify_regime)

transition_df = combined[combined["ds"].dt.year >= df.year.max() + 1].copy()

latest_year = df.year.max()

latest_hist = (
    combined[combined["ds"].dt.year == latest_year]
    .groupby("country")["regime"]
    .first()
    .reset_index()
    .rename(columns={"regime": "regime_2024"})
)

forecast_target_year = latest_year + 6  # 2024 -> 2030
forecast_target = (
    combined[combined["ds"].dt.year == forecast_target_year]
    .groupby("country")["regime"]
    .first()
    .reset_index()
    .rename(columns={"regime": f"regime_{forecast_target_year}"})
)

regime_transitions = latest_hist.merge(forecast_target, on="country", how="left")

regime_transitions["changed_regime"] = (
    regime_transitions[f"regime_{forecast_target_year}"] 
    != regime_transitions["regime_2024"]
)

print("Regime classification + transitions generated.")
display(regime_transitions.head())

# %% [markdown]
# ### Final Dataset for Tableau

# %%
final_forecast_df["ds"] = (
    final_forecast_df["ds"]
    .dt.to_period("Y")
    .dt.to_timestamp("Y")
)

final_forecast_df = final_forecast_df.rename(columns={"yhat": "value"})

historical_df = df.rename(columns={"year": "ds", "score": "value"})
historical_df["ds"] = pd.to_datetime(historical_df["ds"], format="%Y")
historical_df["source"] = "historical"

historical_df = historical_df[["country", "ds", "value", "source"]]

forecast_clean = final_forecast_df[["country", "ds", "value"]].copy()
forecast_clean["source"] = "forecast"

combined_final = pd.concat([historical_df, forecast_clean], ignore_index=True)

combined_final["regime"] = combined_final["value"].apply(classify_regime)

combined_final = combined_final.sort_values(["country", "ds"]).reset_index(drop=True)

combined_final["ds"] = pd.to_datetime(combined_final["ds"], errors="coerce")

combined_final["ds"] = (
    combined_final["ds"].dt.year.astype(str) + "-01-01"
)
combined_final["ds"] = pd.to_datetime(combined_final["ds"])

combined_final.to_csv("final_democracy_forecast_clean.csv", index=False)

print("Cleaned export created: final_democracy_forecast_clean.csv")
display(combined_final.head())
display(combined_final.tail())


