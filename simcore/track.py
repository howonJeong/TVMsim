from dataclasses import dataclass

@dataclass
class Block:
    id: str
    length: int
    occupied: bool = False
    next: str | None = None
    prev: str | None = None

    def __str__(self) -> str :
        return f"[{self.id}{'*' if self.occupied else ''}]{self.length}m"

class LinkedTrack:
    def __init__(self, data):
        self.block_dict: dict[str, Block] = {}
        self.head: list[str] =[]
        for block in data["blocks"]:
            self.block_dict[block['id']] = Block(**block)
        self.connect_track()
        for block in self.block_dict.values():
            if block.prev is None:
                self.head.append(block.id) #시작점 여러개 상황?

    def connect_track(self):
        for block in self.block_dict.values():
            if block.next is not None:  
                self.block_dict[block.next].prev = block.id 

    def __str__(self) -> str:
        ret_str = []
        for cur in self.head:
            single_line = []
            while cur is not None:
                single_line.append((str(self.block_dict[cur])))
                cur=self.block_dict[cur].next
            ret_str.append('-'.join(single_line))
        return  '\n'.join(ret_str)
