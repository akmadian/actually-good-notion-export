from argparser import ArgParser
from notion.Export import Export

def main():
    Parser = ArgParser()
    args = Parser.get_args()
    
    print(args)

    export = Export(args.input_dir)


if __name__ == '__main__':
    main()