from jsonschemacodegen import python as pygen
import json
import argparse
parser = argparse.ArgumentParser(
                    prog='GenerateModels',
                    description='Generate Models from schema')

parser.add_argument('--schema', type=argparse.FileType('r', encoding='UTF-8'), required=True)
parser.add_argument('--class', required=True, dest='cls', metavar='CLASS')
parser.add_argument('--file', required=True)

args = parser.parse_args()
generator = pygen.GeneratorFromSchema("src/utils/")
generator.Generate(json.load(args.schema), "gen_", args.cls, args.file)
