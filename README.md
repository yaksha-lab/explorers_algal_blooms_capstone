# Predicting the Extent of Harmful Algal Blooms Using Satellite Imagery and Machine Learning

This repository is a capstone project for SIADS 699 as part of the Unversity of Michigan Master of Applied Data Science (MADS) program.

**Objective:**

Harmful algae blooms (HABs) have become an increasingly concerning issue in recent years due to their negative impacts on water quality, ecosystem health, and human activities. By leveraging ML techniques, it may be possible to detect and delineate HABs with higher accuracy and efficiency, enabling effective management strategies to mitigate their negative impacts. One of the most common types of algae responsible for HABs is cyanobacteria. Cyanobacteria produce toxins that are poisonous to humans and other animals. Cyanotoxins can cause a wide variety of adverse human health problems including gastrointestinal distress, dermatitis, liver failure, or even death of pets and livestock when they are exposed to water with high levels of toxins. Manual water sampling is often used to assess risk from cyanobacteria. Manual water sampling is accurate, but it is time consuming and generally cost prohibitive across large areas. The use of satellite imagery and computer algorithms to detect HABs shows great promise. Identifying the presence and estimated extent of HABs would allow for more targeted manual sampling effort and better warnings for drinking water systems and recreational water users.


**Methods - model selection, training, and hyperparameter tuning**

We used a form of unsupervised semantic segmentation, known as Self-supervised Transformer with Energy-based Graph Optimization (STEGO), to identify clusters of related pixels in satellite images of lakes. The STEGO model was developed by Hamilton et al. (2022) and is described in a paper titled ‘Unsupervised Semantic Segmentation by Distilling Feature Correspondences’. We experimented with using the pre-trained model developed by Hamilton and with training the model on our own image data.

To identify the optimal combinations of hyperparameters we conducted a grid search. We included the following hyperparameters in our grid search: number of steps(max_steps), number of neighbors(num_neighbors), number of classes(dir_dataset_n_classes), learning rate(lr), batch size(batch_size), and model type(model_type).

Source code from the author was heavily edited to reflect config parameters.




**How to train a model:**

You can use the included google colab notebook to train a model of your choice (STEGO_Colab_Train_Final.ipynb). 

The model training uses a forked version of the STEGO repository, found here: (https://github.com/yaksha-lab/STEGO_prod) 

Please rename the above repository to STEGO for training.

Please use a git diff to see the difference between our STEGO_prod branch and the original STEGO repo, linked in the additional questions section.

**Model training process:**

**Crop Datasets (Optional)** 

Data can be prepared for training using crop_datasets.py. There are several crop types to choose from.

**Precomputed KNNs**

Precomputing KNNs are dependent on the resolution and batch size of the training config. This is done with precompute_knns.py. They must be recomputed each time the following parameters are changed:

  - training/validation/test data, 
  - batch size 
  - training resolution

**Train Segmentor**

train_segmentation.py trains the segmentor using pretrained DINO weights. The weights come in a variety of patch sizes (8/16) and transformer sizes (small/base). For more information on DINO, please see this repository (https://github.com/facebookresearch/dino). If precompute_knns.py is run then this script will train a model based on the dataset inputs and save checkpoint intervals.

  **Additional Questions?**
  Please refer to the original STEGO repo here (https://github.com/mhamilton723/STEGO) 

**Data Access**

Color image data used for this project was collected by the Copernicus Sentinel-3A and Sentinel-3B satellites in 2022 and early 2023. The CIcyano prediction images were produced by the National Oceanographic and Atmospheric Administration (NOAA) using Copernicus Sentinel-3 satellite data from the same time period. Both the color images and the CIcyano prediction images were accessed on the NOAA NCCOS HAB Data Explorer webpage (https://products.coastalscience.noaa.gov/habs_explorer/index.php).

The image data we used is also included in this repository.
