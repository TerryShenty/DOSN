# Three-Layer Structural Dynamic Governance Framework for Mastodon's Decentralization

**An Empirical Study Based on Cross-Instance Interactions**

## 📖 Overview

This project investigates the decentralized governance mechanism of Decentralized Online Social Networks (DOSNs) through a **three-layer structural dynamic governance framework**, using Mastodon as the benchmark platform. 

By analyzing **~1.36 million cross-instance interaction records over 13 days**, we reveal user behavior patterns, semantic community formation, and the optimal network structure for maintaining decentralization. The research provides data-driven insights and actionable tools for DOSN service management and governance.

## 🧐 Background & Motivation

**Decentralized Online Social Networks (DOSNs)** such as Mastodon, Bluesky, and Pleroma have emerged as alternatives to centralized platforms. For DOSNs, ecological health relies on two core pillars:
1. The **frequency and quality** of cross-instance interactions.
2. The **decentralized balance** of the overall network.

Despite the growing popularity of DOSNs, **three key research gaps** hinder effective governance:
*   The quantitative impact of instance size on **Cross-Instance Interaction Ratio (CIIR)** remains unclear.
*   The joint driving mechanism of **language and topics** in shaping cross-instance semantic communities lacks systematic analysis.
*   A **multi-dimensional evaluation system** for measuring decentralization is absent.

This project aims to fill these gaps through empirical analysis and framework construction.

## ❓ Research Questions (RQs)

We focus on three interrelated research questions across three layers:

### 1. Behavioral Motivation Layer
> **RQ1:** How does instance size affect cross-instance interaction behavior (measured by CIIR)?

### 2. Semantic Structure Layer
> **RQ2:** How do languages and topics jointly shape the semantic community structure of DOSNs?

### 3. System Architecture Layer
> **RQ3:** What is the optimal core instance scale window for maintaining a stable decentralized network structure?

## 📊 Data & Methodology

### Data Source
The dataset is derived from the **FediLive project**, publicly available on [Zenodo](https://zenodo.org/records/14869106). It includes:
*   1,361,708 posts (`livefeeds.json`)
*   Boost/favourite interaction data (`boostersfavourites.json`)
*   Reply interaction data (`reply.json`)

### Data Preprocessing
To ensure data quality, we performed three key steps:
1.  **Format Standardization:** Unify IDs and timestamps.
2.  **Outlier & Noise Handling:** Filter non-influential instances (Core instances: ≥20 active users).
3.  **Duplicate Removal:** Generate unique `event_id`.

### Core Datasets Generated
| Dataset Name | Purpose |
| :--- | :--- |
| `interaction_table.csv` | Records all cross/intra-instance interactions (type, timestamp, parties) |
| `instance_attributes.csv` | Instance-level metrics (user counts, active users, top 5 topics) |
| `interaction_matrix.csv` | Interaction counts (reply/favourite/reblog) between instance pairs |
| `instance_interaction_stat.csv` | Detailed intra/cross-instance interaction statistics for each instance |

## 🛠 Methodology & Analytical Pipeline (Enhanced)

To investigate the three-layer governance framework, we employed a pipeline integrating statistical modeling, network science, and Natural Language Processing (NLP):

### 1. Behavioral Layer Analysis (RQ1)
*   **Metric Construction:** We defined the Cross-Instance Interaction Rate (CIIR) as:
  
$$
\text{CIIR} = \frac{\text{Interaction}_{\text{external}}}{\text{Interaction}_{\text{total}}}
$$

*   **Statistical Modeling:** Used Ordinary Least Squares (OLS) Regression with quadratic terms and Generalized Additive Models (GAM) to capture non-linear relationships between instance size (log-transformed) and CIIR.
*   **Grouping & ANOVA:** Categorized instances into **Small**, **Medium**, and **Large** based on active users to test for significant differences in interaction openness.

### 2. Semantic Structure Layer (RQ2)
*   **Community Detection:** Applied the **Louvain Algorithm** to the instance interaction network to identify structural clusters.
*   **Homogeneity Measurement:**
    *   Utilized **Information Entropy** to measure the concentration of languages and topics within each community.
    *   Calculated **Jaccard Similarity** to assess the overlap of interests between different linguistic groups.
*   **NLP Processing:** Employed **TF-IDF** for keyword extraction from instance descriptions to define "Topic Profiles."

### 3. System Architecture Layer (RQ3)
*   **Multidimensional Centrality:** Instead of simple degree centrality, we developed a composite index:
    *   **Output/Input Scores:** Weighted out-degree/in-degree multiplied by the diversity of interaction partners.
    *   **Katz Centrality:** Measuring the long-range influence of an instance across the entire federation.
    *   **Betweenness Centrality:** Identifying "bridge" instances that control information flow.
*   **Concentration Analysis:** Used the **Gini Coefficient** to quantify the inequality of influence distribution.
*   **Sensitivity Scanning:** Conducted a **K-point scan** ($k=3$ to $30$) to observe how the Gini coefficient of core vs. peripheral networks fluctuates as the number of "core instances" increases.

---

## 💡 Detailed Key Findings

### 1. The "Inverted U-Shaped" Behavioral Law
> We found that **"Bigger is not always more open."**

*   **Small Instances:** Often remain isolated due to low activity.
*   **Medium Instances** (Peak at ~20-50 active users): Exhibit the highest CIIR, serving as the "**active ambassadors**" of the federation.
*   **Large Instances:** Show a "**Centripetal Effect**," where users tend to interact internally, creating a risk of "de facto centralization."

### 2. Dual-Track Semantic Structure: "Language as Border, Topic as Bridge"
*   **Linguistic Segregation:** Language is the strongest predictor of community boundaries. Users naturally cluster with others speaking the same language, forming stable "**cultural silos**."
*   **Inter-community Connectivity:** Interestingly, while languages divide, specific **topics** (e.g., Technology, Art, Gaming) act as bridges. A community might be linguistically homogeneous but topically diverse, allowing information to jump across language barriers through shared interests.

### 3. The "3–7 Core" Steady-State Window
Our structural analysis revealed a critical threshold for decentralized health:

*   **Optimal Stability:** When the top **3 to 7 instances** share the core influence, the network maintains a healthy balance between efficiency and decentralization.
*   **Centralization Reversion:** Once the core expands beyond 7 instances or shrinks below 3, the Gini coefficient of the core network rises sharply, indicating that a few "**super-nodes**" are beginning to dominate the system, threatening the federated nature of the platform.

## 🚀 Contributions

### Theoretical
*   Proposed a **three-layer structural dynamic governance framework** (behavior-semantic-system).
*   Revealed the "inverted U-shaped CIIR" and "language-topic dual-track" mechanisms.

### Empirical
*   Provided quantitative evidence from ~1.36 million real interactions.
*   Validated the **3–7 core instance steady-state window**.

### Practical
*   Offered actionable governance tools (CIIR, Gini coefficient) for DOSN operators.
*   Proposed targeted strategies to mitigate centralization risks.

## 🛠️ Usage

1.  **Dataset Access**  
    Download the original dataset from [Zenodo](https://zenodo.org/records/14869106) and use the preprocessing scripts in `/data_cleaning` to generate standardized datasets.

2.  **Analysis Reproduction**  
    Run the analysis notebooks in `/notebooks` for RQ1-RQ3, including regression models, community detection, and centrality calculations.

3.  **Governance Tools**  
    Use the `governance_metrics/` scripts to compute CIIR, Gini coefficients, and core scale sensitivity for custom DOSN data.

## ⚠️ Limitations & Future Work

**Limitations:**
*   13-day data window usually limits long-term evolution analysis.
*   Semantic labels rely on instance descriptions.
*   Lack of intervention experiments.

**Future Work:**
*   Extend dataset to 6–12 months.
*   Integrate user-level behavioral data.
*   Conduct intervention experiments.
*   Extend framework to Bluesky and Pleroma.


