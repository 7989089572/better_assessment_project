import React, {useEffect, useState} from 'react';

export default function CommentsSection({taskId}){
  const [comments, setComments] = useState([]);
  const [author, setAuthor] = useState('');
  const [content, setContent] = useState('');
  const [editingId, setEditingId] = useState(null);
  const apiBase = 'http://localhost:5000/api';

  useEffect(()=>{ fetchComments(); }, [taskId]);

  async function fetchComments(){
    const res = await fetch(`${apiBase}/comments?task_id=${taskId}`);
    const data = await res.json();
    setComments(data);
  }

  async function handleAdd(e){
    e.preventDefault();
    const res = await fetch(`${apiBase}/comments`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({task_id: taskId, author, content})
    });
    if (res.ok){ setAuthor(''); setContent(''); fetchComments(); }
  }

  async function handleDelete(id){
    if (!window.confirm('Delete comment?')) return;
    const res = await fetch(`${apiBase}/comments/${id}`, {method:'DELETE'});
    if (res.ok) fetchComments();
  }

  async function startEdit(c){
    setEditingId(c.id);
    setAuthor(c.author);
    setContent(c.content);
  }

  async function submitEdit(e){
    e.preventDefault();
    const res = await fetch(`${apiBase}/comments/${editingId}`, {
      method:'PUT',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({author, content})
    });
    if (res.ok){ setEditingId(null); setAuthor(''); setContent(''); fetchComments(); }
  }

  return (
    <div>
      <h3>Comments</h3>
      <ul>
        {comments.map(c => (
          <li key={c.id}>
            <strong>{c.author}</strong>: {c.content}
            <div>
              <button onClick={()=>startEdit(c)}>Edit</button>
              <button onClick={()=>handleDelete(c.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
      <form onSubmit={editingId ? submitEdit : handleAdd}>
        <input placeholder='Author' value={author} onChange={e=>setAuthor(e.target.value)} required />
        <input placeholder='Content' value={content} onChange={e=>setContent(e.target.value)} required />
        <button type='submit'>{editingId ? 'Save' : 'Add'}</button>
        {editingId && <button type='button' onClick={()=>{setEditingId(null); setAuthor(''); setContent('');}}>Cancel</button>}
      </form>
    </div>
  );
}
