-- DROP TABLE games_old;

-- CREATE TABLE games_old (
--     id INTEGER PRIMARY KEY,
--     name TEXT NOT NULL,
--     game_id INTEGER NOT NULL,
--     path TEXT NOT NULL,
--     args TEXT,
--     favorite BOOLEAN NOT NULL
-- );

-- DROP TABLE gamesTags;
-- DROP TABLE gamesGenres;
-- DROP TABLE gamesFeatures;
-- DROP TABLE gamesLinks;
-- DROP TABLE ageRatings;
-- DROP TABLE categories;
-- DROP TABLE features;
-- DROP TABLE genres;
-- DROP TABLE series;
-- DROP TABLE sources;
-- DROP TABLE tags;
-- DROP TABLE companies;
-- DROP TABLE publishers;
-- DROP TABLE developers;
-- DROP TABLE games;
-- -- DROP TABLE regions;


CREATE TABLE ageRatings (
    id                  INTEGER     PRIMARY KEY,              -- ID in the database
    name                TEXT        NOT NULL                  -- Name of the rating
);

CREATE TABLE categories (
    id                  INTEGER     PRIMARY KEY,              -- ID in the database
    name                TEXT        NOT NULL                  -- Category name
);

CREATE TABLE features (
    id                  INTEGER     PRIMARY KEY,              -- ID in the database
    name                TEXT        NOT NULL                  -- Name of the feature
);

CREATE TABLE genres (
    id                  INTEGER     PRIMARY KEY,              -- ID in the database
    name                TEXT        NOT NULL                  -- Name of the genre
);

-- CREATE TABLE regions (
--     id                  INTEGER     PRIMARY KEY,              -- ID in the database
--     name                TEXT        NOT NULL                  -- Name of the region
-- );

CREATE TABLE series (
    id                  INTEGER     PRIMARY KEY,              -- ID in the database
    name                TEXT        NOT NULL                  -- Name of the serie
);

CREATE TABLE sources (
    id                  INTEGER     PRIMARY KEY,              -- ID in the database
    name                TEXT        NOT NULL                  -- Name of the source
);

CREATE TABLE tags (
    id                  INTEGER     PRIMARY KEY,              -- ID in the database
    name                TEXT        NOT NULL                  -- Name of the tag
);

CREATE TABLE companies (
    id                  INTEGER     PRIMARY KEY,              -- ID in the database
    name                TEXT        NOT NULL                  -- Name of the company
);

-- CREATE TABLE tools (
--     id                  INTEGER     PRIMARY KEY,              -- ID in the database
-- );

CREATE TABLE games (
    id                  INTEGER     PRIMARY KEY,              -- ID in the database
    uuid                BLOB        NOT NULL    UNIQUE,       -- ID used outside of the database
    name                TEXT        NOT NULL,                 -- Name of the game
    sortingName         TEXT,                                 -- Name used to sort in the library
    backgroundImage     TEXT,                                 -- Path to the background image (uuid\\imageName.extension)
    coverImage          TEXT,                                 -- Path to the cover image (uuid\\imageName.extension)
    bannerImage         TEXT,                                 -- Path to the banner image (uuid\\imageName.extension)
    iconImage           TEXT,                                 -- Path to the icon image (uuid\\imageName.extension)
    directory           TEXT        NOT NULL,                 -- Path to the installation directory
    exePath             TEXT        NOT NULL,                 -- Path to the executable file (directory\\exe.exe)
    description         TEXT,                                 -- Description of the game
    releaseDate         TEXT,                                 -- Release date of the game
    isInstalled         BOOLEAN     NOT NULL,                 -- Whether the game is installed or not
    isHidden            BOOLEAN,                              -- Whether to hide this game or not
    added               TEXT        NOT NULL,                 -- The date when the game was added
    lastModified        TEXT        NOT NULL,                 -- The last time it was modified
    lastActivity        TEXT,                                 -- The last time the game was launched
    seriesId            INT         REFERENCES series(id),    -- The id of the game's series
    ageRatingId         INT         REFERENCES ageRatings(id),-- The id of the game's age rating
    criticScore         INT,                                  -- The critics score for this game
    communityScore      INT,                                  -- The community score for this game
    userScore           INT,                                  -- The score given by the user
    gameId              TEXT,                                 -- The game's id other stores
    version             TEXT,                                 -- The version of the game
    timePlayed          INTEGER,                              -- The time playing the game (in seconds)
    playCount           INTEGER,                              -- The number of time the game was launched
    completionStatus    TEXT                                  -- The state of completion of the game
    -- region              TEXT,                                 -- The region of the game
    -- platform            TEXT,                                 -- The platform the game was made for
    -- source,
);

CREATE TABLE publishers (
    game_id integer NOT NULL REFERENCES games(id),
    company_id  integer NOT NULL REFERENCES companies(id),
    PRIMARY KEY (game_id, company_id)
);
CREATE TABLE developers (
    game_id integer NOT NULL REFERENCES games(id),
    company_id  integer NOT NULL REFERENCES companies(id),
    PRIMARY KEY (game_id, company_id)
);
CREATE TABLE gamesTags (
    game_id integer NOT NULL REFERENCES games(id),
    tag_id  integer NOT NULL REFERENCES tags(id),
    PRIMARY KEY (game_id, tag_id)
);
CREATE TABLE gamesGenres (
    game_id integer NOT NULL REFERENCES games(id),
    tag_id  integer NOT NULL REFERENCES tags(id),
    PRIMARY KEY (game_id, tag_id)
);
CREATE TABLE gamesFeatures (
    game_id integer NOT NULL REFERENCES games(id),
    feature_id  integer NOT NULL REFERENCES features(id),
    PRIMARY KEY (game_id, feature_id)
);
CREATE TABLE gamesLinks (
    game_id integer NOT NULL REFERENCES games(id),
    link_id  integer NOT NULL REFERENCES links(id),
    PRIMARY KEY (game_id, link_id)
);
