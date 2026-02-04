# Mastodon Instance Interaction Analysis

This project investigates the dynamics of cross-instance interactions within the Mastodon network. We break the study down into two primary Research Questions (RQ):

*   **RQ1:** Analyze the relationship between Cross-Instance Interaction Rate (CIIR) and Instance Size.
*   **RQ2:** Analyze the drivers of cross-instance interaction, specifically focusing on Language and Topic through community detection and entropy analysis.

---

## 🏗️ Core Concepts & Data Preparation

### Detailed Definition: CIIR
**Cross-Instance Interaction Rate (CIIR)** is the primary metric for this study. For any given instance $i$:
$$ CIIR = \frac{\text{External Interactions}}{\text{Total Interactions (Internal + External)}} $$

![Formula Visualization](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/41afb825-d92c-4b27-b59c-88cf3a26b3ca)

### Data Merging
Data from various sources was consolidated into a single dataset for statistical analysis.

*   **Merged Data:** [merged_data.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/48ffaae5-e648-4b15-862e-065e7a432347)
*   **Merge Script:** [excelmerge.py](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/4d1b116c-e2f0-4991-a883-80bc3f636d1a)

---

## 📊 RQ1: Instance Size vs. CIIR

### 1. Exploratory Visualization & Correlation
We visualized the relationship using scatter plots with Loess smoothing and performed Pearson correlation tests.

![Scatter Plot](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/3696bc51-669e-43fb-a614-bd15983872c2)
*   **X-axis:** log(Instance Size)
*   **Y-axis:** CIIR
*   **Key Finding:** Pearson $r = 0.009$, indicating almost no linear correlation. The Loess curve (red line) suggests a slight downward trend as size increases, but large instances still maintain high cross-instance interaction.

**Code:** [ciirpicture.py](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/c13bddf2-e873-4dc9-9000-ae32f09ddc49)

### 2. Grouped Analysis (ANOVA & Tukey HSD)
To mitigate skewness from small instances, we categorized instance sizes into 5 levels (Level 1: Smallest, Level 5: Largest) and performed ANOVA analysis.

![Box Plot Analysis](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/d6e1562b-e191-4c90-b2a1-e539ff9dd5b2)

*   **Findings:** The data exhibits an "Inverted U-shape" or "Bridging" trend. Level 4 (medium-large instances) showed the highest average CIIR.
*   **Significance:** ANOVA ($F=6.88, p<0.001$) and Tukey HSD confirmed that Level 4 is significantly different (higher) than levels 1, 2, and 5.

**Code:** [ciiranalysis.py](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/68cc776c-7f44-4ebe-89bf-1350a12f8bc5)

### 3. Quantitative Modeling (Regression & GAM)
We verified the "Inverted U-shape" structure using Quadratic Regression, Generalized Additive Models (GAM), and Bootstrap validation.

![GAM and Quadratic Fit](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/4b2724f8-8817-4ea5-b4e6-3c73e52fc6ef)
![Bootstrap Intervals](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/0d769c86-26e0-4103-be69-8c70659c3ca6)

*   **Quadratic Regression:** The quadratic term ($\beta_2$) was $-0.0153$ ($p<0.001$), statistically confirming the inverted U-shape.
*   **Peak Point:** The model predicts the maximum CIIR at scale_level $\approx 2.71$.
*   **Robustness:** Bootstrap validation confirmed the confidence interval for the negative quadratic term does not cross zero.

**Code:** [Quantitative_analysis.py](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/e94653f5-2dc5-4deb-9afb-29556809b96d)

---

## 🌐 RQ2: Drivers of Interaction (Language & Topic)

We employed community detection algorithms to identify subgroups and analyzed the homogeneity of Language and Topics within these communities using entropy measures.

### 1. Data Processing
We consolidated community detection results with instance language and topic data.
*   **Processed Data:** [with_topics_languages_analysis.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/cf0a1040-fb6d-4f77-82ee-6e8a3827d222)
*   **Processing Script:** [with_topics_languages_analysis.py](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/97b4d116-0da1-409e-8d90-099d308d2ede)

### 2. Entropy and Diversity Analysis
We calculated the proportion of dominant languages/topics and their entropy values. Communities were classified into four types:
1.  **Topic-driven:** Language-concentrated / Topic-diverse.
2.  **Cross-lingual interest-driven:** Language-diverse / Topic-concentrated.
3.  **Dual-driven:** Both concentrated.
4.  **Weakly clustered:** Both diverse.

### 3. Results
![Language Diversity](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/797b5340-01d1-4975-995e-b29f25be7285)
![Topic Classification](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/f4574944-9d35-4244-91b5-d6bcef91f934)

*   **Language:** Highly homogenized interactions. The average main language proportion is **92%**. Most communities are strictly constrained by language.
*   **Topic:** Topic entropy is higher than language entropy. While language constrains local clusters, common themes (Cross-lingual interest-driven, 2.6%) facilitate connectivity across linguistic boundaries.

**Conclusion:** Language creates local centralization (clusters), while topics promote decentralized diffusion across valid clusters.

**Analysis Code:** [with_topics_languages_analysis_1.py](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/35e31aad-485a-4d47-ba49-ae7d8fd9fb96)
