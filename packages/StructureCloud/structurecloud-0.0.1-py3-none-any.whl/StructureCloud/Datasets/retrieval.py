
import numpy as np
from datasets import load_dataset
from datasets.dataset_dict import DatasetDict
 
class StructureCloudDataset():
    '''
    A very simple class for loading StructureCloud datasets
    '''
    def __init__(self, dataset_name, num_fmt : callable = np.array, label_fmt : callable = None, **huggingface_kwargs):
        '''
        Args:
            dataset_name (str): name of the dataset to load
            num_fmt (type): the numerical format to use for the data. 
                default is numpy array, but can be changed to torch tensor or other formats
            label_fmt (type): a function that takes in the labels and returns a desired format of the labels.
                default is None, which means labels are returned as loaded
            huggingface_kwargs (dict): additional arguments to pass to load_dataset
            
        Default numerical format is numpy array
        '''

        if label_fmt is None:
            label_fmt = lambda x: x # no formatting

        self.label_fmt = label_fmt
        self.num_fmt = num_fmt
        self.dataset_name = dataset_name

        ds = load_dataset(
            f'StructureCloud/{dataset_name}',
            **huggingface_kwargs
            )
        
        if isinstance(ds, DatasetDict):
            splits = list(ds.keys())
            if len(splits) > 1:
                print(f'Multiple splits found, but none specified: {splits} \nDefaulting to {splits[0]}')
            ds = ds[splits[0]]

        self.data = ds
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        #get the data at select index and reformat it
        data = self.data[idx]
        pos = self.num_fmt(data['position'])
        node_class = self.num_fmt(data['node_class'])
        unit_cell = self.num_fmt(data['unitcell'])
        labels = self.label_fmt(data['labels'])
        return pos, node_class, unit_cell, labels