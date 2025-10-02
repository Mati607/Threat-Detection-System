# TrustWatch

## Prerequisites
1. Install the Jupyter environment to run our system. [Installation Guide](https://jupyter.org/install).
2. Install the dependencies listed in the `requirements.txt` file.

### Evaluation on DARPA OpTC & E3
1. We used the same ground truth and train/test split as the [FLASH system](https://github.com/DART-Laboratory/Flash-IDS).
2. Use the parser from the FLASH repository to prepare the data files.
3. Provide the path to these data files for TrustWatch to function.

### Evaluation on E5
1. Due to the large size of the E5 dataset, we initially ingested the complete dataset into an Elasticsearch storage system.
2. We then utilized the ground truth and train/test split from the [KAIROS system](https://github.com/ProvenanceAnalytics/kairos).
3. You can choose to locally parse the E5 dataset and generate the data files using the timestamps provided in the TrustWatch E5 scripts.
4. Alternatively, you can ingest the data into an Elasticsearch cluster by providing your credentials in the script, which will then execute automatically.
5. Information on data ingestion into Elasticsearch is available at this [link](https://www.elastic.co/blog/how-to-ingest-data-into-elasticsearch-service).

#### Acknowledgements
Some of the code used in TrustWatch has been adapted from the FLASH system.