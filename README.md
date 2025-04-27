# RMIDDM - COVID19 Experiment

## What is RMIDDM?

**RMIDDM** (Radial Markov Interpretable Drift Detection Method) is a novel method designed to detect concept drift (changes) in data streams at runtime. It aims to overcome limitations of existing approaches by leveraging a combination of **Radial Basis Function Networks (RBFN)** and **Markov Chains (MC)**.

Key characteristics of RMIDDM include:

*   **Runtime Detection:** Identifies changes as data arrives.
*   **Computational Efficiency:** Designed to be performant.
*   **Label Independence:** Operates without needing ground truth labels (unsupervised).
*   **Interpretability:** Provides insights into the detected changes.

Experiments conducted on both synthetic datasets and real-world data (specifically, the COVID-19 dataset) have demonstrated that RMIDDM achieves competitive results and exhibits reliable behavior.

## What is the experiment ?

This repository contains an experiment designed to evaluate the real-world applicability of RMIDDM. The experiment utilizes the COVID-19 dataset provided by Our World in Data (OWID). This dataset includes information related to the COVID-19 pandemic—a severe acute respiratory syndrome caused by SARS-CoV-2—which was declared a global pandemic by the WHO on March 11th, 2020. The pandemic has significantly impacted global health, the economy, and politics.

## Requirements

* [**uv**](https://docs.astral.sh/uv/)
* Python 3.8
* Dependencies:  `requirements.txt`

## Setup and running 

1. Install [**uv**](https://docs.astral.sh/uv/)
2. Clone this repository
3. Create a virtual environment

```
uv venv -p 3.8
```

4. Activate

```
source .venv/bin/activate
```

5. Install dependencies using **uv pip**:

```
uv pip install -r requirements.txt
```

6. Run the experiment:

```
streamlit run main.py
```

A webbrowser will open with the experiment interface. You can select the parameters and run the experiment. The results will be displayed, like the example below:

![Streamlit Interface for RMIDDM COVID-19 Experiment](streamlit.gif)


---



# Parameters Optimization

The parameters of RMIDDM were optimized using [Optuna](https://optuna.org/), a hyperparameter optimization framework. This approach allowed us to systematically search for the optimal configuration of parameters to maximize the detector's performance on the COVID-19 dataset. The default parameters used in this experiment represent the best-performing configuration identified through this optimization process.


## Objective Function

The objective function for parameter optimization was based on the number of concepts detected by RMIDDM. Through careful visual inspection of COVID-19 data trends and patterns, we established a target number of concepts that should be identified in the dataset. The optimization process aimed to find parameter configurations that would result in RMIDDM identifying a number of conceptual changes close to this target, reflecting the known major phases and transitions in the pandemic timeline.

The best parameter configurations were tested and further fine-tuned.

## Running the optimization process

1. Install [**uv**](https://docs.astral.sh/uv/)
2. Clone this repository
3. Create a virtual environment

```
uv venv -p 3.8
```

4. Activate

```
source .venv/bin/activate
```

5. Install dependencies using **uv pip**:

```
uv pip install -r requirements.txt
```

6. Edit the parameters in `optimize.py` file.

7. Run the process:

```
python optimize.py
```

8. Check the results througt `optuna-dashboard`:

```
uv run optuna-dashboard sqlite:///covid_ocwid.db
```

9. Open the dashboard in your web browser at `http://localhost:8080` to visualize the optimization process and results, like the example below:



![Optuna Dashboard](optuna.gif)
