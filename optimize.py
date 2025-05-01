import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import optuna
import pandas as pd

from rbf import RBF

#
# Configuration: Set the expected number of centers here
#
EXPECTED_CENTERS = 15

#
# Configuration: Set the number of trials here
#
N_TRIALS = 100_000

DATASET = "owid-covid-data.csv"

df = pd.read_csv("owid-covid-data.csv")
df = df.loc[df["location"] == "Brazil"]
df["weekly_new_deaths_mean"] = df["new_deaths"].rolling(window=7).mean()
df["weekly_new_cases_mean"] = df["new_cases"].rolling(window=7).mean()
df["weekly_new_deaths_mean"] = df["weekly_new_deaths_mean"].fillna(method="ffill")
df["weekly_new_cases_mean"] = df["weekly_new_cases_mean"].fillna(method="ffill")
df.fillna(method="ffill", inplace=True)
df = df[::7]

def objective(trial):
    sigma = trial.suggest_float('sigma', 0.005, 0.01, step=0.001)
    lambda_ = trial.suggest_float('lambda_', 0.5, 0.8, step=0.05)
    alpha = trial.suggest_float('alpha', 0.025, 0.25, step=0.05)
    delta = 1

    rbf = RBF(sigma, lambda_, alpha, delta)
    for index, row in df.iterrows():
        value = row["weekly_new_deaths_mean"]
        rbf.add_element(value)      

    return abs(EXPECTED_CENTERS - len(rbf.centers))

study_name = "covid_ocwid"
storage_name = "sqlite:///{}.db".format(study_name)
study = optuna.create_study(study_name=study_name, storage=storage_name, load_if_exists=True)
study.optimize(objective, n_trials=N_TRIALS)

print(study.best_params)