from utils import SampleGenerator


def test_1():
    g = SampleGenerator()
    posts = [g.get_random_post() for _ in range(100)]
    return posts

