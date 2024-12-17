import React from 'react';

type Repository = {
  id: number;
  name: string;
  stars: number;
  language: string;
  url: string;
};

type RepositoryListProps = {
  repositories: Repository[];
};

const RepositoryList: React.FC<RepositoryListProps> = ({ repositories }) => {
  return (
    <div className="list-group">
      {repositories.map((repo) => (
        <a
          key={repo.id}
          href={repo.url}
          target="_blank"
          rel="noopener noreferrer"
          className="list-group-item list-group-item-action"
        >
          <div className="d-flex justify-content-between">
            <h5 className="mb-1">{repo.name}</h5>
            <span className="badge bg-primary">{repo.stars} ⭐</span>
          </div>
          <p className="mb-1">{repo.language || 'Unknown Language'}</p>
        </a>
      ))}
    </div>
  );
};

export default RepositoryList;
