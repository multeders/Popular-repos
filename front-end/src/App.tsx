import React, { useState, useEffect } from 'react';
import RepositoryList from './components/RepositoryList';
import FilterForm from './components/FilterForm';
import { fetchPopularRepositories } from './services/api';

const App: React.FC = () => {
  const [repositories, setRepositories] = useState([]);

  const handleFilter = async (date: string, language: string, limit: number) => {
    try {
      const repos = await fetchPopularRepositories(date, language, limit);
      setRepositories(repos);
    } catch (error) {
      console.error('Failed to fetch repositories:', error);
    }
  };
  
  return (
    <div className="container my-5">
      <h1 className="text-center mb-4">GitHub Repository Explorer</h1>
      <FilterForm onFilter={handleFilter} />
      <RepositoryList repositories={repositories} />
    </div>
  );
};

export default App;
