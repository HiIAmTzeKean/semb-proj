DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS personnel;

CREATE TABLE "user" (
	"id"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "personnel" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"vocation"	TEXT DEFAULT 'Auto Tech',
	"fmw"	TEXT DEFAULT 'Sembawang',
	"rank"	TEXT,
	"am_status"	TEXT,
	"am_remarks"	TEXT,
	"pm_status"	TEXT,
	"pm_remarks"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);