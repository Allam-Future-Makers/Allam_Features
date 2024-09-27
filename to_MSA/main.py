from chain import ToMSAChain
from termcolor import colored
def main():
    chain = ToMSAChain(cares_about_requests=False)
    while True:
        sentence = input(colored("Type here: ","green"))
        if sentence == 'exit':
            break
        result = chain(sentence)
        print(colored("Original: " + result['input_sentence'],"magenta"))
        print(colored("Corrected: " + result['finally_corrected_sentence'],"magenta"))

if __name__ == '__main__':
    main()