from datasets import load_dataset

dataset = load_dataset("dataset_valentina")
dataset.push_to_hub("axel-datos/dataset_valentina")
print(dataset.data)
"""dataset = load_dataset("lambdalabs/pokemon-blip-captions")
datasettrain = dataset['train']
print(datasettrain[0])"""