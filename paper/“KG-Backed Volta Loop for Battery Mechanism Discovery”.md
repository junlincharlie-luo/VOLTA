A strong project would be:





## **“KG-Backed Volta Loop for Battery Mechanism Discovery”**





Build an agentic system that **proposes**, **tests**, and **falsifies** battery degradation mechanisms, where a **knowledge graph (KG)** is both the memory and reasoning substrate.



------





### **Core idea (one sentence)**





Use a knowledge graph to encode multi-modal battery evidence + causal hypotheses, then run an agent loop that automatically designs discriminative tests to invalidate weak mechanisms and refine the graph toward robust ones.



------





## **Why this is interesting**





Most “AI for batteries” systems either:



1. do retrieval/summarization, or
2. fit predictive models.





Your project goes beyond both: it does **scientific mechanism competition** under uncertainty:



- multiple rival mechanisms coexist,
- each mechanism makes testable predictions,
- an agent actively seeks experiments/simulations that best separate them.





That’s genuinely novel and high-impact for mechanistic battery science.



------





## **Project blueprint**







## **1) Build a** 

## **Mechanism-Centric Battery KG**





Not just materials-property triples. Include:



- **Entities**: material, phase, interface, defect, electrolyte species, operating condition, signal feature (Raman peak, XPS state, dQ/dV feature), mechanism node, failure mode.

- **Relations**:

  

  - increases, suppresses, competes_with, requires_condition,
  - causes_signal, explains_observation,
  - contradicted_by, supported_by.

  

- **Evidence edges** with provenance:

  

  - source type (paper, experiment, DFT, operando),
  - confidence,
  - context (SOC window, temperature, C-rate, voltage cutoff, particle size, dopant level).

  





This makes mechanism statements explicit and machine-verifiable.



------





## **2) Represent each hypothesis as a** 

## **structured subgraph**





Example hypothesis template:



- Claim: “Oxygen redox + TM migration drives voltage fade in LRLO under high upper cutoff.”
- Preconditions: composition, voltage window, cycling protocol.
- Predicted observables: peak shifts, gas evolution signature, lattice parameter drift, impedance trajectory.
- Competing alternatives: surface reconstruction-dominant pathway, electrolyte oxidation-dominant pathway.





Each hypothesis should produce **forward predictions** (what must appear) and **exclusion predictions** (what should not appear).



------





## **3) Agentic Volta loop (falsification-first)**





Create a multi-agent loop:



1. **Hypothesis Agent**

   Proposes mechanism candidates/subgraphs from KG gaps + literature.

2. **Prediction Agent**

   Converts each mechanism into quantitative/qualitative expected signatures.

3. **Discriminator Agent**

   Chooses next experiment/simulation maximizing expected falsification power.

4. **Execution Interface**

   Pulls results from historical dataset first (cheap), then proposes new test.

5. **Judge Agent**

   Scores each hypothesis (survival score) and updates KG edges:

   

   - strengthen support,
   - add contradiction,
   - split mechanism into conditional branches.

   





This turns your system into an autonomous “mechanism tournament.”



------





## **4) Key algorithmic novelty**





Use **value of information for falsification**:



- pick next test that maximizes expected drop in posterior for wrong hypotheses, not just predictive accuracy.





Possible scoring objective:

\text{Utility}(e)=\mathbb{E}\left[\Delta \sum_h w_h \cdot \mathbf{1}(\text{hypothesis } h \text{ falsified})\right] - \lambda \cdot \text{Cost}(e)

where e is candidate experiment, w_h is scientific importance/uncertainty weight.



## **5) Minimal viable scope (very doable)**





Start with one concrete problem:





### **Use case: Voltage fade mechanisms in Li-rich layered oxides**





Data channels:



- Raman time-series / spatial maps,
- dQ/dV features,
- EIS trends,
- optional XPS/STXM summaries from literature.





Hypothesis set (3–5):



- oxygen redox irreversibility dominant,
- TM migration dominant,
- surface rock-salt reconstruction dominant,
- electrolyte parasitic reaction dominant,
- coupled mechanism (interaction term).





Goal: show your agent can pick 1–2 decisive tests that eliminate at least half of candidates faster than a baseline planner.

## **6) What to publish as contributions**





You can frame three contributions:



1. **Representation**: mechanism-aware, evidence-weighted battery KG schema.
2. **Method**: falsification-driven agentic discovery loop with experiment selection.
3. **Benchmark**: open “mechanism tournament” tasks with known ground-truth or expert consensus trajectories.





This is much stronger than “we used LLM + KG for QA.”

## **7) Suggested system architecture (aligned with your stack)**





- KG: Neo4j or RDF/SPARQL + provenance graph layer.

- Vector layer: Chroma/FAISS for unstructured evidence chunks.

- Orchestrator: LangGraph (state machine for hypothesis lifecycle).

- Scientific tools:

  

  - spectrum feature extraction,
  - simple electrochemical simulators,
  - Bayesian updater for hypothesis confidence.

  

- Memory:

  

  - long-term: KG,
  - episodic: experiment history + agent decisions + rationale.

  

## **8) Evaluation metrics that reviewers will respect**





Don’t only report BLEU/accuracy-like metrics. Use:



- **Falsification efficiency**: hypotheses eliminated per unit cost/time.

- **Experiment efficiency**: number of tests to isolate top mechanism.

- **Causal consistency**: % of accepted hypotheses consistent with all retained evidence.

- **Generalization**: transfer from one chemistry/protocol to another.

- **Ablations**:

  

  - no KG,
  - no discriminator agent,
  - no falsification objective.

## **9) A concrete 12-week plan**





- **Weeks 1–2**: KG schema + ingestion pipeline (literature + your Raman metadata).
- **Weeks 3–4**: hypothesis templates + prediction interface.
- **Weeks 5–6**: discriminator agent (VOI/falsification scoring).
- **Weeks 7–8**: closed-loop on retrospective dataset.
- **Weeks 9–10**: compare baselines + ablation.
- **Weeks 11–12**: case study + paper draft figures.

If you want, I can sketch this next as:



1. a one-slide “project pitch” version for battery faculty,
2. a technical system diagram, and
3. a concrete JSON schema for your mechanism KG + hypothesis objects so you can start coding immediately.