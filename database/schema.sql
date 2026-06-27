CREATE TABLE tickets_ticket (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    number varchar(20) NOT NULL UNIQUE,
    full_name varchar(120) NOT NULL,
    email varchar(254) NOT NULL,
    enrollment varchar(30) NOT NULL,
    category varchar(40) NOT NULL,
    priority varchar(20) NOT NULL,
    subject varchar(160) NOT NULL,
    description text NOT NULL,
    status varchar(20) NOT NULL,
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL
);

CREATE TABLE tickets_ticketevent (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    title varchar(120) NOT NULL,
    note text NOT NULL,
    created_at datetime NOT NULL,
    ticket_id bigint NOT NULL REFERENCES tickets_ticket(id) DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX tickets_ticketevent_ticket_id_idx ON tickets_ticketevent(ticket_id);
