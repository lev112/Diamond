from postgres import *
# from psycopg2._psycopg import ProgrammingError

__author__ = 'Lev'


class DatabaseStatsRDS(DatabaseStats):
    """
    Database-level summary stats
    ignore the rdsadmin table as well
    """
    query = """
        SELECT pg_stat_database.datname as datname,
               pg_stat_database.numbackends as numbackends,
               pg_stat_database.xact_commit as xact_commit,
               pg_stat_database.xact_rollback as xact_rollback,
               pg_stat_database.blks_read as blks_read,
               pg_stat_database.blks_hit as blks_hit,
               pg_stat_database.tup_returned as tup_returned,
               pg_stat_database.tup_fetched as tup_fetched,
               pg_stat_database.tup_inserted as tup_inserted,
               pg_stat_database.tup_updated as tup_updated,
               pg_stat_database.tup_deleted as tup_deleted,
               pg_database_size(pg_database.datname) AS size
        FROM pg_database
        JOIN pg_stat_database
        ON pg_database.datname = pg_stat_database.datname
        WHERE pg_stat_database.datname
        NOT IN ('template0','template1','postgres','rdsadmin')
    """
registry['extended'] = (
    DatabaseStatsRDS,
    DatabaseConnectionCount,
    UserTableStats,
    UserIndexStats,
    UserTableIOStats,
    UserIndexIOStats,
    # ConnectionStateStats,
    LockStats,
    RelationSizeStats,
    BackgroundWriterStats,
    # WalSegmentStats,
    TransactionCount,
    # IdleInTransactions,
    # LongestRunningQueries,
    # UserConnectionCount,
    TableScanStats,
    TupleAccessStats,
)

registry['basic']= (
        DatabaseStatsRDS,
        DatabaseConnectionCount,
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
