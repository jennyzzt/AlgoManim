class MetadataBlock:
    def __init__(self, metadata, action_pairs, start_time, runtime):
        self.metadata = metadata
        self.action_pairs = action_pairs
        self.start_time = start_time
        self.runtime = runtime

    def desc(self, sep='\n'):
        # Get all relevant animation information stored in the action pair metadata
        return self.metadata.desc(sep=sep)

    def start_position(self):
        return self.start_time * 1000

    def end_position(self):
        return (self.start_time + self.runtime) * 1000
