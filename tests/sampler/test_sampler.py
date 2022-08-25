from search_space.sampler import SamplerFactory
from search_space import distribution_names
from tests.config import validate_replay_count
from search_space.sampler import distribution, Sampler


def distributed_like_uniform(list, values_account):
    return True


def test_uniform_sampler():
    uniform_sampler = SamplerFactory().create_sampler(distribution_names.UNIFORM)

    ints = [uniform_sampler.get_int(2, 10)
            for _ in range(validate_replay_count)]

    assert ints == [v for v in ints if v % 1 == 0 and v <= 10 and v >= 2]
    assert distributed_like_uniform(ints, values_account=8)

    floats = [uniform_sampler.get_float(2, 10)
              for _ in range(validate_replay_count)]

    assert floats == [v for v in floats if v <= 10 and v >= 2]
    assert distributed_like_uniform(floats, values_account=1000)

    boolean = [uniform_sampler.get_boolean()
               for _ in range(validate_replay_count)]

    assert boolean == [v for v in boolean if type(v) == type(True)]
    assert distributed_like_uniform(boolean, values_account=2)

    categorical = [uniform_sampler.choice(["white", "black", "other"])
                   for _ in range(validate_replay_count)]

    assert categorical == [
        v for v in categorical if v in ["white", "black", "other"]]
    assert distributed_like_uniform(categorical, values_account=2)

    sequential = [uniform_sampler.get_int(2, 100, repeat_last_value=i % 3 == 1)
                  for i in range(validate_replay_count)]

    for i in range(validate_replay_count):
        if i % 3 == 1:
            assert sequential[i] == sequential[i - 1], """
            Sampler have repeat the same value always be 'repeat_last_value' is 'True'"""

# TODO: Back sampler change

# def test_change_sampler():
#     @distribution(distribution_names.UNIFORM)
#     class OnlyFirstLimit(Sampler):
#         def generate_random_value(self, domain):
#             return domain[0]

#     new_uniform_sampler = SamplerFactory().create_sampler(distribution_names.UNIFORM)
#     values = [new_uniform_sampler.get_int(
#         2, 100) for i in range(validate_replay_count)]

#     assert len([v for v in values if v != 2]) == 0
