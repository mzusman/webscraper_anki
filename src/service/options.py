import argparse

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
class WebscrapperAnkiOptions:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description='pass parameter for the program')
        self.parser.add_argument("--file", default=None,type=str,help="file with a list of words seperated by backslash n")
        self.parser.add_argument("--inline", default=None,type=str,nargs='+',help="inline words seperated by space")
        self.parser.add_argument("--examples_words",type=str2bool,nargs='?',help="add the examples words as well")
        pass

    def parse(self):
        return self.parser.parse_args()

