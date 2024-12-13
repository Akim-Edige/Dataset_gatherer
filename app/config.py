import os

# Path to dataset directory
DATASET_DIR = 'dataset'
# List of signs (you can customize this list)
SIGNS = ['hello', 'thank_you', 'please', 'yes', 'no']
# Path to labels and metadata files
LABELS_FILE = os.path.join(DATASET_DIR, 'labels.json')
METADATA_FILE = os.path.join(DATASET_DIR, 'metadata.csv')
