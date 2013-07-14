from diskspace import DiskSpaceCollector
from diamond.post_collect_mixin import PostCollectMixin

__author__ = 'Lev'


class DiskSpacePostCollector(PostCollectMixin, DiskSpaceCollector):
    pass


