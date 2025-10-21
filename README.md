# IA 640 Project 1 — Democracy Index Visualization  
**Author:** Mutsa Mungoshi  
**Course:** IA 640 – Data Visualization  
**Institution:** Clarkson University  

---

**Snapshot**
images/democracy_map.png

---
## Project Overview
This project develops an interactive Tableau Public visualization examining global democracy patterns from 2006 to 2024.  
The analysis follows the IA 640 analytical framework and applies principles of data abstraction, encoding, and visual design to effectively communicate complex temporal and spatial information.

**Live Visualization:**  
[View on GitHub Pages](https://thooms-coder.github.io/Democracy_Index/)

---

## Step 1: Dataset Selection
The dataset was obtained from the **Economist Intelligence Unit (EIU)**, an authoritative source in global business intelligence and political analysis.  
Selection was guided by four criteria:

- **Diversity:** The dataset incorporates multiple data types and variables from different sources.  
- **Quantity:** It includes a sufficiently large temporal span (2006–2024) for longitudinal analysis.  
- **Quality:** Data is complete, consistent, and standardized across years and countries.  
- **Novelty:** The dataset provides opportunities for examining underexplored global democratic trends.

The dataset reports **Democracy Index scores** for multiple countries, based on 60 indicators grouped into five dimensions:
1. Electoral process and pluralism  
2. Functioning of government  
3. Political participation  
4. Political culture  
5. Civil liberties  

---

## Step 2: Abstraction and Analysis
**Main Objective:** Compare and analyze democracy patterns for individual countries over time.

### Key Variables
| Variable | Type | Description |
|-----------|------|-------------|
| Country | Categorical (Spatial) | Used for faceting and spatial encoding in map visualizations. |
| Year | Interval | Represents the temporal axis and supports time-series analysis. |
| Democracy Index | Quantitative | Encoded with color and position; discretized into 10 bins to enhance clarity. |

### Key Relationships
- **Time-Series:** Tracking changes in democracy within each country.  
- **Nominal Comparison:** Comparing democracy levels across countries in a given year.

A **choropleth map** was selected as the primary idiom for visualizing spatial variation.  
A **dual-color scheme** (blue representing more democratic countries and orange representing less democratic countries) was used for contrast and interpretability. Darker shades indicate stronger expressions of each type.

---

## Step 3: Line Graph Justification
Line graphs were used to represent temporal changes in democracy index values for each country.  
Because "Year" is an interval variable, lines are an effective means of showing temporal progression.

**Design considerations:**
- Auto-scaling of y-axes for efficient spatial use.  
- Consistent color encoding across visualizations.  
- Hover tooltips providing exact democracy index values.  
- Clearly labeled axes to preserve interpretability.

---

## Step 4: Enhancing Context and Interactivity
To increase the analytical depth and usability of the visualization:
- Descriptive annotations were added to clarify observed trends.  
- Interactive filters for **Country** and **Year** enable user-driven exploration.  
- A **Year slider** allows users to animate and observe temporal transitions.  
- Country codes were added as redundant encodings for improved clarity.  
- Hovering over a country triggers a line graph showing its democracy trend over time.

---

## Step 5: Reflection and Evaluation
The visualization was evaluated based on four effectiveness criteria:

| Metric | Description |
|---------|--------------|
| **Accuracy** | Faithful representation of democracy index data and trends. |
| **Discriminability** | Clear differentiation between high and low democracy levels. |
| **Separability** | Effective use of visual variables (color, position) without interference. |
| **Popout** | Strong perceptual contrast that draws attention to key differences. |

Overall, the visualization achieved its objective of enabling comparative and temporal analysis of democracy patterns in a clear and intuitive manner.

---

## Links
- **Interactive Tableau Visualization:** [View on Tableau Public](https://public.tableau.com/views/Project1_17446726355310/Sheet1)  
- **Hosted Version:** [GitHub Pages — Democracy Index Visualization](https://thooms-coder.github.io/Democracy_Index/)  

---

© 2025 Mutsa Mungoshi · IA 640 · Clarkson University

