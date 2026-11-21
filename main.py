import yaml
from pprint import pprint
from dataclasses import dataclass

@dataclass
class Block:
    id: str
    length: int
    occupied: bool = False

with open('./data/test_line.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

print(type(data))
#pprint(data)

block_dict: dict[str, Block] = {} #type hint
for block in data["blocks"]:
    block_dict[block['id']] = Block(**block)

block_dict['B3'].occupied=True

print('-'.join(f"[{block.id}{'*' if block.occupied else ''}]{block.length}m" for block in block_dict.values()))

