const { Pool } = require('pg');

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'authentification_db',
  password: '123456789',
  port: 5433,
});

module.exports = {
  query: (text, params) => pool.query(text, params),
};