import os
import pandas as pd

from resume_parser import extract_resume_text
from scoring import calculate_similarity


# Read the Job Description
with open("data/job_description.txt", "r", encoding="utf-8") as file:
    job_description = file.read()


results = []

# Read all resumes
for filename in os.listdir("resumes"):

    file_path = os.path.join("resumes", filename)

    try:
        resume_text = extract_resume_text(file_path)

        score = calculate_similarity(
            job_description,
            resume_text
        )

        results.append({
            "Candidate": filename,
            "Score": score
        })

        print(f"{filename} -> {score}%")

    except Exception as e:
        print(f"Could not process {filename}: {e}")


# Rank candidates
results.sort(
    key=lambda x: x["Score"],
    reverse=True
)


# Add rank
for rank, candidate in enumerate(results, start=1):
    candidate["Rank"] = rank


# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)


# Save results
df = pd.DataFrame(results)

df = df[
    ["Rank", "Candidate", "Score"]
]

df.to_csv(
    "output/ranked_candidates.csv",
    index=False
)


print("\nResume screening completed!")
print("Results saved to output/ranked_candidates.csv")