import os 
import sys
import csv
import json
import pickle
import multiprocessing as mp

import matplotlib.pyplot as plt

import numpy as np
import torch
from rdkit import Chem
from tqdm import tqdm

import gzip
import shutil

'''
USEFUL FUNCTIONS FOR DATASET STATS PLOT AND SAVING

Instructions:
1. create some iterable that load your source data in the following format:
    
    node_pos, node_class, unitcell, labels = dataset[idx]
    note: labels is a dictionary of one or two dictionaries containing labels 
           labels[object] = object wise labels
           labels[node] = node wise labels

2. pass this iterable to the dataset_histogram function and save the plot 
    
    fig, stat_dict = dataset_histogram(dataset, max_sample_size=-1, full_data_range=True, random_order=True)
    fig.savefig('dataset_histogram.png')

    if your dataset is too large, you can set max_sample_size to a smaller number

3. save your dataset into a set of chunks in either a json or pickle file format

    save_to_chunks( dataset, 
                    output_directory,  # the directory to save data chunks to, will be made if it does not exist
                    chunk_size=-1,     # this means the entire dataset will be saved in one file
                    file_type='pkl',   # 'pkl' or 'json'
                    jobs=1,            # number of parallel jobs to use for saving. Default is 1 (no parallelism).
                    progress_bar=True  # show a progress tqdm bar for saving in a notebook
                    )


'''


def cannonicalize_smiles(smiles):
    """
    Convert a SMILES string to its canonical form.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        # raise ValueError(f'Invalid SMILES string: "{smiles}" ')
        print(f'Invalid SMILES string!! : "{smiles}" ')
        return None
    return Chem.MolToSmiles(mol, canonical=True)

def get_bounding_box(points):
    """
    Calculate the bounding box of a set of points.
    """
    if isinstance(points, torch.Tensor):
        points = points.detach().cpu().numpy()

    min_x = np.min(points[:, 0])
    max_x = np.max(points[:, 0])
    min_y = np.min(points[:, 1])
    max_y = np.max(points[:, 1])
    min_z = np.min(points[:, 2])
    max_z = np.max(points[:, 2])

    length_x = max_x - min_x
    length_y = max_y - min_y
    length_z = max_z - min_z

    #convert into a unit cell, a unit cell is a 3x3 matrix
    unit_cell = np.array([[length_x, 0, 0],
                           [0, length_y, 0],
                           [0, 0, length_z]])
    
    return torch.tensor(unit_cell)


from scipy.spatial.distance import pdist
def longest_unit_cell_diagonal(cell: np.ndarray) -> float:
    indices = np.array([[i, j, k] for i in [0, 1] for j in [0, 1] for k in [0, 1]])
    corners = indices @ cell.T
    return np.max(pdist(corners))



def dataset_histogram(dataset, max_sample_size : int =100000, full_data_range: bool =True, random_order : bool = True, seed=12345) -> plt.Figure:
    '''
    input needs to be cannonical dataset with output format  pos, node_class, unit_cell, labels
    dataset (iterable) : object providing samples
    max_sample_size (int) : maximum number of samples to use for the histograms.
        sampling the entire dataset may be slow, or may not fit in memory.
        if max_sample_size < 1, this will sample the entire dataset.
    full_data_range (bool) : if True, this will iterate over the entire dataset to compute the range (min,max) of 
        number of points (N), length of the unit cell (min, max), and range of elements (n_total)
    random_order (bool) : if True, this will shuffle the dataset before sampling.
    seed (int) : random seed for reproducibility

    Example usage:
    fig = dataset_histogram(dataset, max_sample_size=-1, full_data_range=True, random_order=True)
    fig.savefig('dataset_histogram.png')
    '''

    if max_sample_size < 1:
        max_sample_size = len(dataset)

    max_N = -1
    min_N = np.inf
    
    max_ldiag = -1 
    min_ldiag = np.inf
    max_lxyz = -1 
    min_lxyz = np.inf
    unique_node_id_count = -1 # number of uniques elements in dataset

    N_sample = []
    lxyz_sample = []
    ldiag_sample = []
    id_samples = []
    id_count = {} # store a count of unique elements/node classes in the dataset
    n_count = {}

    order = np.arange(len(dataset))
    if random_order:
        rand_gen = np.random.default_rng(seed)
        rand_gen.shuffle(order)
    
    for i, idx in enumerate(tqdm(order)):
        #assume outputs are in tensor or numpy format
        pos, node_id, unit_cell, labels = dataset[idx]
        
        N = pos.shape[0]
        if isinstance(N, torch.Tensor):
            N = N.item()
        
        node_id = node_id.flatten()
        if isinstance(node_id, torch.Tensor):
            node_id = node_id.tolist()
        
        if N > max_N:
            max_N = N
        if N < min_N:
            min_N = N
       
        #check if N is in n_count
        if N in n_count:
            n_count[N] += 1
        else:
            n_count[N] = 1
        
        for id in node_id:
            assert isinstance(id, int), f"node_id must be an integer, got {type(id)}"
            if id in id_count:
                id_count[id] += 1
            else:
                id_count[id] = 1
                unique_node_id_count += 1

        #orthogonalize the unit cell to get the lengths
        lxyz = np.linalg.norm(unit_cell, axis=1).reshape(-1) #NOTE: this assumes lattice vectores are stacked on dim 0
        lxyz_max_i = np.max(lxyz)
        lxyz_min_i = np.min(lxyz)
       
        if lxyz_max_i > max_lxyz:
            max_lxyz = lxyz_max_i
        if lxyz_min_i < min_lxyz:
            min_lxyz = lxyz_min_i

        ldiag_i = longest_unit_cell_diagonal(unit_cell.numpy())
        if ldiag_i > max_ldiag:
            max_ldiag = ldiag_i
        if ldiag_i < min_ldiag:
            min_ldiag = ldiag_i
        
        if i <= max_sample_size-1:
            N_sample.append(N)
            id_samples.extend(node_id)
            lxyz_sample.extend(lxyz.tolist())
            ldiag_sample.append(ldiag_i)
        elif not full_data_range:
            break

    range_dict = {}
    range_dict['N'] = (min_N, max_N)
    range_dict['Lxyz'] = (min_lxyz, max_lxyz)
    range_dict['Ldiag'] = (min_ldiag, max_ldiag)
    range_dict['unique_node_ids'] = id_count.keys()
    range_dict['unique_node_ids_count'] = len(id_count.keys())
    
    N_bins = np.arange(min_N, max_N+1)
    L_bins = np.linspace(min_lxyz, max_ldiag, 100)

    #plot histograms
    fig_scale = 2
    fig, ax = plt.subplots(3, 1, figsize=(5*fig_scale, 5*fig_scale))
    ax[0].hist(N_sample, bins=N_bins, density=True, alpha=1)
    ax[0].set_xlabel('Number of atoms (N)')
    ax[0].set_ylabel('Fraction')
    ax[0].set_title('Number of nodes in dataset: min={}, max={}'.format(min_N, max_N))


    ax[1].hist(lxyz_sample, bins=L_bins, density=True, alpha=0.6, label='lxyz')
    ax[1].hist(ldiag_sample, bins=L_bins, density=True, alpha=0.6, label='ldiag')
    ax[1].set_xlabel('Length of unit cell side (lxyz) and max diagonal (ldiag)')
    ax[1].set_ylabel('Fraction')
    ax[1].legend()
    ax[1].set_title(f'Unitcell lengths in dataset: min={min_lxyz:0.3f}, max={max_ldiag:0.2f}')

    #use id_count dictionary to plot a bar graph of the number of unique elements
    id_max_count = max(id_count.values())
    id_relative_count = [v/id_max_count for v in id_count.values()]

    #convert id_count.keys() to a list 
    string_ids = [str(id) for id in np.sort(list(id_count.keys()))] #.to_list().sort
    ax[2].bar(string_ids, id_relative_count)
    ax[2].set_xlabel('Unique node ids (elements)')
    ax[2].set_ylabel('Relative Count')

    fig.suptitle('Histogram sample size: {}'.format(len(N_sample)))
    fig.tight_layout()
    fig.subplots_adjust(top=0.9)

    return fig, range_dict



#### functions for saving to files ###

def format_values(value):
    """
    Convert a value to a format suitable for JSON serialization.
    """
    if isinstance(value, torch.Tensor):
        return value.detach().cpu().tolist()
    elif isinstance(value, np.ndarray):
        return value.tolist()
    elif isinstance(value, list):
        return [format_values(v) for v in value]
    elif isinstance(value, dict):
        return {k: format_values(v) for k, v in value.items()}
    else:
        return value
   
def write_chunk(chunk, chunk_name : str, output_dir : str, file_type : str, compress : bool):
        ''' 
        chunk : list of dictionaries, each dictionary is a sample
        '''
        file_ext = {'json': 'jsonl',  # default to jsonl
                    'jsonl': 'jsonl', # default to jsonl
                    'pkl': 'pkl',
                    'pickle' : 'pkl'}[file_type]
       
        chunk_path = os.path.join(output_dir, f'{chunk_name}.{file_ext}')
        open_cmd = gzip.open if compress else open
        if compress:
            # add .gz to the filename
            chunk_path += '.gz'

        if file_ext == 'pkl':
            with open_cmd(chunk_path, 'wb') as f:
                pickle.dump(chunk, f)
        elif file_ext == 'jsonl':
            with open_cmd(chunk_path, 'wt', encoding='utf-8') as f:
                json_lines = [json.dumps(item) for item in chunk]
                f.write('\n'.join(json_lines) + '\n')
        else:
            raise ValueError(f"Unsupported file type: {file_type}. Supported types are: {list(file_ext.keys())}")

def process_dataset_chunk(dataset, data_indices, chunk_name, output_dir, file_type, compress, progress_bar=False):
    if progress_bar:
        data_indices = tqdm(data_indices, desc=f"Formating {chunk_name}")

    data_list = []
    for idx in data_indices:
        position, node_class, unitcell, labels = dataset[idx]
 
        # Format each sample
        sample = {
            'position': format_values(position),
            'node_class': format_values(node_class),
            'unitcell': format_values(unitcell),
            'labels': format_values(labels),
            }
        data_list.append(sample)
    
    if progress_bar:
        print(f"Writing chunk {chunk_name} with {len(data_list)} samples")
    write_chunk(data_list, chunk_name, output_dir, file_type, compress)
    return chunk_name

       
def save_to_chunks(dataset, output_dir, chunk_size=-1, file_type='json', jobs=1, 
                   prefix='chunk', progress_bar=True, compress=True):
    """
    Save the entire dataset to a single JSON file or series of JSON files for a given chunksize.


    Args:
        dataset (iterable): Object providing samples in the standard format.
        output_path (str): Path to save the JSON file.
        chunk_size (int): Number of samples to save in each chunk. 
                          If -1, the entire dataset will be saved in one file.
                          note: chunking will try and maintain fiel size regularity
                          actual chunking may not be the same as chunk_size
        file_type (str): Type of file to save. 'json' or 'pkl' for pickle.
        jobs (int): Number of parallel jobs to use for saving. Default is 1 (no parallelism).
        prefix (str): Prefix for the chunk files. Default is 'chunk_i'.
        compress (bool): If True, compress the JSON file using gzip. Default is True.

    Dataset sample output must be:
        position, node_class, unitcell, labels = dataset[idx]
    """

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} does not exist. Creating directory.")
        os.makedirs(output_dir, exist_ok=False)

    if chunk_size is None or chunk_size < 0:
        #save the entire dataset in one file
        chunk_size = len(dataset)

    #determine the number of chunks
    num_chunks = len(dataset) // chunk_size + (1 if len(dataset) % chunk_size > 0 else 0)
    print(f"Saving dataset in {num_chunks} chunks of size {chunk_size} with {jobs} jobs...")

    jobs = max(min(jobs, num_chunks), 1) # limit the number of jobs to the number of chunks

    all_data_indices = np.arange(len(dataset))
    chunk_indices = np.array_split(all_data_indices, num_chunks)
    print(f"Chunk sizes: {[len(c) for c in chunk_indices]}")
    job_args = []
    for i in range(num_chunks):
        chunk_name = f'{prefix}_{i+1}'
        chunk_indices_i = chunk_indices[i]
        kwargs = {'dataset': dataset,
                    'data_indices': chunk_indices_i,
                    'chunk_name': chunk_name,
                    'output_dir': output_dir,
                    'file_type': file_type,
                    'compress': compress,}
        job_args.append(kwargs)

    if jobs <= 1:
        for i, job_args in enumerate(job_args):
            process_dataset_chunk(**job_args, progress_bar=progress_bar)
    else:
        # Use multiprocessing to save chunks in parallel
        def callback_fn(out):
            print(f"{out} saved successfully")
        def err_callback_fn(out):
            print(f"Error in process: {out}")

        with mp.Pool(processes=jobs) as pool:
            job_outs = []
            for i, kwargs in enumerate(job_args):
                res = pool.apply_async(process_dataset_chunk, kwds=kwargs, callback=callback_fn, error_callback=err_callback_fn)
                job_outs.append(res)

            pool.close()
            pool.join()
            print("All jobs complete!")

    print(f"Data saved to {output_dir}")

