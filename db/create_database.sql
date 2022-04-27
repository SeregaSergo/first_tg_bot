PRAGMA foreign_keys=on;

CREATE TABLE IF NOT EXISTS "Surveys" (
	"id"			INTEGER PRIMARY KEY,
	"file_id"		TEXT,
	"date"			TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "QuestionTypes" (
	"id"			INTEGER PRIMARY KEY,
	"type"			TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "Questions" (
	"id"			INTEGER PRIMARY KEY,
	"id_survey"		INTEGER NOT NULL,
	"question"		TEXT NOT NULL,
	"id_type"		INTEGER NOT NULL,
	FOREIGN KEY ("id_survey") REFERENCES "Surveys"("id")
	FOREIGN KEY ("id_type") REFERENCES "QuestionTypes"("id")
);

CREATE TABLE IF NOT EXISTS "Options" (
	"id"			INTEGER PRIMARY KEY,
	"option"		TEXT NOT NULL,
	"id_question"	INTEGER NOT NULL,
	UNIQUE ("option", "id_question"),
	FOREIGN KEY ("id_question") REFERENCES "Questions"("id")
);
 
CREATE TABLE IF NOT EXISTS "Answers" (
	"id"			INTEGER PRIMARY KEY,
	"id_option"		INTEGER NOT NULL,
	"id_user"		INTEGER NOT NULL,
	"datetime"		TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE ("id_option", "id_user"),
	FOREIGN KEY ("id_option") REFERENCES "Options"("id")
);