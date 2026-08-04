stats = f"""

## 📊 My GitHub Statistics

| Statistik        |            Wert |
| ---------------- | --------------: |
| 📝 Total Commits | {total_commits} |
| 📦 Repositories  |    {len(repos)} |

"""

with open("README.md", "r", encoding="utf-8") as f:
readme = f.read()

readme = readme.replace("{{STATS}}", stats)

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme)

print("✅ README.md aktualisiert")
