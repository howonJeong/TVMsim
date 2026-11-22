class Train:
    def __init__(self, train_id, head_block_id: str, head_offset, length):
        self.train_id = train_id
        self.head_block_id = head_block_id
        self.head_offset = head_offset
        self.length = length

    def __str__(self) -> str:
        return f"{self.train_id} within block {self.head_block_id}: {self.head_offset}m"             