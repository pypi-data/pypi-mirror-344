from datasets import load_dataset

# Load dataset from an S3 URL
dataset = load_dataset("csv", data_files="s3://my-bucket-name/path/to/data/*.csv")

# Inspect the dataset
print(dataset)

dataset.map()