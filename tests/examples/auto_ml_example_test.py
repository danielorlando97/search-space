from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function


class AbsCluster:
    NClusterDomain = Domain[int]()

    def __init__(self, n_clusters: int = NClusterDomain) -> None:
        self.n = n_clusters


class KMeans(AbsCluster):
    pass


class AgglomerativeClustering(AbsCluster):

    def __init__(
        self,
        n_clusters: int = AbsCluster.NClusterDomain,
        affinity: str = Domain[str](
            options=['euclidean', 'manhattan', "l1", "l2"]
        )
    ) -> None:
        super().__init__(n_clusters)
        self.affinity = affinity


class AbsClassifier:
    NCategoryDomain = Domain[int]()

    def __init__(self, n_categories: int = NCategoryDomain) -> None:
        self.n = n_categories


class KNN(AbsClassifier):
    def __init__(self, n_categories: int = AbsClassifier.NCategoryDomain) -> None:
        super().__init__(n_categories * 2 - 1)


class GaussianNB(AbsClassifier):
    def __init__(self, n_categories: int = AbsClassifier.NCategoryDomain) -> None:
        super().__init__([1/n_categories for _ in range(n_categories)])


class SemiSupervisedClassifier:
    ClusterDomain = Domain[AbsCluster](
        options=[KMeans, AgglomerativeClustering])

    def __init__(
        self,
        cluster: AbsCluster = ClusterDomain,
        classifier: AbsClassifier = Domain[AbsClassifier](
            options=[KNN, GaussianNB]) | (
                lambda x, c=ClusterDomain: x.NCategoryDomain == c.NClusterDomain
        )

    ) -> None:
        self.cluster, self.classifier = cluster, classifier


class AutoMLUnsupervisedExample(TestCase):

    def test(self):
        space = Domain[SemiSupervisedClassifier]()

        @replay_function
        def ______():
            semi_supervised_model, _ = space.get_sample()

            assert isinstance(semi_supervised_model, SemiSupervisedClassifier)
            assert isinstance(semi_supervised_model.cluster, AbsCluster)
            assert isinstance(semi_supervised_model.classifier, AbsClassifier)
            assert semi_supervised_model.cluster.n == semi_supervised_model.classifier.n
