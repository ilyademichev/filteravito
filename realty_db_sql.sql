CREATE DATABASE realty;

CREATE TABLE Company (
	  CompanyID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	  Cust INT ,
	  FOREIGN KEY (Cust)
      REFERENCES RealtyItem( RealtyID )
      CompanyName   TEXT NOT NULL ,
      );

CREATE TABLE  Rooms
    (
        RoomsID TINYINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        REFRealtyID INT ,
		FOREIGN KEY ( REFRealtyID )
		REFERENCES RealtyItem( RealtyID ),
        RoomDescription TEXT NOT NULL
    );

CREATE TABLE RealtyItem (
	  RealtyID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	  TimeRecorded INT NOT NULL, #врем
	  Phone TEXT NOT NULL ,#телефон
	  Floor TEXT NOT NULL ,#этаж
	  Address TEXT NOT NULL ,#адрес
	  State TEXT NOT NULL ,#актуальность
	  Area_flat TEXT NOT NULL ,#площадь обьекта
	  Area_land TEXT NOT NULL ,#площадь участка в сотка
	  Relevance TEXT NOT NULL#
	  Author TEXT NOT NULL,#автор
	  Price SMALLINT NOT NULL, #цена
	  ApplicationDate DATE NOT NULL,# дата подачи
	  CallDate DATE NOT NULL,# дата прозвона
	  PhotoFolder TEXT NOT NULL;
	)ENGINE=INNODB;

CREATE TABLE RealtyShots(
	  shot MEDIUMBLOB
)

ALTER TABLE RealtyItem
	ADD  Author TEXT NOT NULL,
        ADD  ur TEXT NOT NULL,
        ADD  Price SMALLINT NOT NULL,
        ADD  Source  TEXT NOT NULL,
        ADD  ApplicationDate DATE NOT NULL,
        ADD  CallDate DATE NOT NULL;

ALTER TABLE RealtyItem
		ADD CONSTRAINT ISassetOF FOREIGN KEY (CompID) REFERENCES Company  ON DELETE CASCADE;



ALTER TABLE Company
DROP FOREIGN KEY realtyitem_foreign;

//ÑÂßÇÈ ÌÅÊÆÄÓ ÁÀÇÀÌÈ

ALTER TABLE `realtyshots`
ADD CONSTRAINT `realtyitem_foreign`
FOREIGN KEY (`ofrealtyid`)
REFERENCES `realtyitem` (`realtyid`)
ON DELETE CASCADE
ON UPDATE NO ACTION;
