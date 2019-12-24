import glob
import markovify
import random

def load_corpora(file_glob='corpora/*.txt'):
  files = {}

  for file_name in glob.glob(file_glob):
    text = open(file_name, 'r')
    files[file_name] = text.read()

  return files

def get_markov_model():
  corpora_files = load_corpora()
  corpora_file_names = corpora_files.keys()

  markov_models = {key: markovify.Text(corpora_files[key], well_formed=False) for key in corpora_file_names}

  # Random weight from 0-2 with intervals of 0.1
  random_weights = random.sample([x * 0.1 for x in range(0, 21)], len(corpora_file_names))

  # Print out the weights of each text for the user
  print("RANDOM WEIGHTS:")
  for idx, key in enumerate(corpora_file_names):
    print(key + ": " + str(random_weights[idx]))
  print("")

  # Combine Markov Chains
  model_combo = markovify.combine(list(markov_models.values()))
  model_combo = model_combo.compile()

  print(model_combo.make_sentence())
  return model_combo
