# Finding Cross-Textual Connections Using Python

In different electronic literature projects I often find myself needing to generate text out of a corpora of texts centered around a subject, style or time period.  Today we are going to build a simple and extendable Python script to allow us to make connections across a corpora of texts using the [`Markovify`](https://github.com/jsvine/markovify) package.

### Methodology

*TODO: Include quote about forming word pool here*

### Compiling our Corpora

For this project I am interested in urban theory and psychogeography, which is the study of urban geography and its effect on the emotions and behaviors of individuals. 

I compiled a number of texts I want to explore, including Guy Debord's *Society of Spectacle*, *Revolution of Everyday Life* by Raoul Vaneigem, Mervin Coverley's history of psychogeography, as well as some miscellaneous texts that I think will have interesting interactions like Poe's *Man in the Crowd* and Borges' *Garden of Forking Paths*.

I will store these texts as `.txt` files in a folder called `corpora` under my main project folder. Our script will start by loading our corpora into memory:
```py
import glob
 
def load_corpora(file_glob='./corpora/*.txt'):
    files = {}
    for file_name in glob.glob(file_glob):
	    text = open(file_name, 'r')
	    files[file_name] = text.read(100)
    return files
   ```

### Markov Chains
Markov Chains are a good first tool to try on a group of texts. It can be a bit of a blunt and sometimes requires many iterations before returning something useful (more on this later!) but it can be a quick and cheap way of generating unexpected insights and connections out of our corpora. 

I like the `Markovify` package  because it is easy to use but does a lot of powerful abstracting behind the scenes that we don't want to worry about initially (for example, by default it suppresses generated sentences that exactly overlap the original text so we get only new text).

To get started with `Markovify` we need to convert our dictionary of text files into Markov models using the `Text` function, which will generate a Markov chain out of each text. Then we will combine these Markov chains together using the handy `combine` helper. In this case we will also call `compile` on our model to improve speed:

```py
import markovify

corpora_files = load_corpora()
corpora_file_names = corpora_files.keys()
markov_models = {key: markovify.Text(corpora_files[key]) for key in corpora_file_names}
model_combo = markovify.combine(list(markov_models.values()), random_weights)
model_combo = model_combo.compile()
```

One more thing to make things more interesting--`combine` takes a second optional argument, a list of weights for each model that determines the relative emphasis of each one. Let's give each of our models a random weight.
```py
import random

corpora_file_names = corpora_files.keys()
    
# Random weight from 0-2 with intervals of 0.1
random_weights = random.sample([x * 0.1 for x in range(0, 20)], len(corpora_file_names))

# Print out the weights of each text for the user 
print("RANDOM WEIGHTS:")
for idx, key in enumerate(corpora_file_names):
    print(key + ": " + str(random_weights[idx]))
    
# Combine Markov Chains 
model_combo = markovify.combine(list(markov_models.values()), random_weights)
```
    
### Output
`Markovify` provides several ways to extract output from our new combined
 model. For this use case `make_sentence` will work for us.
 
```py
print(model_combo.make_sentence())
```
 

Some examples:

    Urbanism is the expression of the experience of nature, on the trivial surface of contemplated pseudo-cyclical time, the production of commodities

    Out of this time flows above its own past which has its basis in the streets
Not bad, but not exactly giving us enough traction to gain insights into our texts. During this phase we will need to generate many sentences out of our model and hand-pick the ones that draw our interest while discarding the rest.

One approach is to generate many sentences out of our model and save them to an external file. Then we can read through this file later and pick out the sentences that will server our project. 

Something more interesting is to present our user with a loop that serves sentences from our model and saves the ones the user chooses. Let's start with abstracting away all the above work into a single function `get_markov_model`. Then let's create a loop that presents the user with some options: `quit`, `save`, `discard`.
```py
markov_model = get_markov_model()

def get_user_choice():
    pass  # TODO

def save_sentence():
    pass  # TODO
def quit():
    pass # TODO

# set up input loop
choice = ''
while choice != 'q':
    new_sentence = markov_model.make_sentence()
    print(new_sentence)
    choice = get_user_choice()

    # option 1 is to save sentence
    if choice == '1':
	    save_sentence()
    elif choice == 'q':
	    quit()   
```

To fill out some of the TODOs, let's create a function that lets the user input whether they want to keep the current sentence. 
```py
def get_user_choice():
    print("\n[1] Save sentence.")
    print("[2] Discard sentence.")
    print("[q] Quit.")

    return input("What would you like to do? ")
```
Which outputs:

    With the development of capitalism, irreversible time as a journey containing its whole meaning within itself.

    [1] Save sentence.[2] Discard sentence.[q] Quit.
    What would you like to do? 
Cool! Now we can cycle rapidly through sentences to find the right ones for our project. But saving a sentence doesn't really do anything. Let's keep sentences in an output text file.

```py
def save_sentence(sentence):
    output_file = open('output.txt', 'a')
    output_file.write('\n %s \n' % sentence)
    output_file.close()
```

## Reshuffle
One last thing! At the beginning we assigned our models random weights, but it would be nice to reshuffle these weights to get different combinations. Let's give the user a new option to reshuffle the models.

```py
def get_user_choice():
    print("\n[1] Save sentence.")
    print("[2] Discard sentence.")
    print("[3] Reshuffle models. ")
    print("[q] Quit.")
```
And then we will simply compile a new model with new weights (this is very inefficient and might cause problems with very large corpora).

```py
	if choice == '1':
		save_sentence(new_sentence)
	if choice == '3':
		markov_model = get_markov_model()
	elif choice == 'q':
		quit()
```

## Next Steps
We now have an interactive way of creating useful word reservoirs out of our chosen corpora. These word reservoirs are often the first step in an electronic literature project and will allow us to quickly remix our chosen texts and create unexpected juxtapositions and insights.

As useful and easy as Markov Chains are, right now our tool can only combine whole files together and the user has no way to delve into specific interests or themes. Next we will look at how word vectors can help us solve these problems. 

