-- realtimebi.Auto definition

CREATE TABLE `Auto` (
  `Auto_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Typ` varchar(100) NOT NULL,
  `Batterie` varchar(100) NOT NULL,
  `Innenraum` varchar(100) NOT NULL,
  `Farbe` varchar(100) NOT NULL,
  `AutoFahren` varchar(100) NOT NULL,
  `Status` int(11) DEFAULT NULL,
  `Wert` float DEFAULT 0,
  `ProdTimestmp` datetime DEFAULT NULL,
  `BeginnProdTime` datetime DEFAULT NULL,
  `Produktionsstrasse` int(11) DEFAULT NULL,
  PRIMARY KEY (`Auto_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=217 DEFAULT CHARSET=utf8;


-- realtimebi.Lager definition

CREATE TABLE `Lager` (
  `LagerID` int(11) NOT NULL AUTO_INCREMENT,
  `Status` float NOT NULL,
  `Kapazität` int(11) NOT NULL,
  PRIMARY KEY (`LagerID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


-- realtimebi.Bestellung definition

CREATE TABLE `Bestellung` (
  `Bestellung_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Typ` varchar(100) NOT NULL,
  `Batterie` varchar(100) NOT NULL,
  `Innenraum` varchar(100) NOT NULL,
  `Farbe` varchar(100) NOT NULL,
  `Eingang` datetime NOT NULL,
  `AutoFahren` varchar(100) NOT NULL,
  `Preis` int(11) NOT NULL,
  `Auto_ID` int(11) DEFAULT NULL,
  `Ausgang` datetime DEFAULT NULL,
  PRIMARY KEY (`Bestellung_ID`),
  KEY `Bestellung_FK` (`Auto_ID`),
  CONSTRAINT `Bestellung_FK` FOREIGN KEY (`Auto_ID`) REFERENCES `Auto` (`Auto_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=783 DEFAULT CHARSET=utf8;


-- realtimebi.Komponente definition

CREATE TABLE `Komponente` (
  `KompID` int(11) NOT NULL AUTO_INCREMENT,
  `Typ` varchar(100) NOT NULL,
  `Ausfuehrung` varchar(100) NOT NULL,
  `Preis` int(11) NOT NULL,
  `Auto_ID` int(11) DEFAULT NULL,
  `Einbau` datetime DEFAULT NULL,
  `Eingang` datetime NOT NULL,
  `LagerID` int(11) DEFAULT NULL,
  PRIMARY KEY (`KompID`),
  KEY `Komponente_FK` (`Auto_ID`),
  KEY `Komponente_FK_1` (`LagerID`),
  CONSTRAINT `Komponente_FK` FOREIGN KEY (`Auto_ID`) REFERENCES `Auto` (`Auto_ID`),
  CONSTRAINT `Komponente_FK_1` FOREIGN KEY (`LagerID`) REFERENCES `Lager` (`LagerID`)
) ENGINE=InnoDB AUTO_INCREMENT=932 DEFAULT CHARSET=utf8;


-- realtimebi.Lager_Auto definition

CREATE TABLE `Lager_Auto` (
  `Auto_ID` int(11) NOT NULL,
  `LagerID` int(11) NOT NULL DEFAULT 1,
  `LagertSeit` datetime NOT NULL,
  PRIMARY KEY (`Auto_ID`,`LagerID`),
  KEY `Lager_Auto_FK_1` (`LagerID`),
  CONSTRAINT `Lager_Auto_FK` FOREIGN KEY (`Auto_ID`) REFERENCES `Auto` (`Auto_ID`),
  CONSTRAINT `Lager_Auto_FK_1` FOREIGN KEY (`LagerID`) REFERENCES `Lager` (`LagerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- realtimebi.Maschine definition

CREATE TABLE `Maschine` (
  `MaschinenID` int(11) NOT NULL AUTO_INCREMENT,
  `Status` varchar(100) NOT NULL,
  `Produktivitaet` int(11) NOT NULL DEFAULT 100,
  `Bearbeitungszeit` int(11) NOT NULL,
  `Auto_ID` int(11) DEFAULT NULL,
  `Strasse` int(11) NOT NULL,
  `Position` int(11) NOT NULL,
  PRIMARY KEY (`MaschinenID`),
  KEY `Maschine_FK` (`Auto_ID`),
  CONSTRAINT `Maschine_FK` FOREIGN KEY (`Auto_ID`) REFERENCES `Auto` (`Auto_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


-- realtimebi.ProduktivitaetVerlauf_Maschine definition

CREATE TABLE `ProduktivitaetVerlauf_Maschine` (
  `MaschinenID` int(11) NOT NULL,
  `Timestmp` datetime NOT NULL,
  `Produktivitaet` int(11) NOT NULL DEFAULT 100,
  PRIMARY KEY (`MaschinenID`,`Timestmp`),
  CONSTRAINT `ProduktivitätVerlauf_Maschine_FK` FOREIGN KEY (`MaschinenID`) REFERENCES `Maschine` (`MaschinenID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- realtimebi.StatusVerlauf_Maschine definition

CREATE TABLE `StatusVerlauf_Maschine` (
  `MaschinenID` int(11) NOT NULL,
  `Timestmp` datetime NOT NULL,
  `Status` varchar(100) NOT NULL,
  PRIMARY KEY (`MaschinenID`,`Timestmp`),
  CONSTRAINT `NewTable_FK` FOREIGN KEY (`MaschinenID`) REFERENCES `Maschine` (`MaschinenID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- realtimebi.Auslastung_Maschine definition

CREATE TABLE `Auslastung_Maschine` (
  `MaschinenID` int(11) NOT NULL,
  `Nutzung` tinyint(1) NOT NULL,
  `Timestmp` datetime NOT NULL,
  `Dauer` int(11) NOT NULL DEFAULT 0,
  `Auslastung` float NOT NULL,
  PRIMARY KEY (`MaschinenID`,`Timestmp`),
  CONSTRAINT `Auslasung_Maschine_FK` FOREIGN KEY (`MaschinenID`) REFERENCES `Maschine` (`MaschinenID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;