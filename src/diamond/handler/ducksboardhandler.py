import re
from diamond.handler.Handler import Handler
from libsaas.services import ducksboard
from libsaas.services.ducksboard import Ducksboard


__author__ = 'LevKatzav'


class DucksboardHandler(Handler):
    def __init__(self, config=None):
        super(DucksboardHandler, self).__init__(config)
        self.labels = set()
        self.api_key = self.config.get('api_key')
        self.ducksboard = Ducksboard(self.api_key,'')
        self.log.info('started DucksboardHandler')

        widgets = self.ducksboard.widgets().get()
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

    def _get_label(self, path):
        return path.lower()


    def process(self, metric):
        # self.log.info('####################')
        label = self._get_label(metric.path)
        if label not in self.labels:
            self.labels.add(label)
            with open('/tmp/diamond_labels.log', 'w') as f:
                sorted_labels = sorted([label for label in self.labels])
                lines = ['{0} {1}'.format(('*' if label in self.labels_in_dashboard else ' '), label) for label in sorted_labels]

                f.writelines('\n'.join(lines))
            # data = {
            #     "value": {"board": [{"name": l, "values": ['Fire']} for l in self.labels]
            #
            #     }
            # }
            # info_source = self.ducksboard.data_source('info')
            # res = info_source.push(data)
            # self.log.info('{0} - {1}'.format(res,data))
        if label not in self.labels_in_dashboard:
            return
        try:
            source = self.ducksboard.data_source(label)
            data = {
                "value": metric.value
            }
            res = source.push(data)
        except:
            self.log.exception('######## {0}: {1}'.format(label,data))
        # self.log.info('{0} - {1}'.format(res, data))