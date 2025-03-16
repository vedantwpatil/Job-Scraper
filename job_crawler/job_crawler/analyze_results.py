import json
import pandas as pd
import os
from datetime import datetime


def analyze_results():
    # Load the results
    results_path = "internship_results/cs_internships.json"
    if not os.path.exists(results_path):
        print("No results found. Run the spider first.")
        return

    with open(results_path, "r") as f:
        internships = json.load(f)

    print(f"Found {len(internships)} potential internships")

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(internships)

    # Filter for high-quality matches
    quality_matches = df[
        (df["title"].str.contains("intern|internship|co-op|coop", case=False))
        & (
            df["title"].str.contains(
                "software|developer|engineer|computer|data|web|full stack|frontend|backend",
                case=False,
            )
        )
    ]

    print(f"Found {len(quality_matches)} high-quality CS internship matches")

    # Save as CSV for easy viewing
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"internship_results/cs_internships_{timestamp}.csv"
    quality_matches.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

    # Show top companies with internships
    top_companies = quality_matches["company"].value_counts().head(10)
    print("\nTop companies with CS internships:")
    print(top_companies)


if __name__ == "__main__":
    analyze_results()
