import React, {useState, useEffect} from 'react';
import {Avatar, Button} from '@material-ui/core'

import './Post.css'


const BASE_URL = 'http://localhost:8000/'


function Post({ post }) {

  const [imageUrl, setImageUrl] = useState(null);
  const hasImage = post.image != null

  useEffect(() => {
    setImageUrl(post.image)
  }, [])

  return (
    <div className='post'>

      <div className='post_header'>
        <Avatar
          alt='user-avatar'
          src=''
        />
        <div className='post_headerInfo'>
          <h3>{post.author.username}</h3>
          <Button className='post_delete'>Delete</Button>
        </div>
      </div>

      {hasImage ? (
        <img
          className='post_image'
          src={imageUrl}
        />
      ): (
        <div></div>
      )}

      <h4 className='post_title'>{post.title}</h4>

    </div>
  )
}


export default Post
