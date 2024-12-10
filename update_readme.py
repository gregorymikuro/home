import requests
import os

# Fetch Wakatime stats
API_KEY = os.getenv("WAKATIME_API_KEY")
url = f"https://wakatime.com/api/v1/users/current/summaries?start=2024-12-02&end=2024-12-09"
headers = {"Authorization": f"Bearer {API_KEY}"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    stats = {}
    for day in data["data"]:
        for lang in day["languages"]:
            lang_name = lang["name"]
            time_spent = lang["total_seconds"] / 3600  # Convert seconds to hours
            stats[lang_name] = stats.get(lang_name, 0) + time_spent

    # Format README content
    stats_str = "\n".join(
        f"{lang:<15} {time:.2f} hrs" for lang, time in sorted(stats.items(), key=lambda x: x[1], reverse=True)
    )
    readme_content = f"""
    ### Coding Stats (From: 02 December 2024 - To: 09 December 2024)

    ```plaintext
    {stats_str}
    ```
    """
    # Update README.md
    with open("README.md", "w") as readme:
        readme.write(readme_content)
else:
    print("Failed to fetch Wakatime stats.")
