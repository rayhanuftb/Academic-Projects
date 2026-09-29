# Educational Research and Data Analysis Practical Work

> Academic Project / Practical Work

## 📚 Course Information

- **Course Title:** Educational Research and Data Analysis Lab
- **Course Code:** EDU 4312
- **Student:** Rayhanul Islam
- **Institution:** University of Frontier Technology, Bangladesh

---

## 📌 Research Problem

**How do digital literacy, platform engagement, and study habits relate to academic performance (GPA) among university students?**

This study investigates the relationships between student engagement with online learning platforms, digital literacy, study habits, and academic outcomes using a synthetic educational survey dataset.

---

## 🎯 Research Objectives

1. To analyze the distribution of key educational variables (GPA, engagement, digital literacy).
2. To examine correlations between study habits, platform usage, and academic performance.
3. To compare academic performance across departments and demographic groups.
4. To identify factors significantly associated with student satisfaction.

---

## ❓ Research Questions

1. What is the distribution of GPA, engagement scores, and digital literacy among students?
2. Is there a significant correlation between study hours and GPA?
3. Do engagement scores differ significantly between male and female students?
4. Does GPA vary significantly across academic departments?
5. Is there a significant association between internet access level and department?

---

## 📐 Methodology

- **Research Design:** Quantitative, cross-sectional survey design
- **Data Collection:** Synthetic survey instrument (200 respondents, 14 variables)
- **Analysis Methods:**
  - Descriptive statistics (central tendency, dispersion, distribution shape)
  - Independent samples t-test
  - One-way ANOVA
  - Chi-square test of independence
  - Pearson correlation and simple linear regression
- **Tools:** Python 3.10+, pandas, scipy, matplotlib, seaborn

---

## ⚠️ Data Disclaimer

**All data used in this project is SYNTHETIC and generated for academic demonstration purposes only.** The dataset does not represent real student responses or actual research findings. This project is not intended for clinical, institutional, or policy decision-making.

---

## 🛠️ Technologies and Tools

- **Language:** Python 3.10+
- **Libraries:** NumPy, Pandas, SciPy, Matplotlib, Seaborn
- **Testing:** pytest

---

## 📁 Project Structure

```
Research and Data Analysis/
├── README.md
├── requirements.txt
├── data/
│   └── student_survey_data.csv      (generated)
├── src/
│   ├── generate_dataset.py          Synthetic data generation
│   ├── data_cleaning.py             Missing values, outliers, encoding
│   ├── descriptive_stats.py         Summary statistics module
│   ├── statistical_analysis.py      Hypothesis testing & regression
│   ├── visualizations.py            Plot generation module
│   └── main.py                      Full analysis pipeline
├── tests/
│   ├── test_descriptive_stats.py
│   ├── test_data_cleaning.py
│   ├── test_statistical_analysis.py
│   └── test_main.py
└── outputs/
    └── figures/                     Generated visualizations
```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Full Analysis

```bash
python src/main.py
```

This generates the synthetic dataset, performs data cleaning, computes descriptive and inferential statistics, and saves visualizations to `outputs/figures/`.

### 3. Run Tests

```bash
pytest tests/ -v
```

---

## 📊 Key Visualizations

- Distribution plots for GPA and engagement scores
- Correlation heatmap of numerical variables
- Scatter plots with regression trends
- Grouped box plots comparing departments
- Missing values pattern visualization

---

## 🎓 Academic Note

This work was completed as part of academic laboratory learning and is included in my academic portfolio to demonstrate practical skills in educational research methodology, data analysis, statistical inference, and data visualization.

---

## 👤 Author

**Rayhanul Islam**  
Educational Technology and Engineering  
University of Frontier Technology, Bangladesh
