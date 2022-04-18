PRAGMA foreign_keys=on;

CREATE TABLE IF NOT EXISTS "Surveys" (
	"id_survey"		INTEGER PRIMARY KEY,
	"adding_date"	timestamp
);

CREATE TABLE IF NOT EXISTS "QuestionTypes" (
	"id_type"		INTEGER PRIMARY KEY,
	"type"			TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Questions" (
	"id_question"	INTEGER PRIMARY KEY,
	"id_survey"		INTEGER NOT NULL,
	"question"		TEXT NOT NULL,
	"id_type"		INTEGER NOT NULL,
	FOREIGN KEY ("id_survey") REFERENCES "Surveys"("id_survey")
	FOREIGN KEY ("id_type") REFERENCES "QuestionTypes"("id_type")
);

CREATE TABLE IF NOT EXISTS "Options" (
	"id_option"		INTEGER PRIMARY KEY,
	"option"		TEXT NOT NULL,
	"id_question"	INTEGER NOT NULL,
	UNIQUE ("option", "id_question"),
	FOREIGN KEY ("id_question") REFERENCES "questions"("id_question")
);
 
CREATE TABLE IF NOT EXISTS "Answers" (
	"id_answer"		INTEGER PRIMARY KEY,
	"id_option"		INTEGER NOT NULL,
	"id_user"		INTEGER NOT NULL,
	"datetime"		timestamp,
	UNIQUE ("id_option", "id_user"),
	FOREIGN KEY ("id_option") REFERENCES "options"("id_option")
);