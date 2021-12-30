from argparser import ArgParser
from notion.Export import Export

def main():
    Parser = ArgParser()
    args = Parser.get_args()
    
    print(args)

    export = Export(args.input_dir)
    export.do_replacements()
    export.do_export()


if __name__ == '__main__':
    main()