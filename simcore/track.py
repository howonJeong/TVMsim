from dataclasses import dataclass
from enum import Enum

@dataclass
class Block:
    id: str
    length: int
    occupied: bool = False
    next: str | None = None
    prev: str | None = None
    switch_id: str | None = None

    def __str__(self) -> str :
        return f"[{self.id}{'*' if self.occupied else ''}]{self.length}m"


class SwitchDir(Enum):
    NORMAL = "NORMAL"    # 정위
    REVERSE = "REVERSE"  # 반위


@dataclass
class Switch:
    id: str
    block: str
    normal_next: str
    reverse_next: str
    direction: SwitchDir = SwitchDir.NORMAL  #정위
    locked: bool = False

    def __post_init__(self):
        if isinstance(self.direction, str):
            self.direction = SwitchDir(self.direction)

class LinkedTrack:
    def __init__(self, data):
        self.block_dict: dict[str, Block] = {}
        self.switch_dict: dict[str, Switch] = {}
        self.head: list[str] =[]

        for block in data["blocks"]:
            self.block_dict[block['id']] = Block(**block)
        for switch in data["switches"]:
            self.switch_dict[switch['id']] = Switch(**switch)
        
        self._validate_switches()

        for switch in self.switch_dict.values():
            self.block_dict[switch.block].switch_id = switch.id

        self.connect_track()

        for block in self.block_dict.values():
            if block.prev is None:
                self.head.append(block.id) #시작점 여러개 상황?

    def _validate_switches(self):
        for switch in self.switch_dict.values():
            if switch.block not in self.block_dict : 
                raise ValueError(f"{switch.id}: 놓인 블록 '{switch.block}'이 없음")            
            if switch.normal_next not in self.block_dict : 
                raise ValueError(f"{switch.id}: 정위 블록 대상 '{switch.normal_next}'이 없음")  
            if switch.reverse_next not in self.block_dict : 
                raise ValueError(f"{switch.id}: 반위 블록 대상 '{switch.reverse_next}'이 없음") 
            if switch.normal_next != self.block_dict[switch.block].next: 
                raise ValueError(f"분기기 상 정위 위치 '{switch.normal_next}' 포함 블록'{switch.block}' next가 동일하지 않음")  
                    
    def connect_track(self):
        for block in self.block_dict.values():
            if block.next is not None:
                self.block_dict[block.next].prev = block.id 
            #정위는 여기까지 자동으로 되고 반위는 아래에서
        for switch in self.switch_dict.values():
            self.block_dict[switch.reverse_next].prev = switch.block

    def next_block(self, block_id: str) -> str | None:
        if self.block_dict[block_id].switch_id is None:
            return self.block_dict[block_id].next
        else:
            cur_switch = self.switch_dict[self.block_dict[block_id].switch_id]
            if cur_switch.direction is SwitchDir.REVERSE:
                return cur_switch.reverse_next
            else:
                return cur_switch.normal_next

    def __str__(self) -> str:
        ret_str = []
        for cur in self.head:
            single_line = []
            while cur is not None:
                single_line.append((str(self.block_dict[cur])))
                cur=self.next_block(cur)
            ret_str.append('-'.join(single_line))
        return  '\n'.join(ret_str)
