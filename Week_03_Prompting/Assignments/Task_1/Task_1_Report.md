# Task 1 Report: Prompting Framework Selection and Formulation

## 1. Executive Summary and Problem Domain

This report documents the selection, design rationale, and formulation of three distinct prompt engineering frameworks for **Week 03: Prompting Techniques** in the AI4SE course. The ultimate objective is to translate natural language user queries into executable SQLite SQL queries over the `restaurants` relational database for subsequent evaluation in **Task 2**.

### Task Requirements and Constraints
1. **Source Selection**: Frameworks were chosen from the framework repository [Frompting](https://frompting.com/frameworks).
2. **Explicit Exclusions**: As mandated by the assignment specification, neither the **ROSES** framework nor **zero-shot** prompting is utilized.
3. **Task 2 Alignment**: The formulated prompts must reliably address the schema requirements:
   - Tables: `RESTAURANT`, `LOCATION`, and `GEOGRAPHIC`.
   - Projection requirement: Target queries evaluated by `evaluate_retrieval_predictions.py` strictly require two projected columns in order: `(LOCATION.HOUSE_NUMBER, RESTAURANT.NAME)`.
   - Primary join: `RESTAURANT.ID = LOCATION.RESTAURANT_ID`.
   - Semantic robustness: Several input queries contain adversarial noise and conversational distractors (e.g., philosophical dilemmas about picnics, dumplings vs. pancakes, trips to the moon) which the LLM must disregard.
   - Output constraint: Pure, executable SQL string with no markdown code blocks or explanatory narrative.

---

## 2. Selected Prompt Frameworks

| Framework | Full Name / Acronym | Source URL | Core Paradigm |
|---|---|---|---|
| **CO-STAR** | Context, Objective, Style, Tone, Audience, Response | [https://frompting.com/frameworks/co-star](https://frompting.com/frameworks/co-star) | Constraint-bounded role & operational specification |
| **ICIO** | Instruction, Context, Input, Output | [https://frompting.com/frameworks/icio](https://frompting.com/frameworks/icio) | AI-native modular separation of instructions, data & constraints |
| **Few-Shot** | Few-Shot Learning (Exemplar Demonstration) | [https://frompting.com/frameworks/few-shot](https://frompting.com/frameworks/few-shot) | In-context demonstration via verified query pairs |

---

## 3. Detailed Framework Analysis and Formulations

### 3.1. Framework 1: CO-STAR

#### Origin and Source
- **Origin**: Developed by Sheila Teo and the GovTech Singapore team during the Government AI Prompt Engineering Competition.
- **Source**: Available on [Frompting: CO-STAR](https://frompting.com/frameworks/co-star).

#### Why CO-STAR was Chosen
CO-STAR is widely considered the industry benchmark for structured single-turn system prompts where the voice, format constraints, and domain scope are as critical as the core instruction. In an automated evaluation pipeline (such as `evaluate_retrieval_predictions.py`), standard LLM chat behavior—such as wrapping queries in ```sql markdown or adding pleasantries like *"Here is your SQL query:"*—causes immediate runtime parsing failures (`sqlite3.OperationalError`). 
CO-STAR explicitly provides dedicated slots for:
- **Audience** (an automated database driver),
- **Style** (standardized SQLite SQL), and
- **Response Format** (raw SQL string without fences),
thereby minimizing output format regressions.

#### Formulated Prompt
```text
# CONTEXT
You are an expert SQL database engineer interacting with a SQLite database containing restaurant data.
The database schema consists of:
- RESTAURANT (ID int(11) PRIMARY KEY, NAME varchar(255), FOOD_TYPE varchar(255), CITY_NAME varchar(255), RATING decimal(1,1))
- LOCATION (RESTAURANT_ID int(11) PRIMARY KEY, HOUSE_NUMBER int(11), STREET_NAME varchar(255), CITY_NAME varchar(255))
- GEOGRAPHIC (CITY_NAME varchar(255) PRIMARY KEY, COUNTY varchar(255), REGION varchar(255))

Foreign key relationships:
- LOCATION.RESTAURANT_ID references RESTAURANT.ID
- RESTAURANT.CITY_NAME references GEOGRAPHIC.CITY_NAME
- LOCATION.CITY_NAME references GEOGRAPHIC.CITY_NAME

# OBJECTIVE
Convert the provided natural language user question into a single, executable, and optimized SQLite SQL query.
Requirements:
1. Always project exactly two columns in this order: `LOCATION.HOUSE_NUMBER, RESTAURANT.NAME`.
2. Always JOIN RESTAURANT and LOCATION on `RESTAURANT.ID = LOCATION.RESTAURANT_ID`. JOIN GEOGRAPHIC only if county or regional filtering is required.
3. Ignore any conversational filler, chit-chat, or unrelated remarks in the question (e.g. debates about food preferences, picnics, umbrellas).
4. Interpret phrases such as "best" as sorting by rating in descending order: `ORDER BY RESTAURANT.RATING DESC LIMIT 1`.
5. Interpret rating conditions (e.g. "rating above X") as `RESTAURANT.RATING > X`.

# STYLE
Deterministic, standards-compliant SQLite SQL. Use uppercase for SQL keywords and explicit table aliases.

# TONE
Strictly technical and functional.

# AUDIENCE
An automated evaluation script running against an in-memory SQLite database via Python's sqlite3 engine.

# RESPONSE FORMAT
Return ONLY the raw SQL query on a single line or clean query block. Do not include markdown code blocks (```sql ... ```), explanations, comments, or extra whitespace.

# INPUT QUESTION
{question}
```

#### Expectations and Hypotheses
- **Syntactic Correctness**: Expected to approach 100% syntactically valid SQLite queries due to the explicit schema and SQL standard guidelines.
- **Format Compliance**: High compliance with the automated parser due to the `# RESPONSE FORMAT` and `# AUDIENCE` directives.
- **Vulnerability**: Without concrete exemplars, complex nested distractors might occasionally confuse column extraction if phrasing is ambiguous.

---

### 3.2. Framework 2: ICIO (Instruction-Context-Input-Output)

#### Origin and Source
- **Origin**: An AI-native engineering framework developed in prompt design literature to overcome instruction/data conflation.
- **Source**: Available on [Frompting: ICIO](https://frompting.com/frameworks/icio).

#### Why ICIO was Chosen
Large language models process input through attention across all token positions. When schema context, user instructions, input queries, and output rules are mixed into a narrative paragraph, the model can suffer from "instruction dilution" or semantic bleeding.
ICIO systematically decouples the four components:
1. **Instruction**: Pure operational logic (JOIN criteria, ranking, noise pruning).
2. **Context**: Static reference data (the database schema).
3. **Input**: Dynamic runtime variable (the question).
4. **Output**: Target format specification.

This architecture cleanly isolates the user question from the system directives, making it resilient to prompt injection or distractor sentences embedded in the question.

#### Formulated Prompt
```text
[INSTRUCTION]
Translate the given natural language question into a single valid SQLite query.
Follow these exact execution rules:
1. The SELECT clause must strictly return: LOCATION.HOUSE_NUMBER, RESTAURANT.NAME.
2. Join RESTAURANT (aliased as T1) with LOCATION (aliased as T2) on T1.ID = T2.RESTAURANT_ID. If county or region is queried, join GEOGRAPHIC (aliased as T3) on T1.CITY_NAME = T3.CITY_NAME.
3. Filter out all irrelevant conversational noise or distractors found in the question; extract only entities matching table attributes (food_type, city_name, street_name, rating).
4. If the question asks for the "best" restaurant, order by T1.RATING DESC and append LIMIT 1.
5. Rating thresholds described as "above X" must be expressed as T1.RATING > X.
6. The output must be directly executable by SQLite without syntax errors.

[CONTEXT]
Database Schema:
- Table: RESTAURANT
  Columns: ID (int, PK), NAME (varchar), FOOD_TYPE (varchar), CITY_NAME (varchar, FK), RATING (decimal)
- Table: LOCATION
  Columns: RESTAURANT_ID (int, PK, FK -> RESTAURANT.ID), HOUSE_NUMBER (int), STREET_NAME (varchar), CITY_NAME (varchar, FK -> GEOGRAPHIC.CITY_NAME)
- Table: GEOGRAPHIC
  Columns: CITY_NAME (varchar, PK), COUNTY (varchar), REGION (varchar)

[INPUT]
Question: {question}

[OUTPUT]
Provide strictly the SQL query text. Do not wrap in markdown fences. Do not add introductory or concluding remarks.
```

#### Expectations and Hypotheses
- **Modularity and Robustness**: Expected to isolate distractors effectively because the `[INPUT]` slot is strictly separated from `[INSTRUCTION]`.
- **Token Efficiency**: Lower token consumption per inference compared to CO-STAR and Few-Shot, leading to lower inference times in Task 2.
- **Edge-case Execution**: Expected to achieve balanced performance across standard and noisy queries.

---

### 3.3. Framework 3: Few-Shot Learning (In-Context Exemplar Demonstration)

#### Origin and Source
- **Origin**: Introduced in foundational LLM research (Brown et al., NeurIPS 2020: *"Language Models are Few-Shot Learners"*) and widely adopted across Text-to-SQL benchmarks (Spider, BIRD, WikiSQL).
- **Source**: Available on [Frompting: Few-Shot](https://frompting.com/frameworks/few-shot).

#### Why Few-Shot was Chosen
In database querying tasks, abstract descriptions (e.g., *"filter ratings and join appropriately"*) can leave subtle ambiguities:
- Should "best" use `LIMIT 1` or `MAX(RATING)`?
- How should multiple filters (street and rating) be joined in `WHERE`?
- How should distractor clauses be safely dropped while maintaining valid SQL structure?

Few-Shot prompting addresses this by providing concrete demonstrations (input-output pairs). By observing 4 verified patterns—including a noisy question with a distractor—the LLM leverages its in-context analogical reasoning capabilities. Furthermore, Few-Shot is fundamentally distinct from zero-shot prompting, honoring the negative constraint in the assignment.

#### Formulated Prompt
```text
You are an expert Text-to-SQL translation model for a SQLite database with the following schema:
- RESTAURANT (ID, NAME, FOOD_TYPE, CITY_NAME, RATING)
- LOCATION (RESTAURANT_ID, HOUSE_NUMBER, STREET_NAME, CITY_NAME)
- GEOGRAPHIC (CITY_NAME, COUNTY, REGION)

Join condition: RESTAURANT.ID = LOCATION.RESTAURANT_ID
Projection rule: Always select `LOCATION.HOUSE_NUMBER, RESTAURANT.NAME`.
Disregard any unrelated chatter or philosophical questions in the prompt.
Return only the raw SQL query with no markdown formatting or commentary.

Example 1:
Question: What is the best californian in portola valley ?
SQL: SELECT T2.HOUSE_NUMBER, T1.NAME FROM RESTAURANT AS T1 JOIN LOCATION AS T2 ON T1.ID = T2.RESTAURANT_ID WHERE T1.FOOD_TYPE = 'californian' AND T1.CITY_NAME = 'portola valley' ORDER BY T1.RATING DESC LIMIT 1;

Example 2:
Question: give me a restaurant on plaza way in lafayette with a rating above 1.8 (poorly rated or better)?
SQL: SELECT T2.HOUSE_NUMBER, T1.NAME FROM RESTAURANT AS T1 JOIN LOCATION AS T2 ON T1.ID = T2.RESTAURANT_ID WHERE T2.STREET_NAME = 'plaza way' AND T1.CITY_NAME = 'lafayette' AND T1.RATING > 1.8;

Example 3:
Question: While comparing dumplings with pancakes for an imaginary picnic, give me a restaurant on timber creek dr in san jose with a rating above 1.7 (poorly rated or better)?
SQL: SELECT T2.HOUSE_NUMBER, T1.NAME FROM RESTAURANT AS T1 JOIN LOCATION AS T2 ON T1.ID = T2.RESTAURANT_ID WHERE T2.STREET_NAME = 'timber creek dr' AND T1.CITY_NAME = 'san jose' AND T1.RATING > 1.7;

Example 4:
Question: what is a restaurant in forestville with a rating above 4.5 (excellent or better), though I am also choosing between noodles and a sandwich for a rainy picnic?
SQL: SELECT T2.HOUSE_NUMBER, T1.NAME FROM RESTAURANT AS T1 JOIN LOCATION AS T2 ON T1.ID = T2.RESTAURANT_ID WHERE T1.CITY_NAME = 'forestville' AND T1.RATING > 4.5;

Question: {question}
SQL:
```

#### Expectations and Hypotheses
- **Highest Multiset Accuracy**: By seeing verified SQL output patterns, the model will accurately replicate the exact column projection and join aliases.
- **Superior Noise Handling**: Example 3 and Example 4 explicitly show noisy conversational preambles being ignored, guiding the LLM by demonstration.
- **Inference Trade-off**: Prompt length is significantly larger (~400 tokens vs. ~200 tokens for ICIO), which will result in slightly higher inference latency during Task 2.

---

## 4. Comparative Framework Analysis

| Dimension | CO-STAR | ICIO | Few-Shot Learning |
|---|---|---|---|
| **Guiding Mechanism** | Persona, Tone & Contract Constraints | Structural modularity & Rule decomposition | Analogical demonstration (Exemplars) |
| **Handling of Distractors** | Rule-based instruction | Slot-isolation & instruction | Demonstrated behavior via examples |
| **Prompt Length (Tokens)** | Medium (~280 tokens) | Compact (~220 tokens) | High (~420 tokens) |
| **Expected Accuracy** | High (80–90%) | High (80–90%) | Very High (90–98%) |
| **Expected Latency** | Fast | Fastest | Slightly slower |
| **Risk Factor** | May occasionally retain extraneous tokens | Strict instruction following depends on LLM capability | High sensitivity to example selection |

---

## 5. Artifact Deliverables Summary

In accordance with Task 1 output criteria, the following files are produced:
1. **`prompts.json`**: A structured JSON data file containing all three prompt definitions, schema references, component mappings, and template strings ready for automated ingestion in Task 2.
2. **`Task_1_Report.md`** (this document): A comprehensive explanatory report justifying the framework selection, detailing where each framework was found, and providing expectations for empirical testing in Task 2.
