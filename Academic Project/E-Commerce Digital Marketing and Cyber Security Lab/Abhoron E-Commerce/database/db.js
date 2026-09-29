const fs = require('node:fs');
const path = require('node:path');
const { DatabaseSync } = require('node:sqlite');

const DB_PATH = path.join(__dirname, 'ecommerce.db');
const SCHEMA_PATH = path.join(__dirname, 'schema.sql');

class EcommerceDatabaseManager {
    constructor(dbFilePath = DB_PATH) {
        this.db = new DatabaseSync(dbFilePath);
        this.initSchema();
    }

    initSchema() {
        if (fs.existsSync(SCHEMA_PATH)) {
            const schemaSql = fs.readFileSync(SCHEMA_PATH, 'utf8');
            this.db.exec(schemaSql);
        }
    }

    query(sql, params = []) {
        const stmt = this.db.prepare(sql);
        return stmt.all(...params);
    }

    get(sql, params = []) {
        const stmt = this.db.prepare(sql);
        return stmt.get(...params);
    }

    run(sql, params = []) {
        const stmt = this.db.prepare(sql);
        return stmt.run(...params);
    }

    exec(sql) {
        return this.db.exec(sql);
    }

    close() {
        this.db.close();
    }
}

let instance = null;

function getEcommerceDb(customPath) {
    if (!instance || customPath) {
        instance = new EcommerceDatabaseManager(customPath || DB_PATH);
    }
    return instance;
}

module.exports = {
    EcommerceDatabaseManager,
    getEcommerceDb
};
