from chain import ToMSAParagraphChain
from termcolor import colored
def main():
    chain = ToMSAParagraphChain(cares_about_requests=False)
    chain('paragraph.txt')
if __name__ == '__main__':
    main()