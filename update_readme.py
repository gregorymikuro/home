import os
import requests

# Fetch Wakatime stats
API_KEY = os.getenv("WAKATIME_API_KEY")
URL = "https://wakatime.com/api/v1/users/current/summaries?start=2024-12-02&end=2024-12-09"

headers = {"Authorization": f"Bearer {API_KEY}"}
response = requests.get(URL, headers=headers)

if response.status_code == 200:
    data = response.json()["data"]
    language_totals = {}

    # Summarize total time per language
    for day in data:
        for language in day["languages"]:
            name = language["name"]
            total_seconds = language["total_seconds"]
            language_totals[name] = language_totals.get(name, 0) + total_seconds

    # Convert seconds to hours and format stats
    formatted_stats = "\n".join(
        f"{lang:<15} {total_seconds / 3600:.2f} hrs" 
        for lang, total_seconds in sorted(language_totals.items(), key=lambda x: x[1], reverse=True)
    )

    # Update README
    with open("README.md", "r") as readme_file:
        readme_content = readme_file.readlines()

    # Find the coding stats section and replace content
    updated_content = []
    in_stats_section = False
    for line in readme_content:
        if "### Coding Stats" in line:
            in_stats_section = True
            updated_content.append(line)
            updated_content.append(f"```plaintext\n{formatted_stats}\n```\n")
        elif in_stats_section and line.strip() == "":
            in_stats_section = False
        elif not in_stats_section:
            updated_content.append(line)

    with open("README.md", "w") as readme_file:
        readme_file.writelines(updated_content)
else:
    print(f"Failed to fetch Wakatime stats. HTTP {response.status_code}: {response.text}")
