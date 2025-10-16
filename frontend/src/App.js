import React from 'react';
import CommentsSection from './components/CommentsSection';

export default function App(){
  return (
    <div style={{padding:20}}>
      <h1>Comments Demo</h1>
      <CommentsSection taskId={1} />
    </div>
  )
}
