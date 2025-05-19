// interceptors api
import axios from 'axios';
import apiUrl from '@/router/api.js';

axios.interceptors.request.use(config => {
  const token = localStorage.getItem('access');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  config.headers['Content-Type'] = 'multipart/form-data'
  return config;
});

axios.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      const refresh = localStorage.getItem('refresh');
      if (refresh) {
        try {
          const res = await axios.post(
          apiUrl.users.refresh,
          { "refresh": refresh },
        );
          const newAccess = res.data.access;
          localStorage.setItem('access', newAccess);
          originalRequest.headers['Authorization'] = 'Bearer ' + newAccess;
          return axios(originalRequest);
        } catch (refreshError) {
          localStorage.removeItem('access');
          localStorage.removeItem('refresh');
          window.location = "/login";
        }
      } else {
        window.location = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default axios;