# Instance Interaction Network Analysis

This project performs a comprehensive analysis of user interactions across different instances (based on the `boostersfavourites` dataset). The goal is to construct an interaction network, analyze cross-instance vs. intra-instance behaviors, categorize instances based on themes and languages, and detect community structures using graph algorithms.

## Project Roadmap

The analysis is divided into several stages, ranging from data preparation to advanced community detection.

### 1. Planning & Data Preparation

**Objective**
Based on the existing dataset, identify active participants and interaction targets to construct a foundational instance list.

**Data Processing**
*   Analyzed the `sid` (interaction initiator) and `id` (interaction target) from the dataset to determine their respective instances.
*   Generated two primary lists:
    1.  **Passive Interaction Statistics (`sum_based_stats`):** Counts unique instances referenced by users. For example, if User A favorites users from Instance X, Y, and Z, and User B favorites users from Instance Y and Z, the stats calculate unique references per user.
        *   [sum_based_stats.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/aacaff9f-b8d2-4bd5-9abf-f8ee71aed175)
    2.  **Active User Statistics (`sum_based_user`):** Counts initiating users grouped by their home instance (e.g., User A belongs to X, User B belongs to Y).
        *   [sum_based_user.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/ffe5a307-a02e-4472-ae00-87d595753f4e)

**Code**
*   [abstruct.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/055b5df7-2f9b-4e31-b0ac-614ba14b56b2) - Extracts instance names and counts from specific JSON files.
*   [sum.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/209554a5-66d6-40c4-9391-155b9b93a790) - Merges identical instances and aggregates counts.

---

### 2. Interaction Metrics Analysis

**Objective**
Analyze the ratio of intra-instance interactions (within the same server) versus cross-instance interactions.

**Analysis**
*   Calculated total interactions, internal interactions, cross-instance interactions, and the cross-instance ratio for all instances.
*   **Visualization:**
    *   Ratio of cross-instance (blue) vs. internal (orange) interactions.
    *   Top 20 instances by cross-instance interaction ratio.
    *   Top 30 instances by total interaction volume.
    *   Comparison of cross-instance (pink) vs. internal (blue) volume for the Top 15 instances.

![final_interaction_analysis_comprehensive.png](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/d73bce70-c35c-4a05-acda-23b2391980ac)

**Code & Data**
*   [sum_interaction.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/d980ae79-e8cc-4983-b775-1337503c9373) - Performs the calculation and generates visualizations.
*   [sum_interaction.ipynb (Dataset)](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/7ece3c9b-d6c4-4b55-be59-eb589aa6855d)

---

### 3. Instance Profiling & Scaling

**Objective**
Classify and sort instances based on user population and activity levels.

**Data Processing**
Sorted instances by **Total Users** and **Active Users** to generate a comprehensive report on instance scale.

*   [Instances_Sorted_By_Total_Users.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/f8c75d9e-6dc7-437b-a2ef-c1fbead221bf)
*   [Instances_Sorted_By_Active_Users.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/cda220a9-e5e3-4876-90c3-4aa44131af68)
*   [Instance_User_Scale_Comprehensive_Report.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/ab52b49d-bd37-4d39-83af-aa20fc24eb6d) (Scale and activity analysis)

**Code**
*   [deal_instances.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/abeb5bdd-3853-4cb3-845d-af54206561d8)

---

### 4. Network Node Classification

**Objective**
Analyze the role of each instance within the interaction network and classify nodes.

**Data Processing**
Instances were sorted based on cross-instance/internal interaction counts and ratios. Nodes were then classified into four categories:

1.  **Source Nodes:** High active interaction (initiators).
    *   [Source_Nodes_Sorted_By_Active_Interaction.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/89167527-b1c5-4686-b5ac-6f0cdf7ee54a)
    *   [TOP20_Source_Nodes.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/d813e0bd-434c-4256-bb65-38833612193a)
2.  **Sink Nodes:** High passive interaction (targets).
    *   [Sink_Nodes_Sorted_By_Passive_Interaction.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/ff2bef24-c2af-4638-8428-a44ec1228239)
    *   [TOP20_Sink_Nodes.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/73c4d1f0-faa6-4f17-a6a1-eed2944842b1)
3.  **Isolated Nodes:** No cross-instance interaction.
    *   [Isolated_Nodes.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/69c3f117-d847-41e6-b241-ac3158b7ce2b)
4.  **Bidirectional Nodes:** Both active and passive interactions.
    *   [Bidirectional_Nodes.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/166b9904-b26f-4a80-a8cf-ad32f11489ae)

*   **Summary:** [Node_Type_Statistics_Summary.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/59a1120d-e695-4d4e-bc52-42f97a208c93)

**Additional Sorted Data**
*   [Sorted_By_Cross_Instance_Total.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/7dd72df6-5a8a-4f7a-952c-3fc5b5a9f060)
*   [Sorted_By_Internal_Total.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/4b7322c6-0555-48d8-8d16-fb32f3b983cd)
*   [Cross_Instance_Ratio_Analysis.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/17ff609e-80c6-4056-9a0d-2f711dd3816a)

**Code**
*   [deal_Interactions.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/1977cd06-fd56-43be-816c-cff51e331d6c)
*   [deal_interaction_acrossinstances_rate.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/f19562b5-cbd2-4464-b0e3-cab2214ca051)

---

### 5. Semantic Theme Analysis (NLP)

**Objective**
Understand the content focus of different instances using Natural Language Processing.

**Analysis**
Utilized NLP models to analyze instance descriptions, generating "Cleaned Tags" and determining specific theme names for classification.

![Theme Analysis Visualization](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/2fba0e0e-40c2-4943-ba97-ccea1a390a62)

**Data**
*   [Multi_language_Theme_Analysis_Report.xlsx](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/2ba50e9f-8664-4be1-b7a6-f92a32eea495) (Complete Report)
*   [Most_Common_Theme_Tags.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/b63be33f-fd95-4da3-b91f-65e396cb9a33)
*   [Theme_Analysis_Summary.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/005f2c4e-85f2-42da-81a6-aba87545e50f)
*   [Topic_Clustering_Statistics.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/ea98ed4e-9fb9-41ea-bb14-fe76a633d2ba)

**Code**
*   [deal_theme.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/99d389f1-343b-45ce-a505-cbd36c7d4412)

---

### 6. Language Detection and Classification

**Objective**
Identify the primary language used in each instance.

**Data Processing**
Scraped language data from `instance.social`. For instances with missing data, languages were detected based on the instance description.

*   [instances_with_detected_language.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/f911b5f8-5e4a-4889-bc03-39571a1ee769)
*   [instances_language_classified.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/6bfa3db8-e037-45b8-b899-b2127fc93ef9)

**Code**
*   [instance_language_detected.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/43edc65d-599f-4974-a92b-6955e7d08276) (Scraping & detection)
*   [language_classfied.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/57ec07e7-e26c-443d-b8c5-80d26c0de5f2) (Classification)

---

### 7. Community Detection

**Objective**
Discover modular structures within the user graph.

**Analysis**
Applied **Louvain** and **Label Propagation** algorithms to detect communities. The Louvain algorithm yielded higher modularity, indicating a clearer community structure.

*   [community_detailed_analysis.csv](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/36182c55-da9b-4d60-a1f0-9f7bceae240e)

**Code**
*   [community_detect.ipynb](https://resv2.craft.do/user/full/8ea413f8-e492-ed3b-2585-e9611ddb63fc/doc/61a8fb48-5717-4293-9275-861cdfaa3e26/e0aecc7b-9a1c-400a-a336-d84114aa3d25)
