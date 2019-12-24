from get_markov_model import get_markov_model

markov_model = get_markov_model()

def get_user_choice():
    print("\n[1] Save sentence. ")
    print("[2] Discard sentence. ")
    print("[3] Reshuffle models. ")
    print("[q] Quit. ")
    
    return input("What would you like to do? ")

def save_sentence(sentence):
  output_file = open('output.txt', 'a')
  output_file.write('\n %s \n' % sentence)
  output_file.close()

# set up input loop
choice = ''
while choice != 'q':
  new_sentence = markov_model.make_sentence()
  print('\n %s \n' % new_sentence)

  choice = get_user_choice()

  if choice == '1':
    save_sentence(new_sentence)
  if choice == '3':
    markov_model = get_markov_model()
  elif choice == 'q':
    quit()
