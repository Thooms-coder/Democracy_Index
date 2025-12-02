# IA 640 Project 1 — Democracy Index Visualization  
**Author:** Mutsa Mungoshi  
**Course:** IA 640 – Data Visualization  
**Institution:** Clarkson University  

---
## Project Overview
This project presents an interactive Tableau visualization that examines global democracy patterns from 2010 to 2030. The visualization incorporates both historical democracy index values and forecasted trajectories. The design follows the IA 640 workflow of data abstraction, encoding decisions, idiom selection, and evaluation to effectively communicate spatial and temporal variation in democratic governance.

**Live Visualization:**  
[View on GitHub Pages](https://thooms-coder.github.io/Democracy_Index/)

## Dashboard Previews

### Dashboard 1
[![Dashboard 1](images/Dashboard%201.png)](https://public.tableau.com/app/profile/mutsa.mungoshi/viz/Democracy_Dashboard_1/Dashboard1)

### Dashboard 2
[![Dashboard 2](images/Dashboard%202.png)](https://public.tableau.com/app/profile/mutsa.mungoshi/viz/Democracy_Dashboard_2/Dashboard2)

---

## Step 1: Dataset Selection
The dataset is derived from the Economist Intelligence Unit (EIU) Democracy Index, an annual measure of democratic quality across countries. The data spans historical years (2010–2024) with an extended modeled forecast to 2030. The dataset was selected based on the IA 640 criteria of diversity, quantity, quality, and novelty:

- **Diversity:** Includes spatial (country), temporal (year), and quantitative (democracy index) attributes. 
- **Quantity:** It includes a sufficiently large temporal span (2006–2024) for longitudinal analysis.  
- **Quality:** Standardized scoring (0–10 scale) and consistent methodology across years. 
- **Novelty:** The dataset provides opportunities for examining underexplored global democratic trends.

The dataset reports **Democracy Index scores** for multiple countries, based on 60 indicators grouped into five dimensions:
1. Electoral process and pluralism  
2. Functioning of government  
3. Political participation  
4. Political culture  
5. Civil liberties  

---

## Step 2: Abstraction and Analysis
**Main Objective:** The primary objective is to analyze how democracy varies across countries and regions and how these patterns evolve over time.

### Key Variables
| Variable | Type | Description |
|-----------|------|-------------|
| Country | Categorical (Spatial) | Used for faceting and spatial encoding in map visualizations. |
| Year | Interval | Represents the temporal axis and supports time-series analysis. |
| Democracy Index | Quantitative | Encoded with color and position; discretized into 10 bins to enhance clarity. |

### Analytical focus
- Temporal change within countries and regions. 
- Spatial variation across continents.
- Distributional differences across regions.
- Regime categorization and global composition.

---

## Step 3: Visual Idioms and Justification

**Choropleth Map**
Used to present global variation in democracy levels for a selected year. A diverging blue–orange color palette highlights democratic versus authoritarian tendencies. This idiom supports spatial comparison and pop-out effects.
**Box-and-Whisker Plot by Region**
Displays the distribution of democracy index values across the world’s major regions. This idiom reveals median scores, interquartile ranges, and outliers, emphasizing regional inequality and variation.
**Treemap of Regime Types**
Summarizes the proportion of countries categorized as full democracies, flawed democracies, hybrid regimes, or authoritarian regimes. This provides an immediate overview of global regime structure.
**Regional Line Chart with Forecast**
Shows historical and forecasted democracy index trajectories for each region from 2010 to 2030. Regime thresholds, reference lines, and a shaded forecast period provide contextual information and support interpretability.

---

## Step 4: Interactivity and Design Considerations
The visualization incorporates several interactive and encoding features consistent with Information Visualization principles::
- Year slider enabling temporal exploration from 2010 to 2030.
- Region filter for isolating specific regional trends.
- Hover tooltips displaying exact democracy index values.
- Consistent color encoding across all views.
- Annotations clarifying the forecast period and regime thresholds.
- Automatic axis scaling and smoothing to improve readability.  

---

## Step 5: Discussion of Code (Python Preprocessing and Forecasting Methods)

The dataset used in this visualization was prepared and extended using a structured Python workflow prior to being imported into Tableau. The goal of this preprocessing was to (1) clean and standardize the historical democracy index data, (2) ensure complete country–year coverage from 2010 to 2024, and (3) generate stable, interpretable forecasts through 2030

### Historical data cleaning

Python was used to load, inspect, and standardize the raw EIU democracy index series. Key steps included:
- Reshaping data from wide format to a long format with one row per country–year.
- Coercing variable types to ensure that year was numeric and score was floating-point.
- Sorting and grouping by country to establish clean temporal order.
- Forward-filling missing values within each country to maintain continuity for time-series modeling.
- Verifying coverage by checking that each country had observations for all years from 2010 onward.
  
These operations produced a consistent, gap-free historical dataset suitable for forecasting.

### Time-series forecasting approach

To generate values for 2025–2030, the notebook applied a Prophet-based univariate forecasting model to each country’s historical time series. Prophet was selected because it:
- Handles short annual time series reliably.
- Automatically models trends and uncertainty.
- Produces smooth forecasts suitable for high-level visualization.

For each country:

1. The historical data (2010–2024) was converted into Prophet’s required structure with ds (date) and y (value).
2. A Prophet model was fitted to the historical values.
3. A six-year future dataframe (2025–2030) was generated.
4. Prophet produced point forecasts (yhat) and uncertainty intervals.
5. Only the point forecast was retained, then clipped to the theoretical democracy index range of 0–10.
   
This process ensured that every country had a complete, consistent time series covering 2010–2030.

### Merging Historical and Forecast Data

The historical values and forecasted values were concatenated into a single dataset, with an added field distinguishing:
- Historical observations (2010–2024)
- Forecasted observations (2025–2030)

This combined dataset allowed Tableau to apply separate encodings (e.g., solid vs. dotted lines, shading of the forecast period).

### Regime Classification and Final Export

An additional Python function classified each country-year into one of four regime types defined in the Economist Intelligence Unit’s Democracy Index reports:
- Full democracy
- Flawed democracy
- Hybrid regime
- Authoritarian regime
  
The final cleaned dataset included:
- country
- ds (year as datetime)
- value (democracy index)
- regime (categorical classification)
- source (historical or forecast)
  
It was exported as a CSV for direct use in Tableau.

---

## Step 6: Evaluation
The visualization was evaluated based on four effectiveness criteria:

| Metric | Description |
|---------|--------------|
| **Accuracy** | Faithful representation of democracy index data and trends. |
| **Discriminability** | Clear differentiation between high and low democracy levels. |
| **Separability** | Effective use of visual variables (color, position) without interference. |
| **Popout** | Strong perceptual contrast that draws attention to key differences. |

Overall, the visualization achieved its objective of enabling comparative and temporal analysis of democracy patterns in a clear and intuitive manner. This preprocessing and modeling pipeline ensured that the Tableau visualization was supported by a clean, well-structured, and analytically consistent dataset that accurately reflected both historical democracy patterns and projected future trajectories.

---


## Links
- **Interactive Tableau Visualization:** [View on Tableau Public](https://public.tableau.com/views/Project1_17446726355310/Sheet1)  
- **Hosted Version:** [GitHub Pages — Democracy Index Visualization](https://thooms-coder.github.io/Democracy_Index/)  

---

© 2025 Mutsa Mungoshi · IA 640 · Clarkson University

