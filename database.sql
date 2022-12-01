CREATE SCHEMA "school";

CREATE TABLE "school"."student"(
    id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    name VARCHAR NOT NULL,
    score numeric NOT NULL
);

INSERT INTO "school"."student"("name", "score")
VALUES('Hakeem', 10.0);

SELECT * FROM "school"."student";