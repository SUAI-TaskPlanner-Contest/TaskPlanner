from Code.entities.db_entities import DbServer
from Code.entities.domain_entities import Server as DomainServer


def from_db_to_domain_server(db_server):
    return DomainServer(
        id=db_server.id,
        user_email=db_server.user_email,
        user_password=db_server.user_password,
        server_uri=db_server.server_uri,
        server_name=db_server.server_name,
        calendar_name=db_server.calendar_name,
        statuses=db_server.statuses,
        priorities=db_server.priorities,
        sizes=db_server.sizes,
        types=db_server.types,
        tasks=db_server.tasks
    )


def from_domain_to_db_server(domain_server):
    return DbServer(

    )