BEGIN TRANSACTION;
DROP TABLE IF EXISTS KluisjesRV;
CREATE TABLE IF NOT EXISTS KluisjesRV (
id serial PRIMARY KEY,
	Kluisnummer	TEXT,
	Naamvoluit	TEXT,
	Geslacht	TEXT,
	stopdatlid	TEXT,
	email	TEXT,
	userid	TEXT,
	kluisje	TEXT,
	kastje	TEXT
);



INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,Stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 01','Rinske Krabbe','Vrouw',NULL,'r.krabbe@hetnet.nl','279',1,'rinskekrabbe');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 04','Annemieke Rensink','Vrouw',NULL,'aamrensink@gmail.com','44',1,'annemiekerensink');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 05','Annemarie van der Burg','Vrouw',NULL,'cmeermin@airpost.net','280',1,'annemarievanderburg');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 07','Vivian van der Kuil','Vrouw',NULL,'vvanderkuil@me.com','281',1,'vivianvanderkuil');COMMIT;
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 08','Wyke Ruedisulj','Vrouw',NULL,'wyki24@gmail.com','282',1,'wykeruedisulj');COMMIT;
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 09','Petra de Leede','Vrouw',NULL,'petradeleede@gmail.com','283',1,'petradeleede');COMMIT;
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 12','Froukje Euwe','Vrouw',NULL,'f_euwe@hotmail.com','284',1,'froukjeeuwe');COMMIT;
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 13','Miranda Rovers','Vrouw',NULL,'miranda@miraud.nl','285',1,'mirandarovers');COMMIT;
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 14','Mimi Bröker-van Dongen','Vrouw',NULL,'w.brokervandongen@upcmail.nl','95',1,'mimibrökervandongen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 15','Maaike van Gulik-Rijlaarsdam','Vrouw',NULL,'maaike@vangulik.org','286',1,'maaikevangulikrijlaarsdam');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 16','Lia Kaboord-Bartels','Vrouw',NULL,'lkaboord@kpnmail.nl','287',1,'liakaboordbartels');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 19','Nadine van Wijk','Vrouw',NULL,'nadinevanwijk@gmail.com','288',1,'nadinevanwijk');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 20','Ellen Beverdam','Vrouw',NULL,'ebeverdam@xs4all.nl','94',1,'ellenbeverdam');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 21','Natalie Cappaert','Vrouw',NULL,'n.l.m.cappaert@gmail.com','289',1,'nataliecappaert');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 23','Birgitte Aertssen','Vrouw',NULL,'birgitte.aertssen@gmail.com','290',1,'birgitteaertssen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames 24','Willemijn Sprangers','Vrouw',NULL,'willemijnsprangers@gmail.com','291',1,'willemijnsprangers');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-25','Talitha van den Elst','Vrouw',NULL,'t.elst@wxs.nl','97',1,'talithavandenelst');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-26','Harmke van Dam','Vrouw',NULL,'stapvdam@xs4all.nl','278',1,'harmkevandam');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-27','Anouk Rijs','Vrouw',NULL,'anoukrijs@hotmail.com','41',1,'anoukrijs');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-31','Miranda Megens','Vrouw',NULL,'miranda_megens@yahoo.com','292',1,'mirandamegens');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-32','Jessica van der Leij','Vrouw',NULL,'jessica@ambeleij.demon.nl','59',1,'jessicavanderleij');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-35','Marina Tap-Hauer','Vrouw',NULL,'fhtap@xs4all.nl','293',1,'marinatap-hauer');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-36','Shanti Haazer','Vrouw',NULL,'haazer@zonnet.nl','252',1,'shantihaazer');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-38','Ineke van der Heide','Vrouw',NULL,'Gbvanderheide@hetnet.nl','294',1,'inekevanderheide');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-41','Lieske de Nooij','Vrouw',NULL,'linooij@gmail.com','82',1,'lieskedenooij');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-42',NULL,NULL,NULL,'info@mantis.nl','279','vrij','leeg');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-43','Diana de Rijk','Vrouw',NULL,'derijkdiana@gmail.com','295',1,'dianaderijk');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-44','Ria Gorsira-de Voogd','Vrouw',NULL,'h.r.geusebroek@gmail.com','107',1,'riagorsira-devoogd');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-45','Marian van Leeuwen-Scheltema','Vrouw',NULL,'marianscheltema@gmail.com','277',1,'marianvanleeuwenscheltema');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-46',NULL,NULL,NULL,'info@mantis.nl','279','vrij','leeg');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames A-48','Anneke Kuhurima','Vrouw',NULL,'anjotona@hotmail.com','249',1,'annekekuhurima');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-25','Nieske Heerema','Vrouw',NULL,'nc.heerema@gmail.com','58',1,'nieskeheerema');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-26','Janneke Nap','Vrouw',NULL,'nap.janneke@gmail.com','245',1,'jannekenap');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-27','Gerda Kwantes-Taams','Vrouw',NULL,'gerdakwantes@gmail.com','296',1,'gerdakwantestaams');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-28','Carolien Appeldoorn-de Lange','Vrouw',NULL,'carappeldoorn@ziggo.nl','98',1,'carolienappeldoorndelange');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-29','Carolina Scheepstra','Vrouw',NULL,'carolina.scheepstra@inholland.nl','297',1,'carolinascheepstra');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-30','Bente Scheffer','Vrouw',NULL,'bente.scheffer@xs4all.nl','298',1,'bentescheffer');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-31','Katja Moison','Vrouw',NULL,'catharina.moison@gmail.com','299',1,'katjamoison');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-32',NULL,NULL,NULL,'info@mantis.nl','279','vrij','leeg');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-33','Ellis Baaijen','Vrouw',NULL,'baaijen@ziggo.nl','92',1,'ellisbaaijen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-34','Elfi de Jong','Vrouw',NULL,'elluf@hotmail.com','300',1,'elfidejong');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-35','Leny Smit','Vrouw',NULL,'LSmit1@Xs4all.nl','301',1,'lenysmit');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-38','Marijke van Kuilenburg-le Maitre','Vrouw',NULL,'maryke@casema.nl','302',1,'marijkevankuilenburglemaitre');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-39','Ieke Schiferli','Vrouw',NULL,'iekeschiferli27@gmail.com','303',1,'iekeschiferli');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-40','Paulien Lasterie','Vrouw',NULL,'paulienlasterie@gmail.com','3',1,'paulienlasterie');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-41','Jeannette de Groot','Vrouw',NULL,'jce.groot@casema.nl','304',1,'jeannettedegroot');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-44','Marjolein Schepel','Vrouw',NULL,'marjolein@schepeladvies.nl','56',1,'marjoleinschepel');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames B-45','Coco Wessel','Vrouw',NULL,'corien@dapnijkerk.nl','103',1,'cocowessel');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-51','Mira van der Mije','Vrouw',NULL,'mail2mira@yahoo.com','90',1,'miravandermije');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-54','Inge Haas','Vrouw',NULL,'smorgens2@gmail.com','305',1,'ingehaas');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames c-56','Kluisjesbeheer','Vrouw','(nu Inge Loes)','ingeloes@gmail.com','306',1,'kluisjesbeheer');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-57','Wilma Hanskamp','Vrouw',NULL,'wilmahanskamp@hotmail.com','307',NULL,'wilmahanskamp');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-59','Teau de Vos van Steenwijk','Vrouw',NULL,'teaudevosvansteenwijk@gmail.com','308',1,'teaudevosvansteenwijk');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-61','Manon Burger','Vrouw',NULL,'manonburger1@gmail.com','309',1,'manonburger');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-62','Leonie van Bommel','Vrouw',NULL,'leonievb1@gmail.com','310',1,'leonievanbommel');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-64','Petra Gerritsen','Vrouw',NULL,'petra.gerritsen@spletters.nl','311',1,'petragerritsen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-65','Meta Rijks','Vrouw',NULL,'mhrijks@planet.nl','251',1,'metarijks');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-68','Gerda Kruithof','Vrouw',NULL,'gerdakruithof@icloud.com','312',1,'gerdakruithof');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-69','Ellen van Dun','Vrouw',NULL,'ellenvandun@casema.nl','313',1,'ellenvandun');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-70','Henny Sinnema','Vrouw',NULL,'hl.sinlan@t-mobilethuis.nl','314',1,'hennysinnema');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Dames C-71','Ank Meyer','Vrouw',NULL,'ankmeyer@xs4all.nl','315',NULL,'ankmeyer');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 01','Rik Vos','Man',NULL,'rikderoodevos@kpnmail.nl','160',NULL,'rikvos');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 02','Willie Ambergen','Man',NULL,'willie@ambeleij.demon.nl','153',NULL,'willieambergen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 03','Leo van den Broek','Man',NULL,'leovandenbroek@casema.nl','156',NULL,'leovandenbroek');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 04','Cor Scheffers','Man',NULL,'cor@corscheffers.nl','155',NULL,'corscheffers');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 05',NULL,NULL,NULL,'info@mantis.nl','279',NULL,'leeg');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 06','Edwin Foppen','Man',NULL,'edwin.foppen@gmail.com','316',NULL,'edwinfoppen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 07','Hans van Wijk','Man',NULL,'joh.vanwijk@ziggo.nl','317',NULL,'hansvanwijk');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 08','Sjoerd Hagedoorn','Man',NULL,'sjoerdhagedoorn@gmail.com','12',NULL,'sjoerdhagedoorn');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 09','Pepijn Reyn','Man',NULL,'pepijn.reyn@clz.nl','318',NULL,'pepijnreyn');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 10','Wim Gorissen','Man',NULL,'whmgorissen@gmail.com','78',NULL,'wimgorissen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 11','Tijmen van Gulik','Man',NULL,'tijmen@vangulik.org','319',NULL,'tijmenvangulik');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 12','Jean-François Raysz','Man',NULL,'rayszjf@hotmail.com','320',NULL,'jean-françoisraysz');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 13','Hugo Linnenbank','Man',NULL,'hugo@linnenbank.org','321',NULL,'hugolinnenbank');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 14','Jeroen Bollen','Man',NULL,'roeien@jeroenbollen.nl','260',NULL,'jeroenbollen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 16','Peter Prak','Man',NULL,'peter.prak@me.com','322',NULL,'peterprak');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 19','Eric Bak','Man',NULL,'ecr.bak@online.nl','323',NULL,'ericbak');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 20','Theo Brok','Man',NULL,'Tamerlan@xs4all.nl','324',NULL,'theobrok');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 21','Jurjen Kolmer','Man',NULL,'jurjen@kolmerweb.nl','325',NULL,'jurjenkolmer');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 22','Peter Hingstman','Man',NULL,'p.hingstman@hccnet.nl','326',NULL,'peterhingstman');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 23','Theo Visser','Man',NULL,'thmm.visser@ziggo.nl','206',NULL,'theovisser');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 24','Gertjan Miedema','Man',NULL,'gertjan@miedemageluid.nl','272',NULL,'gertjanmiedema');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 25','Laurens van der Duijs','Man',NULL,'laurensd007@gmail.com','327',1,'laurensvanderduijs');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 26','Martin Reniers','Man',NULL,'martinreniers@hotmail.com','328',NULL,'martinreniers');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 27','Pieter Kwantes','Man',NULL,'p.kwantes@ziggo.nl','149',NULL,'pieterkwantes');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 29','Gerard Ranke','Man',NULL,'gerard.ranke@ziggo.nl','329',NULL,'gerardranke');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 30','Peter-Jan Tuk','Man',NULL,'goldtuk@telfort.nl','262',NULL,'peter-jantuk');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 32','Jan Karel Tombrock','Man',NULL,'JTombrock@ziggo.nl','330',NULL,'jankareltombrock');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 33','Dick Baars','Man',NULL,'dickbaars@kpnplanet.nl','268',NULL,'dickbaars');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 35','Joan Schmidt','Man',NULL,'joannemieke@kpnmail.nl','331',NULL,'joanschmidt');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 37','Jeroen Paco Heydendael','Man',NULL,'paco@redleafs.nl','48',NULL,'jeroenpacoheydendael');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 38','Marcel Linssen','Man',NULL,'linssentandarts@gmail.com','332',NULL,'marcellinssen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 39','Henk Jan Kiewiet','Man',NULL,'H.j.kiewiet@hccnet.nl','333',NULL,'henkjankiewiet');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 40','Wim van de Bosch','Man',NULL,'w.vandenbosch@planet.nl','201',NULL,'wimvandebosch');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 41','Peter Knappstein','Man',NULL,'peterknappstein@seilemaaker.nl','334',NULL,'peterknappstein');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 42','Erik van der Struijs','Man',NULL,'erikvanderstruijs@xs4all.nl','253',NULL,'erikvanderstruijs');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 43','Bert Appeldoorn','Man',NULL,'bertappeldoorn@ziggo.nl','151',NULL,'bertappeldoorn');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 44','Stevin-Jan van Duijn','Man',NULL,'sjduijn@yahoo.com','26',NULL,'stevin-janvanduijn');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 45','Harold Thijssen','Man',NULL,'Haroldthijssen@hetnet.nl','261',NULL,'haroldthijssen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 47','Simon Glazenborg','Man',NULL,'simon.glazenborg@gmail.com','10',NULL,'simonglazenborg');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 48','Tomas Klos','Man',NULL,'tomasklos@gmail.com','335',NULL,'tomasklos');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 51','Hilco Bekenkamp','Man',NULL,'hbekenkamp-viking@casema.nl','336',NULL,'hilcobekenkamp');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 52','Wim de Groot','Man',NULL,'whdgroot@gmail.com','337',NULL,'wimdegroot');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 53','Kees Wierenga','Man',NULL,'c.wierenga@ziggo.nl','24',NULL,'keeswierenga');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 55','André van Dort','Man',NULL,'avdort@gmail.com','80',NULL,'andrévandort');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 56','Carel Reuser','Man',NULL,'cmreuser@yahoo.com','159',1,'carelreuser');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 57','Edwin Ongkosuwito','Man',NULL,'eongko@yahoo.com','338',NULL,'edwinongkosuwito');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 58','Peter Kerkhoven','Man',NULL,'peter.m.kerkhoven@gmail.com','339',NULL,'peterkerkhoven');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 59','Wessel Goossens','Man',NULL,'wessel.goossens@gmail.com','340',NULL,'wesselgoossens');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 61','Frannie van Essen','Man',NULL,'essen-van@ziggo.nl','341',NULL,'frannievanessen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 63','Martin Noorbergen','Man',NULL,'martinwileenbiertje@hotmail.com','342',NULL,'martinnoorbergen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 64','Bert van Manen','Man',NULL,'info@vanmanen.biz','264',NULL,'bertvanmanen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 65','Gerard van Bruggen','Man',NULL,'gerardvanbruggen64@hetnet.nl','343',NULL,'gerardvanbruggen');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 67','Robert ten Voorde','Man',NULL,'rtenvoorde@datelvision.nl','344',NULL,'roberttenvoorde');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 69','Dick Busscher','Man',NULL,'die123@casema.nl','207',NULL,'dickbusscher');
INSERT INTO KluisjesRV (Kluisnummer,Naamvoluit,Geslacht,stopdatlid,email,userid,kluisje,kastje) VALUES ('Heren 70','Gerard Langeveld','Man',NULL,'gelangeveld@gmail.com','345',NULL,'gerardlangeveld');
COMMIT;
