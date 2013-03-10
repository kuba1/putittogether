DROP TABLE IF EXISTS settings;
DROP TABLE IF EXISTS languages;
DROP TABLE IF EXISTS captions;
DROP TABLE IF EXISTS presentations;
DROP TABLE IF EXISTS frames;

CREATE TABLE languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255)
);
CREATE TABLE captions (
    language_id INTEGER REFERENCES languages (id),
    key VARCHAR(255),
    value VARCHAR(255)
);
CREATE TABLE presentations (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255)
);
CREATE TABLE frames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    presentation_id INTEGER REFERENCES presentations (id),
    puzzle_rows INTEGER,
    puzzle_cols INTEGER,
    puzzle_text VARCHAR(255),
    puzzle_file BLOB
);
CREATE TABLE settings (
    key VARCHAR(255),
    value VARCHAR(255)
);

INSERT INTO languages (name) VALUES('Polski');
INSERT INTO languages (name) VALUES('English');

INSERT INTO settings VALUES('language', 'Polski');

INSERT INTO captions VALUES(1, 'error_title', 'Blad!');
INSERT INTO captions VALUES(2, 'error_title', 'Error!');
INSERT INTO captions VALUES(1, 'file_load_error', 'Nie mozna odczytac pliku. Program obsluguje pliki .bmp, .jpg oraz .png.');
INSERT INTO captions VALUES(2, 'file_load_error', 'Cannot read the file. This program supports .bmp, .jpg and .png files.');

INSERT INTO captions VALUES(1, '_load', '&Zaladuj');
INSERT INTO captions VALUES(2, '_load', '&Load');
INSERT INTO captions VALUES(1, '_restart', '&Zaladuj Ponownie');
INSERT INTO captions VALUES(2, '_restart', '&Load Again');
INSERT INTO captions VALUES(1, '_stop', '&Zatrzymaj');
INSERT INTO captions VALUES(2, '_stop', '&Stop');
INSERT INTO captions VALUES(1, '_play', '&Odtworz');
INSERT INTO captions VALUES(2, '_play', '&Play');
INSERT INTO captions VALUES(1, '_quit', '&Wyjdz');
INSERT INTO captions VALUES(2, '_quit', '&Quit');
INSERT INTO captions VALUES(1, 'wxglade_tmp_menu', '&Plik');
INSERT INTO captions VALUES(2, 'wxglade_tmp_menu', '&File');
INSERT INTO captions VALUES(1, '_load_tool_shortHelp', 'Zaladuj nowy obrazek i zrob z niego puzzle');
INSERT INTO captions VALUES(2, '_load_tool_shortHelp', 'Load new image and create a puzzle out of it');
INSERT INTO captions VALUES(1, '_restart_tool_shortHelp', 'Stworz nowe puzzle z zaladowanego obrazka');
INSERT INTO captions VALUES(2, '_restart_tool_shortHelp', 'Create new puzzle from loaded image');
INSERT INTO captions VALUES(1, '_presentation_tool_shortHelp', 'Edytuj prezentacje');
INSERT INTO captions VALUES(2, '_presentation_tool_shortHelp', 'Edit presentation');
INSERT INTO captions VALUES(1, '_stop_tool_shortHelp', 'Zatrzymaj prezentacje');
INSERT INTO captions VALUES(2, '_stop_tool_shortHelp', 'Stop presentation');
INSERT INTO captions VALUES(1, '_play_tool_shortHelp', 'Odtworz prezentacje');
INSERT INTO captions VALUES(2, '_play_tool_shortHelp', 'Play presentation');

INSERT INTO captions VALUES(1, '_puzzle_label', 'Puzzle:');
INSERT INTO captions VALUES(2, '_puzzle_label', 'Puzzle:');
INSERT INTO captions VALUES(1, '_rows_label', 'Rzedy:');
INSERT INTO captions VALUES(2, '_rows_label', 'Rows:');
INSERT INTO captions VALUES(1, '_columns_label', 'Kolumny:');
INSERT INTO captions VALUES(2, '_columns_label', 'Columns:');
INSERT INTO captions VALUES(1, '_caption_label', 'Napis:');
INSERT INTO captions VALUES(2, '_caption_label', 'Caption:');
INSERT INTO captions VALUES(1, '_caption_size_label', 'Rozmiar napisu:');
INSERT INTO captions VALUES(2, '_caption_size_label', 'Caption size:');
INSERT INTO captions VALUES(1, '_picture_file_label', 'Plik obrazu:');
INSERT INTO captions VALUES(2, '_picture_file_label', 'Picture file:');
INSERT INTO captions VALUES(1, '_load_picture_button', 'Zaladuj obrazek');
INSERT INTO captions VALUES(2, '_load_picture_button', 'Load picture');
INSERT INTO captions VALUES(1, '_sound_file_label', 'Plik dzwiekowy:');
INSERT INTO captions VALUES(2, '_sound_file_label', 'Sound file:');
INSERT INTO captions VALUES(1, '_play_sound_button', 'Odtworz');
INSERT INTO captions VALUES(2, '_play_sound_button', 'Play');
INSERT INTO captions VALUES(1, '_load_sound_button', 'Zaladuj dzwiek');
INSERT INTO captions VALUES(2, '_load_sound_button', 'Load sound');
INSERT INTO captions VALUES(1, '_add_frame_button', 'Dodaj');
INSERT INTO captions VALUES(2, '_add_frame_button', 'Add');
