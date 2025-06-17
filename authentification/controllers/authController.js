const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const register = async (req, res) => {
  try {
    const { username, email, password } = req.body;
    console.log("Registering user:", { username, email });

    const existingUser = await User.findByEmail(email);
    if (existingUser) {
      return res.status(400).json({ message: 'User already exists' });
    }

    const hashedPassword = await bcrypt.hash(password, 12);
    const user = await User.create(username, email, hashedPassword);
    res.status(201).json({ user });

  }  catch (error) {
  console.error("❌ Erreur dans register:", error.message);
  console.error("📄 Stack trace:", error.stack);
  res.status(500).json({
    message: 'Erreur serveur : ' + error.message,
    stack: error.stack,
  });
}

};

const login = async (req, res) => {
  try {
    const { email, password } = req.body;
    console.log("📩 Tentative de login:", email);

    const user = await User.findByEmail(email);
    console.log("🔍 Utilisateur trouvé:", user);

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    const isPasswordCorrect = await bcrypt.compare(password, user.password);
    console.log("🔑 Mot de passe correct ?", isPasswordCorrect);

    if (!isPasswordCorrect) {
      return res.status(400).json({ message: 'Invalid credentials' });
    }
    const JWT_SECRET = process.env.JWT_SECRET || 'votre_cle_secrete';
    const token = jwt.sign(
      { email: user.email, id: user.id },
      JWT_SECRET,  // ✅ Cohérent avec le reste du projet
      { expiresIn: '1h' }
    );

    return res.status(200).json({ result: user, token });
  } catch (error) {
    console.error("🔥 Erreur de login:", error.message);
    return res.status(500).json({ message: 'Erreur serveur: ' + error.message });
  }
};

module.exports = { register, login };