import pickle
import pandas as pd
import ast
from sentence_transformers import SentenceTransformer, util
from pathlib import Path
def map_to_esco(
    extracted_df: pd.DataFrame,
    esco_df: pd.DataFrame,
    st_model,
    esco_embeddings
) -> pd.DataFrame:
    def enrich_raw_row(row):
        parts = [
            row["Skill"],
            row.get("Skill Description", ""),
            ", ".join(row["Knowledge Required"]),
            ", ".join(row["Task Abilities"]),
        ]
        return ". ".join([p for p in parts if p]) + "."

    raw_texts = extracted_df.apply(enrich_raw_row, axis=1).tolist()
    raw_embeds = st_model.encode(
        raw_texts, normalize_embeddings=True, show_progress_bar=True
    )
    sims = util.cos_sim(raw_embeds, esco_embeddings).cpu().numpy()

    records = []
    for i, row in extracted_df.iterrows():
        best_idx = sims[i].argmax()
        best_sim = sims[i][best_idx]
        records.append({
            "Research ID":            row["Research ID"],
            "Description":            row["Description"],
            "Raw Skill":              row["Skill"],
            "Raw Skill Description":  row["Skill Description"],
            "Level":                  row["Level"],
            "Best ESCO Skill":        esco_df.loc[best_idx, "preferredLabel"],
            "ESCO Skill Description": esco_df.loc[best_idx, "description"],
            "Skill Tag":              f"ESCO.{best_idx}",
            "Correlation":            round(float(best_sim), 4),
            "Knowledge Required":     row["Knowledge Required"],
            "Task Abilities":         row["Task Abilities"],
        })
    return pd.DataFrame(records)

# this file is src/my_package/matching.py
ESCO_EMBEDS_PATH = Path(__file__).parent / "public" / "esco_embeds.pkl"


def run_esco_mapping(extracted_df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    Load all resources, optionally limit to first `top_n` rows,
    then map to ESCO and return the result DataFrame.
    """
    # 1) Optionally trim
    df = extracted_df if top_n is None else extracted_df.head(top_n)

    # 2) Load ESCO lookup table & embeddings
    esco_df = pd.read_csv("https://raw.githubusercontent.com/LAiSER-Software/datasets/refs/heads/master/taxonomies/ESCO_skills_Taxonomy.csv")             # your ESCO labels+desc
    with ESCO_EMBEDS_PATH.open("rb") as f:
        esco_embeddings = pickle.load(f)

    # 3) Init encoder
    st_model = SentenceTransformer("all-mpnet-base-v2")

    # 4) Perform mapping
    best_df = map_to_esco(df, esco_df, st_model, esco_embeddings)

    # 5) Save & return
    best_df.to_csv("best_esco_matches.csv", index=False)
    return best_df
