PRAGMA foreign_keys=on;

CREATE TABLE IF NOT EXISTS "questions" (
	"id_question"	INTEGER PRIMARY KEY,
	"question"		TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "options" (
	"id_option"		INTEGER PRIMARY KEY,
	"option"		INTEGER NOT NULL,
	"id_question"	INTEGER NOT NULL,
	UNIQUE ("option", "id_question"),
	FOREIGN KEY ("id_question") REFERENCES "questions"("id_question")
);
 
CREATE TABLE IF NOT EXISTS "answers" (
	"id_answer"		INTEGER PRIMARY KEY,
	"id_option"		INTEGER NOT NULL,
	"id_user"		INTEGER NOT NULL,
	"datetime"		INTEGER NOT NULL,
	UNIQUE ("id_option", "id_user"),
	FOREIGN KEY ("id_option") REFERENCES "options"("id_option")
);