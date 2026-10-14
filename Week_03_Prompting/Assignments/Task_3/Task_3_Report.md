# Task 3 Report: Multiset Fractional Retrieval Metric (MFRM)

## 1. Executive Summary

In Text-to-SQL tasks, evaluation systems predominantly rely on **binary execution accuracy** (`0` or `1`), which tests whether the multiset of retrieved database tuples matches the ground-truth result with complete identity. While useful as a strict regression gate, this binary approach creates an extreme **"cliff effect"**: a query that retrieves 62 out of 63 correct records receives a score of `0.0`, identical to a query that crashes with a syntax error or returns irrelevant garbage.

To address this diagnostic limitation, this report proposes, defends, and implements the **Multiset Fractional Retrieval Metric (MFRM)**, encompassing:
1. **Multiset Jaccard Similarity ($J$)**
2. **Multiset Precision ($P$), Recall ($R$), and $F_1$-Score**

Applying this metric to the predictions obtained in **Task 2** yields a profound insight: while **Few-Shot Learning** appeared ~3.87% worse than **CO-STAR** and **ICIO** under binary accuracy (95.48% vs 99.35%), under MFRM it achieves **100.00% Mean Recall** and a **99.44% Mean $F_1$-Score** (a negligible 0.20% delta). MFRM reveals that Few-Shot never missed any relevant entities; its slight penalty arose exclusively from retrieving occasional duplicate branch locations.

---

## 2. Mathematical Formulation of the Metric

Relational databases operate under **bag semantics** (multisets), where identical tuples can appear multiple times. Let $P$ denote the multiset of rows returned by the predicted SQL query, and $E$ denote the multiset of rows returned by the expected ground truth query.

For each distinct tuple $x \in P \cup E$, let $\text{count}_P(x)$ and $\text{count}_E(x)$ represent its multiplicity in $P$ and $E$, respectively.

### 2.1. Multiset Intersection and Union
$$\text{Intersection: } |P \cap E| = \sum_{x \in P \cup E} \min\big(\text{count}_P(x), \text{count}_E(x)\big)$$
$$\text{Union: } |P \cup E| = \sum_{x \in P \cup E} \max\big(\text{count}_P(x), \text{count}_E(x)\big)$$

### 2.2. Metric Definitions
1. **Multiset Jaccard Similarity ($J$):**
   $$J(P, E) = \frac{|P \cap E|}{|P \cup E|}$$
2. **Multiset Precision ($P$):**
   $$\text{Precision} = \frac{|P \cap E|}{|P|}$$
3. **Multiset Recall ($R$):**
   $$\text{Recall} = \frac{|P \cap E|}{|E|}$$
4. **Multiset $F_1$-Score ($F_1$):**
   $$F_1 = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

### 2.3. Boundary & Edge Case Handling
- If both sets are empty ($P = \emptyset$ and $E = \emptyset$), the query correctly anticipated that no records match the criteria:
  $$J = 1.0, \quad P = 1.0, \quad R = 1.0, \quad F_1 = 1.0$$
- If one set is empty while the other contains rows ($P = \emptyset \oplus E = \emptyset$):
  $$J = 0.0, \quad P = 0.0, \quad R = 0.0, \quad F_1 = 0.0$$
- If a query raises a database execution/syntax error, $P$ is treated as an empty set ($\emptyset$).

---

## 3. Defense and Justification: Why MFRM is Applicable and Necessary

### 3.1. Eliminating the "Cliff Effect"
Under binary accuracy, partial correctness is completely ignored. In database applications (such as recommendation systems, analytical dashboards, or enterprise search), a user asking for *"restaurants in Alameda above 2.0 rating"* who receives 62 correct restaurants plus 1 duplicate branch suffers negligible informational harm. Under binary accuracy, this is penalized with `0.0`. MFRM awards this prediction a Jaccard score of:
$$J = \frac{62}{63} \approx 0.9841 \quad (98.4\%)$$
reflecting high real-world utility.

### 3.2. Diagnostic Decomposition: Precision vs. Recall
Binary accuracy cannot explain **why** a query failed. By decomposing multiset overlap into Precision and Recall:
- A query with **Recall = 1.0** and **Precision < 1.0** over-selects (e.g., missed a restrictive filter or duplicated joins).
- A query with **Recall < 1.0** and **Precision = 1.0** under-selects (e.g., used overly restrictive conditions).
This diagnostic power is essential for prompt engineers to refine prompt instructions.

### 3.3. Originality and Inherent Database Realism
Unlike token-based similarity metrics (such as BLEU or ROUGE, which compare SQL text strings and fail to capture equivalent queries like `WHERE A AND B` vs `WHERE B AND A`), MFRM evaluates the **semantic execution result** grounded directly in relational multiset theory.

---

## 4. Does MFRM Complement or Replace the Original Metric?

**MFRM complements the original metric rather than replacing it outright.**

A comprehensive software engineering evaluation requires a **two-tier metric framework**:

| Tier | Metric | Target Role | Key Strength |
|---|---|---|---|
| **Tier 1 (Strict)** | **Binary Multiset Accuracy** | Regression testing & Formal verification | Ensures zero defect tolerance for mission-critical queries (e.g., financial transactions, access control). |
| **Tier 2 (Continuous)** | **Multiset Fractional Retrieval (MFRM)** | Quality of Service (QoS) & Usability testing | Measures informational utility, user satisfaction, and resilience against edge-case anomalies. |

Replacing binary accuracy entirely would remove the incentive for models to achieve exact schema perfection. Using MFRM alongside binary accuracy provides both a ceiling standard (perfection) and a diagnostic continuum (practical utility).

---

## 5. Empirical Evaluation on Task 2 Predictions

Using the implementation in `evaluate_multiset_metric.py`, we calculated the metrics across all 155 benchmark questions for the three prompting frameworks evaluated in Task 2:

### 5.1. Comparative Metric Table

| Framework | Binary Accuracy | Mean Jaccard ($\mu \pm \sigma$) | Mean Precision | Mean Recall | Mean $F_1$-Score ($\mu \pm \sigma$) |
|---|:---:|:---:|:---:|:---:|:---:|
| **CO-STAR** | 99.35% | **0.9954 $\pm$ 0.0576** (99.54%) | **0.9954** | **1.0000** | **0.9964 $\pm$ 0.0449** (99.64%) |
| **ICIO** | 99.35% | **0.9954 $\pm$ 0.0576** (99.54%) | **0.9954** | **1.0000** | **0.9964 $\pm$ 0.0449** (99.64%) |
| **Few-Shot** | 95.48% | **0.9919 $\pm$ 0.0639** (99.19%) | **0.9919** | **1.0000** | **0.9944 $\pm$ 0.0478** (99.44%) |

### 5.2. Partial Credit Distribution Histogram

To further illustrate the diagnostic power of MFRM, the 155 queries for each framework were partitioned into Jaccard score intervals:

| Jaccard Score Range | CO-STAR | ICIO | Few-Shot Learning | Interpretation |
|---|:---:|:---:|:---:|---|
| **$J = 1.0$ (Exact Match)** | 154 | 154 | 148 | 100% perfect result |
| **$0.9 \le J < 1.0$ (Near Perfect)** | 0 | 0 | **5** | Minor cardinality difference (e.g. 62/63 rows) |
| **$0.5 \le J < 0.9$ (Substantial Overlap)**| 0 | 0 | **1** | Good overlap, minor filter drift |
| **$0.0 < J < 0.5$ (Low Overlap)** | 1 | 1 | 1 | Adversarial query (Line 67) |
| **$J = 0.0$ (Complete Failure / Error)**| 0 | 0 | **0** | Zero crashes or completely wrong queries |

```text
========================================================================================
                      PARTIAL CREDIT SCORE DISTRIBUTION (155 queries)
========================================================================================
Score Range       | CO-STAR              | ICIO                 | Few-Shot
----------------------------------------------------------------------------------------
J = 1.00 (Exact)  | [154] ██████████████ | [154] ██████████████ | [148] █████████████
0.90 <= J < 1.00  | [  0]                | [  0]                | [  5] ▌
0.50 <= J < 0.90  | [  0]                | [  0]                | [  1] ▏
0.00 <  J < 0.50  | [  1] ▏ (Line 67)    | [  1] ▏ (Line 67)    | [  1] ▏ (Line 67)
J = 0.00 (Fail)   | [  0]                | [  0]                | [  0]
========================================================================================
```

### 5.3. Analysis of Empirical Findings
1. **The Few-Shot Redemption**:
   Under the original metric, Few-Shot seemed notably inferior (148 vs 154). Under MFRM, 5 of the 7 "failures" achieved $J \ge 0.90$, and 1 achieved $J = 0.88$. Few-Shot achieved an extraordinary **Mean Recall of 1.0000** and **Mean $F_1$ of 99.44%**, confirming that it possesses virtually identical information retrieval power to CO-STAR and ICIO.
2. **Zero Hard Failures Across All Frameworks**:
   Not a single prompt technique produced a query with $J = 0.00$ or an unhandled SQL syntax error. The only query in the entire dataset with $J < 0.50$ was the deliberate adversarial distractor on Line 67 (*"What is the lifes greates illusion?"*), which affected all three models equally.

---

## 6. Implementation & Reproducibility

The complete calculation logic is implemented in:
- `evaluate_multiset_metric.py`

To reproduce the metric calculations and display the comparative table:
```bash
python3 Week_03_Prompting/Assignments/Task_3/evaluate_multiset_metric.py
```
Output data is automatically exported to:
- `multiset_metrics_summary.json`

---

## 7. Conclusion

The proposed **Multiset Fractional Retrieval Metric (MFRM)** effectively eliminates the evaluation cliff of binary exact matching. By computing Jaccard similarity, precision, recall, and $F_1$-scores across bag semantics, MFRM provides a fine-grained, diagnostically rich assessment that **complements** binary accuracy and accurately reflects user-perceived retrieval quality in AI-driven database engineering.
