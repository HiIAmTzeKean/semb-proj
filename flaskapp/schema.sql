DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS "personnel_status";
DROP TABLE IF EXISTS "personnel";

CREATE TABLE "user" (
	"id" INTEGER,
	"username" TEXT NOT NULL UNIQUE,
	"password" TEXT NOT NULL,
	"fmw" TEXT DEFAULT 'Sembawang',
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "personnel" (
	"id" INTEGER,
	"name" TEXT NOT NULL,
	"fmw" TEXT DEFAULT 'Sembawang',
	"rank" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "personnel_status" (
    "id" INTEGER,
    "personnel_id" INTEGER NOT NULL,
    "date" DATETIME NOT NULL,
    "time" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "remarks" TEXT,
    FOREIGN KEY (personnel_id) REFERENCES personnel(id),
    CONSTRAINT CHK_Status CHECK (time='AM' OR time='PM'),
    PRIMARY KEY("id" AUTOINCREMENT)
);