import { api } from './api';

export const authService = {
  login: async (email: string, passwordHash: string) => {
    // Nota: enviando passwordHash conforme solicitado ou assumindo que o backend espera 'password'
    const res = await api.post('/auth/login', { email, password: passwordHash });
    return res.data;
  },
  
  me: async () => {
    const res = await api.get('/auth/me');
    return res.data;
  }
};
