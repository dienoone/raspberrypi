class UploadFileChunk:
    def __init__(self, data, message_id, chunk_index, total_chunks):
        self.data = data
        self.message_id = message_id
        self.chunk_index = chunk_index
        self.total_chunks = total_chunks

    def to_dict(self):
        return {
            "Data": self.data,
            "MessageId": self.message_id,
            "ChunkIndex": self.chunk_index,
            "TotalChunks": self.total_chunks
        }
