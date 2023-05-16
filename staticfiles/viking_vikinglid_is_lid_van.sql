BEGIN TRANSACTION;
DROP TABLE IF EXISTS "viking_vikinglid_is_lid_van";
CREATE TABLE IF NOT EXISTS "viking_vikinglid_is_lid_van" (
	"id"	integer NOT NULL,
	"vikinglid_id"	bigint NOT NULL,
	"activiteit_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("activiteit_id") REFERENCES "viking_activiteit"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vikinglid_id") REFERENCES "viking_vikinglid"("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1668,41,6);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1669,59,7);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1670,252,8);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1671,82,9);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1672,107,10);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1673,277,11);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1674,249,12);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1675,58,13);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1676,245,14);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1677,98,15);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1678,92,16);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1680,56,18);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1681,103,19);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1682,90,20);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1683,251,21);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1684,160,22);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1685,153,23);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1686,156,24);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1687,155,25);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1688,12,26);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1689,78,27);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1690,260,28);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1691,206,29);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1692,272,30);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1693,149,31);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1694,262,32);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1695,268,33);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1696,48,34);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1697,201,35);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1698,253,36);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1699,151,37);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1700,26,38);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1701,261,39);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1702,10,40);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1703,24,41);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1704,80,42);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1705,159,43);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1706,264,44);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1707,207,45);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1910,44,2);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1925,278,9);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1969,121,117);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1974,324,95);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1979,95,2);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1980,94,3);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1981,97,4);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1982,278,5);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (1994,3,17);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (2114,189,117);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (2223,122,404);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (2224,122,35);
INSERT INTO "viking_vikinglid_is_lid_van" ("id","vikinglid_id","activiteit_id") VALUES (2238,405,404);
DROP INDEX IF EXISTS "viking_vikinglid_is_lid_van_vikinglid_id_activiteit_id_4d7c8a8d_uniq";
CREATE UNIQUE INDEX IF NOT EXISTS "viking_vikinglid_is_lid_van_vikinglid_id_activiteit_id_4d7c8a8d_uniq" ON "viking_vikinglid_is_lid_van" (
	"vikinglid_id",
	"activiteit_id"
);
DROP INDEX IF EXISTS "viking_vikinglid_is_lid_van_vikinglid_id_c2deceb7";
CREATE INDEX IF NOT EXISTS "viking_vikinglid_is_lid_van_vikinglid_id_c2deceb7" ON "viking_vikinglid_is_lid_van" (
	"vikinglid_id"
);
DROP INDEX IF EXISTS "viking_vikinglid_is_lid_van_activiteit_id_95864030";
CREATE INDEX IF NOT EXISTS "viking_vikinglid_is_lid_van_activiteit_id_95864030" ON "viking_vikinglid_is_lid_van" (
	"activiteit_id"
);
COMMIT;
