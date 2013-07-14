from diskspace import DiskSpaceCollector
from diamond.PostCollectMixin import PostCollectMixin

__author__ = 'Lev'


class DiskSpacePostCollector(PostCollectMixin, DiskSpaceCollector):
    pass


