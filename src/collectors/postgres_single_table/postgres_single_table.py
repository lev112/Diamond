from postgres import *
# from psycopg2._psycopg import ProgrammingError

__author__ = 'Lev'

registry['extended'] = (
    DatabaseStats,
    DatabaseConnectionCount,
    UserTableStats,
    UserIndexStats,
    UserTableIOStats,
    UserIndexIOStats,
    ConnectionStateStats,
    LockStats,
    RelationSizeStats,
    BackgroundWriterStats,
    # WalSegmentStats,
    TransactionCount,
    IdleInTransactions,
    LongestRunningQueries,
    UserConnectionCount,
    TableScanStats,
    TupleAccessStats,
)




class PostgresqlSingleDbCollector(PostgresqlCollector):
    def get_default_config_help(self):
        config_help = super(PostgresqlSingleDbCollector, self).get_default_config_help()
        config_help.update({
            'database': 'Database to take statistics on'
        })
        return config_help

    def get_default_config(self):
        """
        Return default config.
        """
        config = super(PostgresqlSingleDbCollector, self).get_default_config()
        config.update({
            'database': None,
        })
        return config

    def _get_db_names(self):
        database = self.config['database']
        if database:
            return [database]
        else:
            return super(PostgresqlSingleDbCollector, self)._get_db_names()
