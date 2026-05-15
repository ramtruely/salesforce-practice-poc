import requests
import sys

# ----------------------------
# CONFIG
# ----------------------------
OWNER = "ramtruely"   # your GitHub username
REPO = "salesforce-practice-poc"
TOKEN = ""  # 🔥 replace

PR_NUMBER = sys.argv[1]

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

print(f"\n🔍 Tracking PR #{PR_NUMBER}\n")

# ----------------------------
# Step 1: Get PR commits
# ----------------------------
commits_url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}/commits"
commits_res = requests.get(commits_url, headers=headers)

if commits_res.status_code != 200:
    print("❌ Failed to fetch commits:", commits_res.text)
    sys.exit(1)

commits_data = commits_res.json()

commit_shas = [c["sha"] for c in commits_data]

# ----------------------------
# Step 2: Get workflow runs
# ----------------------------
runs_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"
runs_res = requests.get(runs_url, headers=headers)

if runs_res.status_code != 200:
    print("❌ Failed to fetch runs:", runs_res.text)
    sys.exit(1)

runs_data = runs_res.json()["workflow_runs"]

# ----------------------------
# Step 3: Filter runs for PR commits
# ----------------------------
matched_runs = [
    r for r in runs_data if r["head_sha"] in commit_shas
]

# ----------------------------
# Step 4: Count results
# ----------------------------
total = len(matched_runs)
success = sum(1 for r in matched_runs if r["conclusion"] == "success")
failed = sum(1 for r in matched_runs if r["conclusion"] == "failure")

# ----------------------------
# Output
# ----------------------------
print("📊 Summary")
print("-----------------------------")
print(f"Total Runs     : {total}")
print(f"Successful Runs: {success}")
print(f"Failed Runs    : {failed}")

print("\n📄 Details")
print("-----------------------------")

for r in matched_runs:
    print(f"{r['name']} | {r['conclusion']} | {r['html_url']}")
