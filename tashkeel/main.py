from chain import TashkeelChain
from termcolor import colored


def main():
    chain = TashkeelChain()
    print(colored("Arabic Diacritization Tool", "cyan"))
    print(colored("Type 'exit' to quit", "yellow"))

    while True:
        sentence = input(colored("\nEnter Arabic text: ", "green"))
        if sentence.lower() == "exit":
            break

        result = chain(sentence)
        print(colored("\nOriginal: ", "magenta") + sentence)
        print(colored("Diacritized: ", "magenta") + result)


if __name__ == "__main__":
    main()
