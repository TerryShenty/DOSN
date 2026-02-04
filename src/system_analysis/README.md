# Decentralization and Core Instance Analysis in Mastodon

This analysis focuses on constructing a directed, weighted social network of Mastodon instances to identify core instances, analyze network characteristics, and evaluate the degree of decentralization.

## 1. Data Refinement & Network Construction

### Processing Steps
1.  **Remove Internal Interactions:** Deleted intra-instance interaction data. Excluded instances with no attributes and their associated interactions.
2.  **Construct Network:** Built a directed social network where every node has attributes and no self-loops.
3.  **Filter by Activity:** Further removed nodes with **< 20 active users** and their associated interactions.
    *   **Initial:** 8963 nodes, 99587 edges.
    *   **Refined:** 72 nodes, 1266 edges.

### Rationale for Filtering
*   **Representativeness & Stability:** Instances with very few active users yield sparse interaction data, making statistical results unstable and prone to accidental factors.
*   **Noise Reduction:** Small instances often exhibit extreme or anomalous behavior. Removing them prevents distortion of global inequality metrics (like the Gini coefficient).
*   **Focus on Structure:** The study aims to understand the "mainstream" or "core" structure. Focusing on larger nodes better reflects the interaction patterns and resource distribution among influential instances.

---

## 2. Basic Network Characteristics

**Network Summary:**
*   **Nodes:** 72
*   **Edges:** 1266

**Node Statistics:**
*   **Active Users:** Range: 20 - 7057 (Avg: 237.25)
*   **Total Users:** Range: 43 - 118,042 (Avg: 4519.67)

**Degree Statistics:**
*   **Average In/Out-degree:** 17.58
*   **Average Weighted In/Out-degree:** 5384.47

---

## 3. Identification of Core Instances

### Methodology
We established a baseline requirement of **≥20 active users** for core instances and used multiple metrics to classify them:

1.  **PageRank**
2.  **Betweenness Centrality**
3.  **Eigenvector Centrality**
4.  **Active Output & Passive Attraction Scores (Custom Metrics)**

#### Custom Metric Definitions

**Raw Measures:**
*   **Weighted Out-degree:** Sum of weights of all outgoing edges (Total external interactions initiated).
*   **Out-degree Diversity:** Number of unique target nodes (Unique instances interacted with).
*   **Weighted In-degree:** Sum of weights of all incoming edges (Total passive attraction).
*   **In-degree Diversity:** Number of unique nodes pointing to the instance (Unique instances attracting interaction).

**Per Capita Measures:**
*   All raw measures were divided by the number of active users to normalize for size.

**Composite Scores:**
*   **Active Output Score:** `weight_out * norm(per capita weighted out) + weight_diversity * norm(per capita out diversity)`
*   **Passive Attraction Score:** `weight_out * norm(per capita weighted in) + weight_diversity * norm(per capita in diversity)`
    *   *Note: Power functions were used in final calculation: Score = (Measure + ε)^0.6 × (Diversity + ε)^0.4*

### Analysis Findings

**1. Multi-Centric Features (Decentralization)**
*   The Top 10 instances across different metrics show almost **no overlap**.
*   This indicates there is no single dominant node; different "centers" exist for different reasons (behavioral vs. structural), supporting a decentralized structure resistant to single-point failure.

**2. Structural Hubs vs. Behavioral Leaders**
*   **Structural Metrics (PageRank/Eigenvector):** Uneven distribution suggests the existence of "authorities" or "hubs."
    *   *PageRank* reflects global authority.
    *   *Eigenvector Centrality* reflects the distinct logic of "transitive influence" (connecting to VIPs).
*   **Specific Nodes:** Instances like `mstdn.guru` (tech focus) and `social.mikutter.hachune.net` (interest community) score extremely high in structural metrics. They act as bridges or information hubs, even if they aren't the most actively interactive per capita.

![Core Instance Visualization](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/8e087e05-19b8-4d6d-a689-d83f8783f763)

---

## 4. RQ3: Decentralization & Multi-Dimensional Analysis

### Multi-Dimensional Metric System
*   **Interaction Dimension:** Active Output Score vs. Passive Input Score.
*   **Structural Dimension:** PageRank (global reach) and Betweenness (bridging role).
*   **Influence Dimension:** Eigenvector (recursive centrality) and Katz (attenuated long-range influence).

### Comparative Analysis
*   **Centralization Trend:** All metrics follow a power-law distribution. Importance is highly skewed, revealing inherent centralizing forces in the federated network.
*   **Hub-Spoke Asymmetry:** Passive interaction scores are significantly higher than active scores. Core instances aggregate attention, while non-core instances are active across boundaries.
*   **Distinct Influence Logic:** Influence metrics (Eigenvector, Katz) have low correlation with behavioral/structural metrics, indicating a unique mechanism of power propagation.

### Gini Coefficient & Core-Periphery Segmentation

We constructed sub-networks (Core vs. Non-Core) dynamically by varying the number of core instances (Top 3 to Top 30) for each metric and calculated Gini Coefficients.

**Key Insights:**
1.  **Optimal Decentralization Window:** Decentralization peaks when the core consists of the **Top 3-7 instances**. Beyond this range, centralization typically increases (Internal Matthew Effect).
2.  **Structural Rigidity:** The "Non-Core" network shows stable inequality coefficients across 5 of 6 metrics, suggesting the periphery structure is resistant to change.
3.  **PageRank Exception:** Only PageRank showed a significant drop in Gini coefficient within the non-core network (0.406 → 0.150), reflecting its sensitivity to hierarchy removal.

### Implications for Platform Governance
*   **Multi-Metric Monitoring:** Reliance on a single algorithm creates blind spots. Governance must monitor behavioral, structural, and influence metrics simultaneously.
*   **Respect Influence Metrics:** Eigenvector/Katz metrics reveal hidden power structures distinct from simple activity.
*   **Balance Core-Periphery:** While the periphery is stable, the core composition changes. Governance should aim to distribute resources to reinforce the core-periphery interaction loop.

---

## 5. Future Work & Roadmap

1.  **Refine Definitions:**
    *   Redefine active users statistically to remove bias from instance size.
    *   Adjust weighting/normalization in core metric calculations via PCA or correlation analysis.
2.  **Dynamic Analysis:**
    *   Identify core instances and track their variation over time using longitudinal data.
3.  **Decentralization Index:**
    *   Analyze the correlation between specific core instances and the overall network decentralization index.
4.  **Finalization:**
    *   Standardize data annotation rules.
    *   Generate comprehensive visualizations.
    *   Integrate findings into the final project report.

*Data Requirements Summary:*
*   Instance Interaction Matrix (Source -> Target -> Count)
*   Instance Metadata: ID, Total Users, Active Users, Total Interactions (Internal+External), External Interaction Ratio.
