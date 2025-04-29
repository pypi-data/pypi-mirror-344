import re
import json
import ast
import pandas as pd
from dep_laiser.run_gemini import generate_structured_skills
from dep_laiser.matching import run_esco_mapping

pd.set_option('display.max_colwidth', None)
import json

def load_syllabi_data() -> pd.DataFrame:
    """
    Load your syllabi data. Modify this function to read from CSV, database, etc.
    """
    syllabi_data = pd.read_csv("https://raw.githubusercontent.com/LAiSER-Software/datasets/refs/heads/master/syllabi-data/preprocessed_50_opensyllabus_syllabi_data.csv")
    return syllabi_data

def generate_results(df: pd.DataFrame) -> list[str]:
    """
    Calls the LLM for each row in df.
    Returns a list of raw JSON strings.
    """
    raws = []
    for _, row in df.iterrows():
        raw = generate_structured_skills(
            query=row.to_dict(),
            input_type="syllabi",
            num_key_skills=5,
            num_key_kr="3-5",
            num_key_tas="3-5"
        )
        raws.append(raw)
    return raws

def parse_results(raws: list[str], df: pd.DataFrame) -> pd.DataFrame:
    """
    Parses LLM outputs and attaches metadata.
    """
    records = []
    for i, raw in enumerate(raws):
        text = raw.strip()
        start = text.find('[')
        end = text.rfind(']') + 1
        snippet = re.sub(r',\s*([\]\}])', r'\1', text[start:end])
        try:
            parsed = json.loads(snippet)
        except json.JSONDecodeError:
            parsed = ast.literal_eval(snippet)

        meta = df.iloc[i]
        for entry in parsed:
            entry.update({
                "Research ID": meta["id"],
                "Title": meta["title"],
                "Description": meta["description"],
                "Learning Outcomes": meta["learning_outcomes"]
            })
            records.append(entry)

    # Desired column order
    columns = [
        "Research ID",
        "Title",
        "Description",
        "Learning Outcomes",
        "Skill",
        "Level",
        "Knowledge Required",
        "Task Abilities",
        "Skill Description"
    ]
    return pd.DataFrame(records, columns=columns)

def load_extracted(path="extracted_anket_df.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    # turn those string‐lists back into real lists
    for col in ["Knowledge Required", "Task Abilities"]:
        df[col] = df[col].apply(ast.literal_eval)
    return df
def extract_skills(
    df: pd.DataFrame,
    title: str = "title",
    description: str = "description",
    learning_outcomes: str = "learning_outcomes"
) -> pd.DataFrame:
    """
    df: user’s DataFrame
    title_col: name of the column with the course title
    desc_col: name of the column with the course description
    learning_outcomes_col: name of the column with learning outcomes
    """
    # 1) Rename user’s columns to what generate_results & parse_results expect
    mapping = {
        title: "title",
        description: "description",
        learning_outcomes: "learning_outcomes"
    }
    df_renamed = df.rename(columns=mapping)

    # 2) Generate LLM raw outputs (uses df_renamed["title"/"description"/"learning_outcomes"])
    raw_jsons = generate_results(df_renamed)

    # 3) Parse and build final DataFrame
    extracted_df = parse_results(raw_jsons, df_renamed)

    # 4) Run the ESCO‐mapping pipeline on the first 10 rows
    best_df = run_esco_mapping(extracted_df)

    return best_df
if __name__ == "__main__":
     extract_skills()
