import re
from diamond.handler.Handler import Handler
from libsaas.services import ducksboard
from libsaas.services.ducksboard import Ducksboard
from datetime import datetime, timedelta

__author__ = 'LevKatzav'


class DucksboardHandler(Handler):
    def __init__(self, config=None):
        super(DucksboardHandler, self).__init__(config)
        self.labels = {}
        self.labels_in_dashboard = set()
        self.api_key = self.config.get('api_key')
        self.sync_time = timedelta(minutes=int(self.config.get('sync_time_min', '5')))
        self.labels_file_name =  self.config.get('labels_file_name', '/tmp/diamond_labels.log')
        self.last_sync_time = None
        self.ducksboard = Ducksboard(self.api_key, '')
        self.log.info('started DucksboardHandler')
        self._sync_labels()

    def _get_label(self, path):
        return path.lower()

    def _sync_labels(self):
        # get all the widgets so that only the needed labels will be sent
        widgets = self.ducksboard.widgets().get()
        old_labels_in_dashboard = self.labels_in_dashboard
        self.labels_in_dashboard = set()
        for widget in [x for x in widgets['data']]:
            wid = widget['widget']['id']
            update_widget = False
            for slot in widget['slots'].values():
                label = slot['label']
                self.labels_in_dashboard.add(label)
                subtitle = slot.get('subtitle', '')
                if re.match(r'label\d+', subtitle):
                    slot['subtitle'] = label
                    update_widget = True
            if update_widget:
                self.ducksboard.widget(wid).update(widget)

        # the labels in the dashboard has changed
        if old_labels_in_dashboard != self.labels_in_dashboard:
            self.log.info('labels_in_dashboard has been updated')
            self.labels = {}  # so that the labels log will be created again
            self.last_sync_time = datetime.now()



    def process(self, metric):
        if datetime.now() > self.last_sync_time + self.sync_time:
            self._sync_labels()
        label = self._get_label(metric.path)
        # generate a list of all the labels
        if label not in self.labels:
            self.labels[label] = [metric.value, False]  # (value, is_in_dashboard)
        if label not in self.labels_in_dashboard:
            return
        try:
            data = {
                "value": metric.value
            }
            source = self.ducksboard.data_source(label)
            res = source.push(data)
            if not self.labels[label][1]:
                self.labels[label][1] = True
                with open(self.labels_file_name, 'w') as f:
                    sorted_labels = sorted([(label, value, is_in_dashboard) for (label, [value, is_in_dashboard]) in self.labels.iteritems()])
                    lines = ['{0} {1}\t#{2}'.format(('*' if is_in_dashboard else ' '), label, value) for (label, value, is_in_dashboard) in sorted_labels]

                    f.writelines('\n'.join(lines))
        except Exception:
            self.log.exception('{0}: {1}'.format(label,data))