import axios from 'axios';

const API_URL = 'http://localhost:8000/repositories/popular';

export const fetchPopularRepositories = async (
  date: string,
  language: string,
  limit: number
) => {
  try {
    const response = await axios.get(`${API_URL}?date=${date}&language=${language}&limit=${limit}`);

    if (response.status === 200) {
      return response.data;
    } else {
      alert(`Unexpected status code: ${response.status}`);
      return [];
    }
  } catch (error: any) {
    if (axios.isAxiosError(error) && error.response) {
      alert(`Error ${error.response.status}: ${error.response.data.detail || 'Something went wrong'}`);
    } else {
      alert(`Network Error: ${error.message || 'Unable to connect to the server'}`);
    }
    return [];
  }
};
