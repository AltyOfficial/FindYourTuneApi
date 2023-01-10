import React, {useState, useEffect} from 'react';

import './App.css';

import Post from './Post.js';


const BASE_URL = 'http://localhost:8000/'


function App() {

  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch(BASE_URL + 'api/posts/')
      .then(response => {
        const json = response.json()
        if (response.ok) {
          return json
        }
        throw response
      })
      .then(data => {
        setPosts(data.results)
      })
  })

  return (
    <div className="app">

      <div className='app_header'>
        <img className='app_headerLogo'
          alt='InstagramClone Logo'
          src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Instagram_logo.svg/800px-Instagram_logo.svg.png'
        />
        <div className='app_headerRightMenu'>
          Posts
          Bands
        </div>
      </div>

      <div className='app_posts'>
        {
          posts.map(post => (
            <Post
              post = {post}
            />
          ))
        }
      </div>

    </div>
  );
}

export default App;
