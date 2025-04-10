import api from './client';

// Envia e-mail e senha para /login e retorna access_token
export const login = async (email, password) => {
  const response = await api.post('/login', {
    username: email, // o FastAPI espera "username"
    password,
  });
  return response.data;
};
