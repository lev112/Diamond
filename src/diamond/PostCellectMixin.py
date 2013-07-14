__author__ = 'Lev'


class PostCollectMixin(object):
    eval_globals = {
        '__builtins__': None
    }

    def __init__(self, *args, **kw):
        super(PostCollectMixin, self).__init__(*args, **kw)
        # the config should be in the form 'name1:val1+val2; name2:(val3+val4)/val5; ...'
        actions = [line.split(':', 1) for line in self.config['post_collections'].split(';') if line.strip()]
        self.post_collections = {name.strip(): exp for name, exp in actions}


    def get_default_config_help(self):
        config_help = super(PostCollectMixin, self).get_default_config_help()
        config_help.update({
            'post_collections':  'how to collect metrics the are composed of other metrics',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PostCollectMixin, self).get_default_config()
        config.update({
           'post_collections':  '',
        })
        return config

    def collect(self):
        self.collected_metrics = {}
        super(PostCollectMixin, self).collect()
        for name, exp in self.post_collections.iteritems():
            value = eval(exp, self.eval_globals, self.collected_metrics)
            super(PostCollectMixin, self).publish(name=name, value=value)


    def publish(self, name, value, *args, **kw):
        self.collected_metrics[name] = value
        super(PostCollectMixin, self).publish(name=name, value=value, *args, **kw)
