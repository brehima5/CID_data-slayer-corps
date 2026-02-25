# Data Slayer Corps: Closing NYC’s College Readiness Gap

## Critical Research Question (CRQ)
> **To what extent do a high school’s Economic Need Index (ENI) and Percent of Students in Temporary Housing predict the Readiness-Gap (percentage difference between high school graduation & College and Career Readiness) for specific demographic subgroups, and which schools serve as "positive outliers" by defying these systemic predictors?**

## Key Actionable Recommendations
* **Recommendation 1 (Policy):** The NYC DOE should direct supplemental CCR funding to schools in the top ENI quartile (≥ 0.85), where a single standard-deviation increase in economic need is associated with a **−16.4 point drop** in college readiness. Priority should be given to schools with co-occurring housing instability (≥ 5 % temporary housing) such as (**schools example**), which compounds the poverty effect by an additional **−4.6 points**.
* **Recommendation 2 (Resource):** Invest in **attendance intervention programs** at high-need schools (>0.80). Attendance is the strongest *modifiable* predictor in the model — a 5-percentage-point improvement (~1 SD) is associated with **+4.7 points** higher CCR. Unlike ENI and housing status, attendance is partially within reach of school-level action (e.g., mentoring, early-warning systems, family outreach).
* **Recommendation 3 (Data/Tech):** Lower the DOE's **n < 15 suppression threshold** or adopt differential-privacy techniques for subgroup CCR reporting. Currently, 76 % of Asian and 80 % of White subgroup CCR data is suppressed, creating a systematic visibility gap that inflates apparent racial disparities and prevents equitable resource allocation. A city-level data-sharing agreement could enable privacy-preserving subgroup analysis without compromising individual student confidentiality.

## Methodology & Technical Specifications
<div align="center">

| | |
| :---: | :---: |
| **Civic Issue Focus** | **Target Stakeholder** |
| High School Education Disparities | NYC Department of Education |

</div>

<br>

### Data Sources

*InfoHub - 2024-25 School Quality Reports: Citywide Results for High Schools*

This project analyzes the 2024–2025 NYC School Quality Reports (SQR). These reports evaluate public schools using student performance data and feedback from the annual NYC School Survey. Performance is measured across four key areas: School Description, Instruction, Safety and Climate, and Family Relationships. For specific technical details on these metrics, refer to the DOE’s Educator Guide [here](https://infohub.nyced.org/docs/default-source/default-document-library/finalized-2024-25-educator-guide-hs-1.pdf).

<div align='center'>

<a href="https://infohub.nyced.org/reports/students-and-schools/school-quality/school-quality-reports-and-resources/school-quality-reports-citywide-results" target="_blank">
  <img src="https://img.shields.io/badge/Source-NYC_InfoHub-00355E?style=for-the-badge&logo=gitbook&logoColor=white" alt="NYC InfoHub Source"/>
</a>

</div>

<br>
<br>

*Department of Education (DOE) - School Point Locations*

This project also utilized School Zone Locations, which contained an ESRI shape file of all NYC public school locations. This was primarily used to connect polygonal coordinates to all public schools found in the SQR dataset, allowing for a geospatial analysis lens of the CRQ.

<div align='center'>
    
<a href="https://data.cityofnewyork.us/Education/School-Point-Locations/jfju-ynrr/about_data" target="_blank">
  <img src="https://img.shields.io/badge/Source-NYC_Open_Data-00355E?style=for-the-badge&logo=gitbook&logoColor=white" alt="NYC Open Data Source"/>
</a>

</div>

###  Tools Utilized

<div align="center">

**Languages & Frameworks**
<br>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white" alt="SQL"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit"/>

**Data Science & Geospatial Libraries**
<br>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
<img src="https://img.shields.io/badge/GeoPandas-139C5A?style=for-the-badge&logo=pandas&logoColor=white" alt="GeoPandas"/>
<img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Scikit-Learn"/>
<img src="https://img.shields.io/badge/Statsmodels-20A39E?style=for-the-badge" alt="Statsmodels"/>

**Databases & Visualization**
<br>
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
<img src="https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white" alt="Tableau"/>

</div>

## Key Findings
1.  **[Finding 1 - The primary answer to your CRQ, supported by data.]**
2.  **[Finding 2 - A key disparity or relationship identified in the data.]**
3.  **[Finding 3 - A model insight or statistical inference.]**

## Links to Final Deliverables
* **Interactive Tableau Dashboard:** [PASTE TABLEAU PUBLIC LINK HERE]
* **Local Streamlit Application:** Run instructions: `streamlit run deployment/app.py`
* **Technical Report (PDF):** [Link to `deliverables/Deliverable_Report.pdf`]

## Repository Navigation
* `sql/data_processing.sql`: **Star Schema** construction and ETL.
* `python/notebooks/eda.ipynb`: Visual EDA and statistical analysis.
* `python/src/model_training.py`: Final model code and evaluation.
* `ai_process.md`: Documentation on ethical AI usage.

## Data Source Attribution 

We acknowledge and appreciate the work of [Author/Organization Name] in making this data publicly available under the [License Type] license.

## Contributor and Roles 

* (Fellow name one: Role X)[Link to LinkedIn]
* (Fellow name two: Role Y)[Link to LinkedIn]
* (Fellow name three: Role Z)[Link to LinkedIn]

## Recommended Tree Structure (Revise for Final Project)
```pyton
CID-TeamName-ProjectName/
├── data/
│   ├── raw/
│   │   └── civic_data_source_1.csv
│   │   └── civic_data_source_2.csv
├── sql/
│   └── data_processing.sql
├── python/
│   ├── src/
│   │   └── create_schema.py
│   │   └── model_training.py
│   └── notebooks/
│       └── eda.ipynb
├── deployment/
│   └── app.py
├── deliverables/
│   ├── Stakeholder_Presentation.pptx
│   └── Deliverable_Report.pdf
├── .gitignore
├── ai_process.md
└── README.md
