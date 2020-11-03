from gui.panels.customisation_type import CustomisationType

class MetadataBlock:
    def __init__(self, metadata, action_pairs, start_index, end_index, start_time, runtime):
        self.start_index = start_index
        self.end_index = end_index
        self.start_time = start_time
        self.metadata = metadata
        self.action_pairs = action_pairs
        self.runtime = runtime

    def desc(self):
        # Get all relevant animation information stored in the action pair metadata
        return self.metadata.desc()

    def start_position(self):
        return self.start_time * 1000

    def end_position(self):
        return (self.start_time + self.runtime) * 1000

    def first_pair(self):
        return self.action_pairs[0]

    def act(self):
        return self.first_pair().act()

    def can_set_runtime(self):
        return self.first_pair().can_set_runtime()

    def can_set_color(self):
        possible = False
        for action_pair in self.action_pairs:
            if action_pair.can_set_color():
                possible = True
                break
        return possible

    def get_color(self):
        for action_pair in self.action_pairs:
            if action_pair.can_set_color():
                return action_pair.get_color()
        return None

    def add_action_pair(self, action_pair):
        self.action_pairs.append(action_pair)
        self.end_index += 1

    def is_action_pair_in(self, action_pair):
        return action_pair in self.action_pairs

    def customizations(self):
        customizations = dict()
        if self.can_set_color():
            customizations[CustomisationType.COLOR] = self.get_color()

        if self.can_set_runtime():
            customizations[CustomisationType.RUNTIME] = self.runtime

        return customizations
