from ..asts import constraints


class VisitorLayer:

    @property
    def do_domain_optimization(self):
        return True

    @property
    def do_transform_to_modifier(self):
        return True

    @property
    def do_transform_to_check_sample(self):
        return True

    def domain_optimization(self, node, domain):
        return node, domain

    def transform_to_modifier(self, node, domain, context):
        return node, domain

    def transform_to_check_sample(self, node, sample, context):
        return node


# TODO: write visitor
