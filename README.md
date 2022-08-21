# Knowledge-Graph-Application-MscProject
## Description
The code for making projection of logical and multilateral relations into the vector space and give reasonable answer to it.
## Functions of script files
### train.py
* The script to extract information from the pkl files and train it.
* The results are logged in a text file.
### data_utils.py
* Return the reconstituted object hierarchy of the pickled representation data of an object.
### train_helpers.py
* Calculate the exponential movement average (EMA) loss as well as the AUC-ROC values during the iteration process.
### model.py
* Define the end-to-end autoencoder models for representation learning on heteregenous graphs/networks.
* Define the encoder decoder model that reasons about edges, metapaths and intersections.
### utils.py
* The script that stores misc utility functions.
### graph.py
* Define the embedding of the graph and queries.
### encoders.py
* Define various encoder classes that is used in this project.
### decoder.py
* Define various decoder classes that is used in this project.
### aggregators.py
* Define various aggregator classes that is used in this project.
### nodetypes.py
* Define node types that is adapted to Neo4j.
### relations.py
* Define relation types that is adapted to Neo4j.
### graphparser.py
* Extract information from the datafile and give 
### buildgraph.py
* Create a Buildgraph() class and create a knowledge graph in the Neo4j database.
## Setup and requirements
Run `pip install -r requirements.txt` to obtain the necessary requirements.
The data used in this project can be downloaded [here](https://drive.google.com/file/d/1bMD0RHLWbKJIfI4FTZct7M6MBLbj2VuA/view?usp=sharing)
## Running the code
Input the command `python -m nqe.bio.train` to train the model. By default the configuration of this model is set at its best performance, you can check in details and change it if you want. The output of this data is automatically logged and saved in a text file in directory "./netquery/engineering". If you are training with GPU, please add a cuda flag in your command, i.e., `python -m nqe.bio.train --cuda`.
