# 🔮 Automatic Review Validation (CHAR-1977)

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Installing](#installing)
- [Usage](#usage)

---

## About <a name = "about"></a>

All code and models related to Basic Automatic Review Validation.

- [Jira (CHAR-1977)](https://nextchance.atlassian.net/browse/CHAR-1977/)
- [Confluence](https://nextchance.atlassian.net/wiki/spaces/CHAR/pages/1970372613/Automatic+review+validation)
- [Documentation](https://github.com/NextChance/charmander-data/blob/main/CHAR-1977_Automatic_review_validation/README.md)

## Getting Started <a name = "getting_started"></a>

There is a folder distribution, related with the functionality of the proyect.

- aws: All the scripts related with the deploy of the model in SageMaker endpoint.
- data: If needed, artifacts or small datasets neccesary for the model deploy.
- docs: Any additional documentation needed.
- notebooks: Folder for exploration notebooks and similar. **This documents musn't not to be neccesary for the model deploy.**
- src: All the code with models and infrastructure.
- streamlit: All the code for streamlit demo (if was needed).
- test: All the tests related with the deploy of the model.

## Installing <a name = "installing"></a>

For running all the models of this folder, first we will install the requirements.txt file, using:

```
pip install -r requirements.txt
```


## Usage <a name = "usage"></a>

To use the streamlit demo, you need to run:

```
streamlit run "{LOCAL_FOLDER}/charmander-data/CHAR-1977_Automatic_review_validation/streamlit/demo_streamlit.py"
```
