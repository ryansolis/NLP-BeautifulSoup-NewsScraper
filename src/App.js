import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ArticleList.css';

function ArticleList() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [articlesPerPage] = useState(30);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [searchDate, setSearchDate] = useState('');
  const [selectedDate, setSelectedDate] = useState('');

  useEffect(() => {
    axios.get('/articles')
      .then(response => {
        setArticles(response.data);
        setLoading(false);
      })
      .catch(error => console.log(error));
  }, []);

  // Get current articles
  const indexOfLastArticle = currentPage * articlesPerPage;
  const indexOfFirstArticle = indexOfLastArticle - articlesPerPage;

  const filteredArticles = articles.filter(article => {
    const keywordMatch = article.title.toLowerCase().includes(searchKeyword.toLowerCase());
    const dateMatch = article.pubdate.includes(searchDate);

    return keywordMatch && dateMatch;
  });

  const currentArticles = filteredArticles.slice(indexOfFirstArticle, indexOfLastArticle);

  // Change page
  const nextPage = () => setCurrentPage(currentPage + 1);
  const prevPage = () => setCurrentPage(currentPage - 1);


  // Format date to "month day, year" format
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const options = { month: 'long', day: 'numeric', year: 'numeric' };
    return date.toLocaleDateString('en-US', options);
  }

  // Update selected date
  const handleDateChange = (event) => {
    const selectedDate = formatDate(event.target.value);
    setSelectedDate(selectedDate);
    setSearchDate(selectedDate);
  }

  if (loading) {
    return (
      <div className="loading">
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="container">
      <h1 className="title">
        NLP News Website Feed
      </h1>
      <div className="search">
        <input type="text" placeholder="Search by Keyword" value={searchKeyword} onChange={e => setSearchKeyword(e.target.value)} />
        <input type="date" placeholder="" value={selectedDate} onChange={handleDateChange} />
      </div>
      {currentArticles.length > 0 ? currentArticles.map(article => (
        <div className="card" key={article.id}>
          <h2 className="card-title">{article.title}</h2>
          <div className="card-author">
            by {article.author} ({article.pubdate})
          </div>
          <p className="card-summary">{article.summary}</p>
          <a className="card-link" href={article.url}>
            Read more
          </a>
        </div>
      )) : <div className="no-results">No articles found.</div>}
      <div className="pagination">
        <div
          className={`next-prev ${currentPage === 1 ? 'disabled' : ''}`}
          onClick={prevPage}
        >
          Previous
        </div>
        {Array.from({ length: Math.ceil(filteredArticles.length / articlesPerPage) }, (_, i) => (
          <div
            key={i}
            className={`page-item ${i + 1 === currentPage ? 'active' : ''}`}
            onClick={() => setCurrentPage(i + 1)}
          >
            <a className="page-link" href="#">{i + 1}</a>
          </div>
        ))}
        <div
          className={`next-prev ${currentPage === Math.ceil(filteredArticles.length / articlesPerPage) ? 'disabled' : ''}`}
          onClick={nextPage}
        >
          Next
        </div>
      </div>
    </div>
  );
}

export default ArticleList;

