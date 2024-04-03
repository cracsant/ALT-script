# ALT-script
# Package Comparison Utility

This CLI utility compares packages between two repositories using a provided REST API. It fetches package data from the API, performs comparisons, and outputs the results in JSON format.

## Installation

1. Clone the repository to your local machine:

git clone https://github.com/cracsant/ALT-script

2. Navigate to the cloned repository:

cd ALT-script


## Usage

To run the utility, use the following command:

python3 script.py repo1 repo2

Replace "repo1" and "repo2" with the names of the repositories you want to compare. The available repository names are 'sisyphus', 'p10', and 'p9', according to the information provided. For example, to compare packages between 'sisyphus' and 'p10', you would run:

python3 script.py sisyphus p10

According to the information, we can only use the 'sisyphus', 'p10' and 'p9' repositories with this API request
The utility will fetch package data from the specified repositories, perform comparisons, and save the results in JSON files within the 'Comparison1', 'Comparison2', and 'Comparison3' folders.

## Dependencies

This utility requires Python 3 and the requests library. You can install the dependencies using pip:

pip install requests
