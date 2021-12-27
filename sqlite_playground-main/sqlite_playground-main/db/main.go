package main

import (
	"database/sql"
	"fmt"
	"io/ioutil"

	_ "github.com/mattn/go-sqlite3"
)

func initDB() *sql.DB {
	db, err := sql.Open("sqlite3", "main.db")
	if err != nil {
		panic(err)
	}
	if db == nil {
		panic("db nil")
	}
	return db
}

func execSQLFile(db *sql.DB, filename string) error {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		return fmt.Errorf("failed to read schema file: %w", err)
	}
	if _, err := db.Exec(string(content)); err != nil {
		return fmt.Errorf("failed to exec %q: %w", filename, err)
	}
	return nil
}

func main() {
	db := initDB()
	defer db.Close()

	if err := execSQLFile(db, "schema.sql"); err != nil {
		panic(err)
	}

	if err := execSQLFile(db, "data.sql"); err != nil {
		panic(err)
	}
}
