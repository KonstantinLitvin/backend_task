import dataclasses
import datetime as dt
import json
import random
import string
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Comment:
    id: int
    post_id: int
    title: str
    date: str
    comment: str

    def __ge__(self, other):
        return self.date >= other.date

    def __le__(self, other):
        return self.date <= other.date

    def __lt__(self, other):
        return self.date < other.date

    def is_alive(self, time_iso: str):
        return self.date <= time_iso


@dataclass
class Post:
    id: int
    title: str
    date: str
    body: str
    deleted: bool

    def __ge__(self, other):
        return self.date >= other.date

    def __le__(self, other):
        return self.date <= other.date

    def __lt__(self, other):
        return self.date < other.date

    def is_alive(self, time_iso: str):
        return self.date <= time_iso

    def is_deleted(self):
        return self.deleted


class SampleGenerator:
    def __init__(self):
        self.rand_list = random.sample(range(1, 10001), 1000)

    def get_random_comment(self):
        return Comment(self.get_unique_random_int(),
                       self.get_unique_random_int(),
                       self.get_random_string(),
                       SampleGenerator.get_random_date(),
                       self.get_random_string())

    def get_random_post(self):
        return Post(self.get_unique_random_int(),
                    self.get_random_string(),
                    self.get_random_date(),
                    self.get_random_string(),
                    self.get_random_bool())

    @staticmethod
    def get_random_bool():
        return random.choice([True, False])

    @staticmethod
    def get_random_string(k=10):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))

    def get_unique_random_int(self):
        return self.rand_list.pop()

    @staticmethod
    def get_random_date(start=dt.datetime.strptime('2018-06-29T08:15:27', '%Y-%m-%dT%H:%M:%S'),
                        end=dt.datetime.strptime('2020-12-29T08:15:27', '%Y-%m-%dT%H:%M:%S')):
        """random str iso format datetime"""
        return (start + dt.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))).isoformat()

    def dump_random_comments(self, file_name, n=1000):
        comments = [dataclasses.asdict(self.get_random_comment()) for _ in range(n)]
        with open(Path('data', file_name), 'w') as f:
            json.dump({'comments': comments}, f, indent=1)

    def dump_random_posts(self, file_name, n=1000):
        comments = [dataclasses.asdict(self.get_random_post()) for _ in range(n)]
        with open(Path('data', file_name), 'w') as f:
            json.dump({'posts': comments}, f, indent=1)


def get_current_time_iso():
    return dt.datetime.now().replace(microsecond=0).isoformat()


def generate():
    SampleGenerator().dump_random_comments('comments_1.json', 100)
    SampleGenerator().dump_random_posts('posts_1.json', 100)


if __name__ == '__main__':
    generate()
