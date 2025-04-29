# StructureCloud
A collection of 3D Point cloud datasets commonly used for training generative modeling and molecular discovery. 

## Install

install hugging face dataset library 
```bash
pip install datasets 
```

install StructureCloud (TODO: not yet on PyPi)
```bash
$ pip install StructureCloud
```


## StructureCloud Datasets
StructureCloud is aimed at simplifying pointcloud dataset retrieval and manipulation with a simple unifying output format. The datasets in StructureCloud are chosen speifically for training models that adress problems related to 3D structures.


## Usage
```python
import numpy as np
import torch
from StructureCloud.Datasets import StructureCloudDataset as scd

# load numerical values as numpy objects
dataset_default = scd('dataset_name', split='train') 

# load numerical values as torch tensors
dataset_torch = scd('dataset_name', split='train', num_fmt=torch.tensor) 

#dataset output format is as follows
positions, features, unitcell, lables = dataset[index]

# output shapes:
# positions [N, 3] - positions in 3d space
# features [N, 1] or [N, d] - node feature/identities (ie element#, class, etc) 
# unitcell/bounding box [3,3]
# labels - a dictionary
# lables['node'] = { dict of nodewise lables : [N,d] } 							
# labels['object] = { dict of whole object labels : [d] }


#### selecting and formating data labels ###
## by default, the labels dictonary returns all additional information associated with the dataset.
## but a specific label can be selected by defining a formating function in 'label_fmt' 

get_object_target = lambda x : torch.tensor(x['object']['targets'])
get_object_smiles = lambda x : x['object']['SMILES']

qm9_regression = StructureCloudDataset('QM9', label_fmt = get_object_target)
qm9_smiles = StructureCloudDataset('QM9', label_fmt = get_object_smiles )

reg_target = qm9_regression[1000][3]
smiles = qm9_smiles[1000][3]
print(smiles)
print(reg_target)

```

### Available Datasets
**Small Organic Molecules**
- QM9
- PCQM4Mv2
- GEOM

**Proteins and biomolecules**
- AlphaFold Homo Sapiens (proteins)
- (LP)PDBbind2020

**Materials**
- MP-20
- Perov-5
- Carbon-24
- MPTS-52
- PCOD2

**3D objects**
- coming soon...

**Gaussian Splats**
- coming soon..,
- 


