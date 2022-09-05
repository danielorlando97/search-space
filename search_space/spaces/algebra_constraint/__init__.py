from . import ast


class VisitorLayer:
    def transform_to_modifier(self, node, context):
        return node

    def transform_to_check_sample(self, node, context):
        return node
