import yaml
from simcore import track, train

def train_occpy_block(line: track.LinkedTrack, test_train: train.Train) -> list:
    train_pos_info = []
    curr = test_train.head_block_id
    remaining_length = test_train.length - test_train.head_offset
    train_pos_info.append(line.block_dict[curr].id)

    while remaining_length>0: #경계 조건
        curr=line.block_dict[curr].prev
        if curr is None:    
            break
        train_pos_info.append(line.block_dict[curr].id)
        remaining_length -= line.block_dict[curr].length

    return train_pos_info

def update_all_occupancy(line: track.LinkedTrack, train_pos_info_agg: list):
    for block in line.block_dict.values():
        block.occupied = False

    for bid in train_pos_info_agg:
        line.block_dict[bid].occupied=True

if __name__ == "__main__":
    with open('./data/test_line.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    whole_line = track.LinkedTrack(data)
    print("Line Loaded")
    print(whole_line)

    test_train1 = train.Train('Test1', 'B2', 330, 343)
    test_train2 = train.Train('Test2', 'B16', 100, 3403)
    
    update_all_occupancy(whole_line, train_occpy_block(whole_line, test_train1)+train_occpy_block(whole_line, test_train2))
    print("Train Loaded")

    print(whole_line)