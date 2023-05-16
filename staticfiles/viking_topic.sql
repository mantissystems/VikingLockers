BEGIN TRANSACTION;
DROP TABLE IF EXISTS "viking_topic";
CREATE TABLE IF NOT EXISTS "viking_topic" (
	"id"	integer NOT NULL,
	"name"	varchar(200) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "viking_topic" ("id","name") VALUES (3,'Kluisjes-leeg');
INSERT INTO "viking_topic" ("id","name") VALUES (9,'Met Kluis');
INSERT INTO "viking_topic" ("id","name") VALUES (10,'Wachtlijst');
INSERT INTO "viking_topic" ("id","name") VALUES (11,'Aanvraag');
COMMIT;
