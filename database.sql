-- -------------------------
-- TABLE: language
-- -------------------------
CREATE TABLE IF NOT EXISTS "language" (
    "language_code"   TEXT NOT NULL UNIQUE,
    "language"        TEXT NOT NULL,
	PRIMARY KEY("language_code")
);

-- -------------------------
-- TABLE: request
-- -------------------------
CREATE TABLE IF NOT EXISTS "request" (
    "request_id"       INTEGER NOT NULL UNIQUE,
    "user_translated"  BOOLEAN NOT NULL DEFAULT 0,
    "created_at"       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("request_id" AUTOINCREMENT)
);

-- -------------------------
-- TABLE: vocabulary
-- -------------------------
CREATE TABLE IF NOT EXISTS "vocabulary" (
    "term_id"   INTEGER NOT NULL UNIQUE,
    "term"      TEXT NOT NULL,
    "meaning"   TEXT NOT NULL,
    "type"      TEXT NOT NULL,
    "fk_language_code" TEXT NOT NULL,
    FOREIGN KEY ("fk_language_code") REFERENCES "language"("language_code"),
	PRIMARY KEY("term_id" AUTOINCREMENT)
);

-- -------------------------
-- TABLE: sentence
-- -------------------------
CREATE TABLE IF NOT EXISTS "sentence" (
    "sentence_id"  INTEGER NOT NULL UNIQUE,
    "english"      TEXT NOT NULL,
    "translation"  TEXT NOT NULL,
    "fk_request_id"  INTEGER NOT NULL,
    "fk_language_code" TEXT NOT NULL,
    FOREIGN KEY ("fk_request_id") REFERENCES "request"("request_id"),
    FOREIGN KEY ("fk_language_code") REFERENCES "language"("fk_language_code"),
	PRIMARY KEY("sentence_id" AUTOINCREMENT)
);

-- -------------------------
-- TABLE: request_vocabulary
-- (junction table for many-to-many)
-- -------------------------
CREATE TABLE IF NOT EXISTS "request_vocabulary" (
    "fk_request_id" INTEGER NOT NULL,
    "fk_term_id"    INTEGER NOT NULL,
    PRIMARY KEY ("fk_request_id", "fk_term_id"),
    FOREIGN KEY ("fk_request_id") REFERENCES "request"("request_id"),
    FOREIGN KEY ("fk_term_id") REFERENCES "vocabulary"("term_id")
);
