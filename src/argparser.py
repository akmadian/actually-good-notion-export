import argparse

class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Actually Good Notion Export'
        )

        self.parser.add_argument('input_dir', type=str)

    def get_args(self):
        return self.parser.parse_args()