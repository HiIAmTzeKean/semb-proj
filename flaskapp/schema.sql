DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS "personnel_status";
DROP TABLE IF EXISTS "personnel";


CREATE TABLE "user" (
	"id"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"fmw"	TEXT NOT NULL,
	"fmd"	TEXT NOT NULL,
	"clearance"	INTEGER NOT NULL CHECK("clearance" = 1 OR "clearance" = 2 OR "clearance" = 3),
	PRIMARY KEY("id" AUTOINCREMENT)
);


CREATE TABLE "personnel" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"fmw"	TEXT,
	"rank"	TEXT,
	"active"	INTEGER NOT NULL DEFAULT 1 CHECK("active" = 1 OR "active" = 0),
	PRIMARY KEY("id" AUTOINCREMENT)
);


CREATE TABLE "personnel_status" (
	"id"	INTEGER,
	"personnel_id"	INTEGER NOT NULL,
	"date"	DATETIME NOT NULL,
	"am_status"	TEXT NOT NULL,
	"am_remarks"	TEXT,
	"pm_status"	TEXT NOT NULL,
	"pm_remarks"	TEXT,
	FOREIGN KEY("personnel_id") REFERENCES "personnel"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);