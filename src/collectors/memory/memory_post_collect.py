from memory import MemoryCollector
from diamond.post_collect_mixin import PostCollectMixin

__author__ = 'Lev'


class MemoryPostCollector(PostCollectMixin, MemoryCollector):
    pass


