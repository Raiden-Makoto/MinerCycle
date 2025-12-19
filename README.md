# 🧪 Inverse Design of High-Performance Structural Ceramics

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Library](https://img.shields.io/badge/Library-Pymatgen%20%7C%20Matminer-green)
![ML](https://img.shields.io/badge/Model-Random%20Forest-orange)

## 📋 Executive Summary
The discovery of lightweight, high-stiffness materials is critical for transforming the aerospace and automotive industries, where reducing mass directly translates to increased fuel efficiency, range, and payload capacity, while high stiffness ensures these structural components maintain their shape and integrity under heavy loads. Moreover, these materials are essential for reducing global carbon emissions and enabling next-generation technologies, such as long-range electric vehicles and cost-effective space exploration platforms.  

This project utilized Machine Learning (Random Forest Regression & Classification) to discover novel MAX-phase composites, which are advanced materials that combine metallic and ceramic properties using layered ternary compounds $M_{n+1}AX_n$, where $M$=transition metal, $A$=Group IIIA/IVA element, $X$=C/N/B, $n$=1-3. These compounds are hexagonal, layered nanostructures with strong M-X bonds (covalent/metallic) and weaker M-A bonds, allowing us to combine ceramic strength (high modulus) with metallic properties (conductivity, machinability, plastic deformation), in addition to thermal/oxidation resistance and damage tolerance. 

By training on 10,000+ materials from the **Materials Project** database, the model learned to predict the elastic properties and thermodynamic stability of uncharacterized compounds. The pipeline successfully "rediscovered" known MAX-phase ceramics such as V2PC (validating accuracy), and identified **Niobium Silicon Carbide (Nb2SiC)** as a novel candidate with a specific stiffness **60% higher than industry-standard steel**.

---

## 🚀 Key Results

### 1. The Novel Discovery: Nb₂SiC
The model identified **Nb₂SiC** as a high-potential candidate.
* **Predicted Specific Stiffness:** ~43 GPa/(g/cm³)
* **Comparison:** 1.7x more efficient than Titanium Alloy; 1.6x more efficient than Steel.
* **Status:** High-priority candidate for Density Functional Theory (DFT) validation.

### 2. Validation (The "Sanity Check")
To ensure the model learned physical laws rather than noise, its predictions were analyzed for known materials:
* **Ti₂SiC:** Model predicted **96% Stability** (Correct: It is a well-known stable MAX phase).
* **V₂PC:** Model predicted **77% Stability** (Correct: It is a known metastable material).
* **Conclusion:** The model correctly distinguishes between stable, metastable, and unstable chemistries.

<p align="center">
  <img src="figures/portfolio_plot.png" alt="Pareto Front Visualization" width="600">
  <br>
  <em>Figure 1: The proposed candidates (Gold Stars) plotted against the known universe of materials (Grey). Nb2SiC sits significantly above the baseline of common structural materials.</em>
</p>

### 🧪 3. Thermodynamics & Synthesis Verification

To validate the ML predictions, **Density Functional Theory (DFT) surrogate calculations** was performed on the generated candidates using the **CHGNet Universal Potential** (pre-trained on 1.5M+ quantum calculations).

* **Geometric Stability:** The crystal structure retained **98.3%** of its volume during relaxation (Volume Change: +1.66%), indicating excellent structural integrity.

<p align="center">
  <img src="figures/Nb4Si2C2.png" alt="Candidate Structure" width="600">
  <br>
</p>

* **Reaction Energetics:** The  formation energy ($\Delta H_f$) was calculated from elemental precursors:
    $$2\text{Nb} + \text{Si} + \text{C} \rightarrow \text{Nb}_2\text{SiC}$$
    * **Result:** $\Delta H_f = \mathbf{-2.647 \text{ eV/f.u.}}$ (Exothermic).
    * **Implication:** There is a strong thermodynamic driving force for synthesis.

---

## 🛠️ Methodology

The discovery pipeline consists of three stages:

### Phase 1: Data Acquisition & Cleaning
* **Source:** Materials Project API (`mp_api`).
* **Filtering:** Removed radioactive elements, noble gases, and entries with incomplete elastic tensors.
* **Final Dataset:** ~12,000 materials with calculated Bulk Modulus ($K$) and Density ($\rho$).

### Phase 2: Feature Engineering
* **Descriptors:** Converted chemical formulas (e.g., "Ti2AlC") into numerical vectors using **Matminer** and **Magpie** statistics (atomic radii, electronegativity, valence electrons, etc.).
* **Algorithm:** * **Regressor:** `RandomForestRegressor` (Estimating Stiffness & Density).
    * **Classifier:** `RandomForestClassifier` (Estimating Thermodynamic Stability / Distance to Hull).

### Phase 3: Generative Screening (The "Dreamer")
* **Search Space:** Generated 2,000+ hypothetical **MAX Phase** structures ($M_2AX$) using combinatorial substitution.
    * $M$: Ti, V, Cr, Zr, Nb, Mo, Hf, Ta, W
    * $A$: Al, Si, P, S, Ga, Ge, In, Sn
    * $X$: C, N, B
* **Selection Criteria:** Materials were ranked by **Specific Stiffness** ($K / \rho$) and filtered for a $>67\%$ predicted probability of stability.

---

## 📊 Performance Comparison

The chart below highlights the efficiency gap between the AI-discovered candidate and traditional engineering materials.

| Material | Specific Stiffness (GPa / g/cm³) | Notes |
| :--- | :--- | :--- |
| **Diamond** | 126 | Theoretical Limit (Too expensive/brittle) |
| **Nb₂SiC (This Project)** | **43** | **Novel AI Candidate** |
| **Titanium Alloy** | 26 | Aerospace Standard |
| **Steel (304)** | 25 | Construction Standard |
