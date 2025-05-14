class Action:
    def __init__(self, pid, action_type, resource_name, cycle):
        self.pid = pid
        self.action_type = action_type.upper()  # READ o WRITE
        self.resource_name = resource_name
        self.cycle = int(cycle)

    def __repr__(self):
        return f"{self.pid} {self.action_type} {self.resource_name} @{self.cycle}"
