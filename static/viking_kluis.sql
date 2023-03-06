BEGIN TRANSACTION;
DROP TABLE IF EXISTS "viking_kluis";
CREATE TABLE IF NOT EXISTS "viking_kluis" (
	"id"	integer NOT NULL,
	"body"	text NOT NULL,
	"updated"	datetime NOT NULL,
	"created"	datetime NOT NULL,
	"user_id"	integer NOT NULL,
	"name"	varchar(200) NOT NULL,
	"location"	text,
	"slot"	varchar(18) NOT NULL,
	"sleutels"	integer NOT NULL,
	"code"	text,
	"topic_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("topic_id") REFERENCES "viking_topic"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (1,'Annemieke Rensink','2022-11-10 07:39:23.850804','2022-11-10 00:00:00',45,'Annemieke Rensink','Dames 04','V',44,'1',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (2,'Mimi Bröker-van Dongen','2022-11-10 07:38:02.892052','2022-11-09 00:00:00',96,'Mimi Bröker-van Dongen','Dames 14','V',95,'2',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (3,'Ellen Beverdam',0,'2022-11-09 00:00:00',95,'Ellen Beverdam','Dames 20','H',94,'3',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (4,'Talitha van den Elst',0,'2022-11-09 00:00:00',98,'Talitha van den Elst','Dames A-25','H',97,'4',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (5,'Harmke van Dam',0,'2022-11-09 00:00:00',279,'Harmke van Dam','Dames A-26','H',278,'5',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (6,'Anouk Rijs',0,'2022-11-09 00:00:00',42,'Anouk Rijs','Dames A-27','H',41,'6',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (7,'Jessica van der Leij',0,'2022-11-09 00:00:00',60,'Jessica van der Leij','Dames A-32','H',59,'7',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (8,'Shanti Haazer',0,'2022-11-09 00:00:00',253,'Shanti Haazer','Dames A-36','H',252,'8',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (9,'Lieske de Nooij',0,'2022-11-09 00:00:00',83,'Lieske de Nooij','Dames A-41','H',82,'9',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (10,'Ria Gorsira-de Voogd',0,'2022-11-09 00:00:00',108,'Ria Gorsira-de Voogd','Dames A-44','H',107,'10',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (11,'Marian van Leeuwen-Scheltema',0,'2022-11-09 00:00:00',278,'Marian van Leeuwen-Scheltema','Dames A-45','H',277,'11',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (12,'Anneke Kuhurima',0,'2022-11-09 00:00:00',250,'Anneke Kuhurima','Dames A-48','H',249,'12',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (13,'Nieske Heerema',0,'2022-11-09 00:00:00',59,'Nieske Heerema','Dames B-25','H',58,'13',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (14,'Janneke Nap',0,'2022-11-09 00:00:00',246,'Janneke Nap','Dames B-26','H',245,'14',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (15,'Carolien Appeldoorn-de Lange',0,'2022-11-09 00:00:00',99,'Carolien Appeldoorn-de Lange','Dames B-28','H',98,'15',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (16,'Ellis Baaijen',0,'2022-11-09 00:00:00',93,'Ellis Baaijen','Dames B-33','H',92,'16',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (17,'Paulien Lasterie',0,'2022-11-09 00:00:00',4,'Paulien Lasterie','Dames B-40','H',3,'17',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (18,'Marjolein Schepel',0,'2022-11-09 00:00:00',57,'Marjolein Schepel','Dames B-44','H',56,'18',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (19,'Coco Wessel',0,'2022-11-09 00:00:00',104,'Coco Wessel','Dames B-45','H',103,'19',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (20,'Mira van der Mije',0,'2022-11-09 00:00:00',91,'Mira van der Mije','Dames C-51','H',90,'20',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (21,'Meta Rijks',0,'2022-11-09 00:00:00',252,'Meta Rijks','Dames C-65','H',251,'21',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (22,'Rik Vos',0,'2022-11-09 00:00:00',161,'Rik Vos','Heren 01','H',160,'22',9);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (23,'Willie Ambergen',0,'2022-11-09 00:00:00',154,'Willie Ambergen','Heren 02','H',153,'23',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (24,'Leo van den Broek',0,'2022-11-09 00:00:00',157,'Leo van den Broek','Heren 03','H',156,'24',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (25,'Cor Scheffers',0,'2022-11-09 00:00:00',156,'Cor Scheffers','Heren 04','H',155,'25',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (26,'Sjoerd Hagedoorn',0,'2022-11-09 00:00:00',13,'Sjoerd Hagedoorn','Heren 08','H',12,'26',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (27,'Wim Gorissen',0,'2022-11-09 00:00:00',79,'Wim Gorissen','Heren 10','H',78,'27',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (28,'Jeroen Bollen',0,'2022-11-09 00:00:00',261,'Jeroen Bollen','Heren 14','H',260,'28',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (29,'Theo Visser',0,'2022-11-09 00:00:00',207,'Theo Visser','Heren 23','H',206,'29',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (30,'Gertjan Miedema',0,'2022-11-09 00:00:00',273,'Gertjan Miedema','Heren 24','H',272,'30',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (31,'Pieter Kwantes',0,'2022-11-09 00:00:00',150,'Pieter Kwantes','Heren 27','H',149,'31',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (32,'Peter-Jan Tuk',0,'2022-11-09 00:00:00',263,'Peter-Jan Tuk','Heren 30','H',262,'32',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (33,'Dick Baars',0,'2022-11-09 00:00:00',269,'Dick Baars','Heren 33','H',268,'33',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (34,'Jeroen Paco Heydendael',0,'2022-11-09 00:00:00',49,'Jeroen Paco Heydendael','Heren 37','H',48,'34',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (35,'Wim van de Bosch',0,'2022-11-09 00:00:00',202,'Wim van de Bosch','Heren 40','H',201,'35',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (36,'Erik van der Struijs',0,'2022-11-09 00:00:00',254,'Erik van der Struijs','Heren 42','H',253,'36',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (37,'Bert Appeldoorn',0,'2022-11-09 00:00:00',152,'Bert Appeldoorn','Heren 43','H',151,'37',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (38,'Stevin-Jan van Duijn',0,'2022-11-09 00:00:00',27,'Stevin-Jan van Duijn','Heren 44','H',26,'38',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (39,'Harold Thijssen',0,'2022-11-09 00:00:00',262,'Harold Thijssen','Heren 45','H',261,'39',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (40,'Simon Glazenborg',0,'2022-11-09 00:00:00',11,'Simon Glazenborg','Heren 47','H',10,'40',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (41,'Kees Wierenga',0,'2022-11-09 00:00:00',25,'Kees Wierenga','Heren 53','H',24,'41',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (42,'André van Dort',0,'2022-11-09 00:00:00',81,'André van Dort','Heren 55','H',80,'42',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (43,'Carel Reuser',0,'2022-11-09 00:00:00',160,'Carel Reuser','Heren 56','H',159,'43',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (44,'Bert van Manen',0,'2022-11-09 00:00:00',265,'Bert van Manen','Heren 64','H',264,'44',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (45,'Dick Busscher',0,'2022-11-09 00:00:00',208,'Dick Busscher','Heren 69','H',207,'45',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (46,'leeg','2022-12-16 13:13:47.010025','2022-11-09 00:00:00',1,'Dames 01','Dames 01','H',2,'46',3);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (47,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 05','H',2,'47',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (48,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 07','H',2,'48',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (49,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 08','H',2,'49',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (50,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 09','H',2,'50',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (51,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 12','H',2,'51',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (52,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 13','H',2,'52',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (53,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 15','H',2,'53',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (54,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 16','H',2,'54',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (55,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 19','H',2,'55',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (56,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 21','H',2,'56',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (57,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 23','H',2,'57',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (58,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames 24','H',2,'58',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (59,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames A-31','H',2,'59',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (60,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames A-35','H',2,'60',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (61,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames A-38','H',2,'61',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (62,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames A-42','H',2,'62',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (63,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames A-43','H',2,'63',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (64,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames A-46','H',2,'64',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (65,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames B-27','H',2,'65',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (66,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames B-29','H',2,'66',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (67,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames B-30','H',2,'67',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (68,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames B-31','H',2,'68',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (69,'leeg',0,'2022-11-09 00:00:00',1,'wb','Dames B-32','H',2,'69',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (70,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames B-34','H',2,'70',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (71,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames B-35','H',2,'71',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (72,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames B-38','H',2,'72',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (73,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames B-39','H',2,'73',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (74,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames B-41','H',2,'74',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (75,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames C-54','H',2,'75',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (76,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames c-56','H',2,'76',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (77,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames C-57','H',2,'77',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (78,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames C-59','H',2,'78',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (79,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames C-61','H',2,'79',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (80,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames C-62','H',2,'80',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (81,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames C-64','H',2,'81',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (82,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames C-68','H',2,'82',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (83,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames C-69','H',2,'83',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (84,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames C-70','H',2,'84',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (85,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Dames C-71','H',2,'85',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (86,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 05','H',2,'86',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (87,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 06','H',2,'87',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (88,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 07','H',2,'88',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (89,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 09','H',2,'89',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (90,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 11','H',2,'90',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (91,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 12','H',2,'91',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (92,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 13','H',2,'92',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (93,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 16','H',2,'93',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (94,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 19','H',2,'94',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (95,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 20','H',2,'95',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (96,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 21','H',2,'96',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (97,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 22','H',2,'97',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (98,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 25','H',2,'98',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (99,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 26','H',2,'99',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (100,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 29','H',2,'100',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (101,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 32','H',2,'101',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (102,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 35','H',2,'102',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (103,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 38','H',2,'103',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (104,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 39','H',2,'104',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (105,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 41','H',2,'105',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (106,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 48','H',2,'106',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (107,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 51','H',2,'107',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (108,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 52','H',2,'108',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (109,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 57','H',2,'109',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (110,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 58','H',2,'110',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (111,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 59','H',2,'111',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (112,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 61','H',2,'112',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (113,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 63','H',2,'113',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (114,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 65','H',2,'114',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (115,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 67','H',2,'115',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (116,'leeg',0,'2022-11-09 00:00:00',1,'leeg','Heren 70','H',2,'116',NULL);
INSERT INTO "viking_kluis" ("id","body","updated","created","user_id","name","location","slot","sleutels","code","topic_id") VALUES (117,'wachtlijst','2023-01-07 20:12:30.879445','2023-01-07 20:09:24.788377',1,'Wachtlijst','Wachtlijst','--',2,'117',3);
DROP INDEX IF EXISTS "viking_kluis_user_id_0659ee43";
CREATE INDEX IF NOT EXISTS "viking_kluis_user_id_0659ee43" ON "viking_kluis" (
	"user_id"
);
DROP INDEX IF EXISTS "viking_kluis_topic_id_e3d4b6e5";
CREATE INDEX IF NOT EXISTS "viking_kluis_topic_id_e3d4b6e5" ON "viking_kluis" (
	"topic_id"
);
COMMIT;
