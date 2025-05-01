# GHA-Deploy-CLI
Python Command Line tool to run Github actions pipelines

# Usage
To install the tool use the following command:
```
pip install git+https://github.com/ktierney15/GHA-Deploy-CLI.git@version
```
GH Action run: ```gha-deploy [repo name] [pipeline name] [ref (or tag)]```

## Coming soon
- going to allow user to pass in username (or org). My user is hardcoded at the moment because only im using it
- CD to publish as a pypi package
- will add flags to allow user to pass inputs or not wait for the workflow to finish
