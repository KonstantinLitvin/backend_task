import dataclasses
import json
from collections import defaultdict
from pathlib import Path

from utils import Post, get_current_time_iso, Comment


class JsonStore:
    COMMENTS_FILE = 'comments_1.json'
    POST_FILE = 'posts_1.json'

    def __init__(self):
        self.posts = self._load_posts()
        self.comments = self._load_comments()

    def get(self):
        """
        returns:
        {
            "posts":
            [
                {
                    "id": 1,
                    "title": "post_1",
                    "date": "2019-01-01T20:56:35",
                    "body": "The post",
                    "comments_count": 1
                }
            ],
            "posts_count": 1
        }

        """
        posts = []
        post_n = 0
        t = get_current_time_iso()
        for post in self.posts.values():
            post: Post
            if post.is_deleted() or not post.is_alive(t):
                continue
            post_n += 1
            p = dataclasses.asdict(post)
            del p['deleted']
            p['comments_count'] = len(self.comments[post.id])
            posts.append(p)
        return {'posts': posts, "posts_count": post_n}

    def get_by_id(self, id_):
        post: Post
        post = self.posts.get(id_)
        t = get_current_time_iso()

        if post is not None and not post.deleted and post.is_alive(t):
            p = dataclasses.asdict(post)
            del p['deleted']
            comments = [dataclasses.asdict(c) for c in (self.comments.get(id_, [])) if c.is_alive(t)]
            p['comments'] = comments
            p['comments_count'] = len(comments)
            return p
        return None

    @staticmethod
    def read_json(file_name):
        with open(Path('data', file_name)) as f:
            return json.load(f)

    def _load_comments(self):
        comments = self.read_json(self.COMMENTS_FILE).get('comments')
        if comments is None:
            raise Exception(f'No comments key in {self.COMMENTS_FILE}')

        comments = sorted([Comment(**c) for c in comments])
        d = defaultdict(list)
        [d[c.post_id].append(c) for c in comments]
        return d

    def _load_posts(self):
        posts = self.read_json(self.POST_FILE).get('posts')
        if posts is None:
            raise Exception(f'No posts key in {self.POST_FILE}')

        posts = {p['id']: Post(**p) for p in posts}
        return {k: v for k, v in sorted(posts.items(), key=lambda item: item[1])}
