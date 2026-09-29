"""
Main analysis script for Educational Research and Data Analysis Practical Work.

This script demonstrates the complete research analysis pipeline:
1. Data generation (synthetic)
2. Data cleaning
3. Descriptive statistics
4. Statistical analysis
5. Visualizations

IMPORTANT: All data used in this project is SYNTHETIC and generated for
academic demonstration purposes only.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate_dataset import generate_student_survey_data, save_dataset
from data_cleaning import DataCleaner
from descriptive_stats import DescriptiveStatistics
from statistical_analysis import StatisticalAnalysis
from visualizations import ResearchVisualizer


def run_analysis():
    """Execute the full analysis pipeline."""
    print("=" * 70)
    print("EDUCATIONAL RESEARCH AND DATA ANALYSIS")
    print("Synthetic Dataset Analysis - Academic Demonstration")
    print("=" * 70)

    print("\n[1] Generating synthetic dataset...")
    df = generate_student_survey_data(n_students=200)
    data_path = save_dataset(df, output_dir="data")
    print(f"    Dataset saved to: {data_path}")
    print(f"    Shape: {df.shape}")

    print("\n[2] Data Cleaning...")
    cleaner = DataCleaner()
    data_info = cleaner.info(df)
    print(f"    Missing values before cleaning:")
    for col, count in data_info["missing_values"].items():
        if count > 0:
            print(f"      - {col}: {count} ({data_info['missing_percent'][col]}%)")

    df_clean = cleaner.handle_missing_values(
        df, numerical_strategy="median", categorical_strategy="mode"
    )
    print(f"    Missing values after cleaning: {df_clean.isnull().sum().sum()}")

    print("\n[3] Descriptive Statistics...")
    desc = DescriptiveStatistics()

    numerical_cols = [
        "age", "digital_literacy_score", "engagement_score",
        "study_hours_weekly", "gpa", "satisfaction_score",
        "hours_on_platform_daily", "quiz_completion_rate",
    ]
    categorical_cols = ["gender", "department", "internet_access"]

    report = desc.full_report(df_clean, numerical_cols, categorical_cols)

    print("\n    Numerical Variables Summary:")
    print("    " + "-" * 60)
    for var, stats in report["numerical"].items():
        print(f"    {var}: mean={stats['mean']}, std={stats['std_dev']}, "
              f"range=[{stats['min']}, {stats['max']}]")

    print("\n    Categorical Variables Summary:")
    print("    " + "-" * 60)
    for var, info in report["categorical"].items():
        print(f"    {var}: {info['unique_count']} categories, mode='{info['mode']}'")

    print("\n[4] Statistical Analysis...")
    sa = StatisticalAnalysis()

    print("\n    a) Correlation Analysis (key variables):")
    corr_cols = ["engagement_score", "gpa", "study_hours_weekly", "quiz_completion_rate"]
    corr_matrix = sa.correlation_matrix(df_clean, corr_cols)
    print(f"    Correlation matrix computed for {len(corr_cols)} variables.")

    print("\n    b) T-Test: Engagement by Gender (Male vs Female):")
    t_result = sa.t_test_two_groups(
        df_clean, "engagement_score", "gender", "Male", "Female"
    )
    print(f"       t={t_result['t_statistic']}, p={t_result['p_value']}, "
          f"significant={t_result['significant_at_005']}")
    print(f"       Cohen's d={t_result['cohens_d']}")

    print("\n    c) ANOVA: GPA across Departments:")
    anova_result = sa.anova_one_way(df_clean, "gpa", "department")
    print(f"       F={anova_result['f_statistic']}, p={anova_result['p_value']}, "
          f"eta²={anova_result['eta_squared']}")

    print("\n    d) Chi-Square: Internet Access vs Department:")
    chi_result = sa.chi_square_test(df_clean, "internet_access", "department")
    print(f"       χ²={chi_result['chi2_statistic']}, p={chi_result['p_value']}, "
          f"Cramér's V={chi_result['cramers_v']}")

    print("\n    e) Linear Regression: Engagement vs GPA:")
    reg_result = sa.simple_linear_regression(df_clean, "engagement_score", "gpa")
    print(f"       slope={reg_result['slope']}, R²={reg_result['r_squared']}, "
          f"p={reg_result['p_value']}")

    print("\n    f) Pearson Correlation: Study Hours vs GPA:")
    pcorr = sa.pearson_correlation(df_clean, "study_hours_weekly", "gpa")
    print(f"       r={pcorr['pearson_r']}, R²={pcorr['r_squared']}, "
          f"p={pcorr['p_value']}")

    print("\n[5] Generating Visualizations...")
    viz = ResearchVisualizer(output_dir="outputs/figures")

    fig1 = viz.plot_distribution(df_clean, "gpa", "GPA Distribution")
    print(f"    Saved: {fig1}")

    fig2 = viz.plot_distribution(df_clean, "engagement_score", "Engagement Score Distribution")
    print(f"    Saved: {fig2}")

    fig3 = viz.plot_categorical_counts(df_clean, "department", "Students by Department")
    print(f"    Saved: {fig3}")

    fig4 = viz.plot_correlation_heatmap(df_clean, corr_cols, "Correlation Heatmap")
    print(f"    Saved: {fig4}")

    fig5 = viz.plot_scatter(df_clean, "engagement_score", "gpa", "department", "GPA vs Engagement")
    print(f"    Saved: {fig5}")

    fig6 = viz.plot_group_comparison(df_clean, "gpa", "department", "GPA by Department")
    print(f"    Saved: {fig6}")

    fig7 = viz.plot_missing_values(df, "Missing Values Pattern (Raw Data)")
    print(f"    Saved: {fig7}")

    fig8 = viz.plot_bar_comparison(df_clean, "internet_access", "engagement_score", "Engagement by Internet Access")
    print(f"    Saved: {fig8}")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print("\nAll outputs saved to the 'data/' and 'outputs/' directories.")
    print("This is an academic demonstration using SYNTHETIC data.")


if __name__ == "__main__":
    run_analysis()
