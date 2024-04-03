import os
import requests
import json
import argparse

# Function to make a request to the API and save response to a JSON file
def get_and_save_packages(branch, filename):
    print(f"Fetching packages from {branch}")
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "w") as file:
            json.dump(response.json(), file, indent=4)
        print(f"Saved packages from {branch} branch to {filename}")
    else:
        print(f"Failed to fetch packages from {branch} branch")

# Function to compare packages in two repositories and return packages only in 1st repository
def compare_packages_in_first(repo1, repo2):
    print("Comparing packages in the 1st repository...")
    total_packages = len(repo1)
    completed_packages = 0
    diff = set()
    for pkg in repo1:
        if pkg not in repo2:
            diff.add(pkg)
        completed_packages += 1
        progress = (completed_packages / total_packages) * 100
        print(f"\rProgress: {progress:.2f}%", end='', flush=True)
    print("\nComparison completed.")
    return diff

# Function to compare packages in two repositories and return packages only in 2nd repository
def compare_packages_in_second(repo1, repo2):
    print("Comparing packages in the 2nd repository...")
    total_packages = len(repo2)
    completed_packages = 0
    diff = set()
    for pkg in repo2:
        if pkg not in repo1:
            diff.add(pkg)
        completed_packages += 1
        progress = (completed_packages / total_packages) * 100
        print(f"\rProgress: {progress:.2f}%", end='', flush=True)
    print("\nComparison completed.")
    return diff

# Function to compare packages in two repositories and return packages with larger version in 1st repository
def compare_versions(repo1, repo2):
    print("Comparing package versions...")
    total_packages = len(repo1)
    completed_packages = 0
    diff = {}
    for pkg in repo1:
        if pkg in repo2 and repo1[pkg]["version"] > repo2[pkg]["version"]:
            diff[pkg] = repo1[pkg]
        completed_packages += 1
        progress = (completed_packages / total_packages) * 100
        print(f"\rProgress: {progress:.2f}%", end='', flush=True)
    print("\nComparison completed.")
    return diff

# Function to load packages from a JSON file
def load_packages(filename):
    print(f"Loading packages from {filename}...")
    with open(filename) as f:
        data = json.load(f)
    packages = {pkg["name"]: pkg for pkg in data["packages"]}
    print("Packages loaded.")
    return packages

# Function to save comparison results to a JSON file in a specified folder
def save_comparison_results(diff, folder, output_filename):
    if not os.path.exists(folder):
        os.makedirs(folder)
    print(f"Saving comparison results to {folder}/{output_filename}...")
    result = {"mismatch_count": len(diff), "mismatched_packages": list(diff)}
    with open(os.path.join(folder, output_filename), "w") as output_file:
        json.dump(result, output_file, indent=4)
    print("Comparison results saved.")

def main():
    parser = argparse.ArgumentParser(description="CLI utility to compare packages between two repositories")
    parser.add_argument("repo1", help="First repository to compare")
    parser.add_argument("repo2", help="Second repository to compare")
    args = parser.parse_args()
    if args.repo1 not in ["p9", "p10", "sisyphus"] or args.repo2 not in ["p9", "p10", "sisyphus"]:
        print("According to the information, we can only use the 'sisyphus', 'p10' and 'p9' repositories with this API request")
        exit()


    # Make requests and save responses to JSON files
    get_and_save_packages(args.repo1, f"{args.repo1}_packages.json")
    get_and_save_packages(args.repo2, f"{args.repo2}_packages.json")

    # Load packages from JSON files
    repo1_packages = load_packages(f"{args.repo1}_packages.json")
    repo2_packages = load_packages(f"{args.repo2}_packages.json")

    # Compare packages and save comparison results to JSON files for each architecture
    for arch in set(pkg["arch"] for pkg in repo1_packages.values()) | set(pkg["arch"] for pkg in repo2_packages.values()):
        diff1 = compare_packages_in_first(
            {pkg: repo1_packages[pkg] for pkg in repo1_packages if repo1_packages[pkg]["arch"] == arch},
            {pkg: repo2_packages[pkg] for pkg in repo2_packages if repo2_packages[pkg]["arch"] == arch})
        save_comparison_results(diff1, "Comparison1", f"comparison1_{arch}.json")

        diff2 = compare_packages_in_second(
            {pkg: repo1_packages[pkg] for pkg in repo1_packages if repo1_packages[pkg]["arch"] == arch},
            {pkg: repo2_packages[pkg] for pkg in repo2_packages if repo2_packages[pkg]["arch"] == arch})
        save_comparison_results(diff2, "Comparison2", f"comparison2_{arch}.json")

        diff3 = compare_versions(
            {pkg: repo1_packages[pkg] for pkg in repo1_packages if repo1_packages[pkg]["arch"] == arch},
            {pkg: repo2_packages[pkg] for pkg in repo2_packages if repo2_packages[pkg]["arch"] == arch})
        save_comparison_results(diff3, "Comparison3", f"comparison3_{arch}.json")

if __name__ == "__main__":
    main()
