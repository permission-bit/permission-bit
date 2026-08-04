import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

repos = []
page = 1

while True:
    response = requests.get(
        "https://api.github.com/user/repos",
        headers=headers,
        params={
            "visibility": "all",      # public + private
            "affiliation": "owner",   # nur Repos, die dir gehören
            "per_page": 100,
            "page": page
        }
    )

    response.raise_for_status()
    data = response.json()

    if not data:
        break

    repos.extend(data)
    page += 1

print(f"Repositories: {len(repos)}")

for repo in repos:
    private = "🔒 Privat" if repo["private"] else "🌍 Öffentlich"
    print(f"{private} - {repo['name']}")


total_commits = 0

for repo in repos:
    print(f"Durchsuche {repo['name']}...")

    page = 1

    while True:

        response = requests.get(
            f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/commits",
            headers=headers,
            params={
                "author": repo["owner"]["login"],
                "per_page": 100,
                "page": page,
            },
        )

        response.raise_for_status()

        commits = response.json()

        if not commits:
            break

        total_commits += len(commits)

        page += 1

print(f"\n📝 Gesamtzahl der Commits: {total_commits}")

stats = f"""<!-- START_STATS -->
## 📊 GitHub Statistics

| Statistik | Wert |
|-----------|------:|
| 📝 Total Commits | {total_commits} |
| 📦 Repositories | {len(repos)} |
<!-- END_STATS -->"""


with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()


start = "<!-- START_STATS -->"
end = "<!-- END_STATS -->"

start_index = readme.find(start)
end_index = readme.find(end)


if start_index == -1 or end_index == -1:
    raise Exception(
        "Stats-Bereich nicht gefunden. Füge START_STATS und END_STATS in README.md ein."
    )


end_index += len(end)


readme = (
    readme[:start_index]
    + stats
    + readme[end_index:]
)


with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)


print("✅ README.md aktualisiert")