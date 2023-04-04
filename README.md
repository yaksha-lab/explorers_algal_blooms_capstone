This repository is a capstone project for SIADS 699 as part of the Unversity of Michigan Master of Applied Data Science (MADS) program.

**Objective:**

Harmful algae blooms (HABs) have become an increasingly concerning issue in recent years due to their negative impacts on water quality, ecosystem health, and human activities. By leveraging ML techniques, it may be possible to detect and delineate HABs with higher accuracy and efficiency, enabling effective management strategies to mitigate their negative impacts. One of the most common types of algae responsible for HABs is cyanobacteria. Cyanobacteria produce toxins that are poisonous to humans and other animals. Cyanotoxins can cause a wide variety of adverse human health problems including gastrointestinal distress, dermatitis, liver failure, or even death of pets and livestock when they are exposed to water with high levels of toxins. Manual water sampling is often used to assess risk from cyanobacteria. Manual water sampling is accurate, but it is time consuming and generally cost prohibitive across large areas. The use of satellite imagery and computer algorithms to detect HABs shows great promise. Identifying the presence and estimated extent of HABs would allow for more targeted manual sampling effort and better warnings for drinking water systems and recreational water users.


**Methods - model selection, training, and hyperparameter tuning**

We used a form of unsupervised semantic segmentation, known as Self-supervised Transformer with Energy-based Graph Optimization (STEGO), to identify clusters of related pixels in satellite images of lakes. The STEGO model was developed by Hamilton et al. (2022) and is described in a paper titled ‘Unsupervised Semantic Segmentation by Distilling Feature Correspondences’. We experimented with using the pre-trained model developed by Hamilton and with training the model on our own image data.


**How to train a model:**

You can use the included google colab notebook to train a model of your choice (STEGO Colab Trainv3.ipynb). 

The model training uses a forked version of the STEGO repository, found here: (https://github.com/yaksha-lab/STEGO_prod)

**Model training process:**

**Crop Datasets (Optional)** 

Data can be prepared for training using crop_datasets.py. There are several crop types to choose from.

**Precomputer KNNs**

Precomputing KNNs are dependent on the resolution and batch size of the training config. This is done with precompute_knns.py. They must be recomputed each time the following parameters are changed:

  - training/validation/test data, 
  - batch size 
  - training resolution

**Train Segmentor**

train_segmentation.py trains the segmentor using pretrained DINO weights. The weights come in a variety of patch sizes (8/16) and transformer sizes (small/base). For more information on DINO, please see this repository (https://github.com/facebookresearch/dino). If precompute_knns.py is run then this script will train a model based on the dataset inputs and save checkpoint intervals.

  **Hyperparameter Tuning**

To ensure an optimal model, we will need to tune hyperparameters to our specific data and task. Hyperparameters are key settings that determine the behavior and performance of a machine learning model. Tuning these hyperparameters allows us to ensure that it achieves the best possible results. We have decided to evaluate the following parameters within our grid search:



*   Number of Neighbors: 'n_neighbors': [3, 5, 7]
*   Batch Size: 'batch_size': [8, 16, 32, 64]
*   Model: model_type: ['KNN', 'SVM', 'RandomForest']
*   Number of Steps: 'max_steps': [4000, 5000, 6000, 10000]
*   Classes: 'dir_dataset_n_classes': [2, 5, 10] 










```python

```
