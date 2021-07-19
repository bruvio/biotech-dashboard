import logging

import pandas as pd

logger = logging.getLogger()


def get_data():
    try:

        assay = pd.read_csv("./data/assay_results.csv")
        labels = pd.read_csv("./data/compound_labels.csv")
        ic50 = pd.read_csv("./data/compound_ic50.csv")
        df = pd.merge(assay, labels, on="Compound ID")
        df.columns = ["ID", "Concentration", "Inhibition", "Label"]
    except Exception:
        logger.error("failed to read data")
        return None, None, None, None
    return assay, ic50, labels, df
