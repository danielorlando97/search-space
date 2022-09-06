from . import ast


class VisitorLayer:
    @property
    def do_transform_to_modifier(self):
        return True

    @property
    def do_transform_to_check_sample(self):
        return True

    def transform_to_modifier(self, node, domain=None, context=None):
        return node, domain

    def transform_to_check_sample(self, node, sample, context=None):
        return node

# TODO: write visitor
