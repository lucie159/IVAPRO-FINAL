const db = require('../config/db');

const User = {
  create: async (username, email, password) => {
  console.log("Tentative de création :", username, email); // ← Ajoute ceci
  const { rows } = await db.query(
    'INSERT INTO users(username, email, password) VALUES($1, $2, $3) RETURNING *',
    [username, email, password]
  );
  return rows[0];
},


  findByEmail: async (email) => {
    const { rows } = await db.query('SELECT * FROM users WHERE email = $1', [email]);
    return rows[0];
  },
};

module.exports = User;