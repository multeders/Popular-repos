import React, { useState } from 'react';

type FilterFormProps = {
  onFilter: (date: string, language: string, limit: number) => void;
};

const TOP_LANGUAGES = [
  'JavaScript',
  'Python',
  'Java',
  'C#',
  'C++',
  'PHP',
  'TypeScript',
  'Ruby',
  'Swift',
  'Go',
  'Kotlin',
  'Rust',
  'Dart',
  'Scala',
  'Perl',
  'Haskell',
  'Shell',
  'Lua',
  'R',
  'Objective-C',
];

const FilterForm: React.FC<FilterFormProps> = ({ onFilter }) => {
  const [date, setDate] = useState('');
  const [language, setLanguage] = useState('');
  const [limit, setLimit] = useState(10);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if(!date){
      alert("Please enter a date");
      return;
    }
    onFilter(date, language, limit);
  };

  return (
    <form className="mb-4" onSubmit={handleSubmit}>
      <div className="row g-3">
        <div className="col-md-4">
          <label htmlFor="date" className="form-label">
            Date (YYYY-MM-DD)
          </label>
          <input
            type="date"
            id="date"
            className="form-control"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>
        <div className="col-md-4">
          <label htmlFor="language" className="form-label">
            Language
          </label>
          <select
            id="language"
            className="form-select"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            <option value="">None</option>
            {TOP_LANGUAGES.map((lang) => (
              <option key={lang} value={lang}>
                {lang}
              </option>
            ))}
          </select>
        </div>
        <div className="col-md-4">
          <label htmlFor="limit" className="form-label">
            Results Limit
          </label>
          <select
            id="limit"
            className="form-select"
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
          >
            <option value={10}>Top 10</option>
            <option value={50}>Top 50</option>
            <option value={100}>Top 100</option>
          </select>
        </div>
      </div>
      <button type="submit" className="btn btn-primary mt-3">
        Search
      </button>
    </form>
  );
};

export default FilterForm;
