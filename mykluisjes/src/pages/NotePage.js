import React, { useState, useEffect } from 'react'
import { useParams, Link } from "react-router-dom";
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg'
// https://django-react-notesapp-master-production.up.railway.app
const NotePage = ({  history }) => {
    const params = useParams(); // vervanger van match.params.id
    let noteId = params.id;
    let [note, setNote] = useState(null)

    useEffect(() => {
        getNote();
      }, [noteId]);


    let getNote = async () => {
        if (noteId === 'new') return

<<<<<<< HEAD
        let response = await fetch(`/notes/${noteId}/`)
=======
        let response = await fetch(`notes/${noteId}/`)
>>>>>>> 74067c0 (v13-1-08)
        let data = await response.json()
        setNote(data)
    }

    let createNote = async () => {
<<<<<<< HEAD
        fetch(`/notes/create/`, {
=======
        fetch(`notes/`, {
>>>>>>> 74067c0 (v13-1-08)
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(note)
        })
    }


    let updateNote = async () => {
<<<<<<< HEAD
        fetch(`/notes/${noteId}/update/`, {
=======
        fetch(`notes/${noteId}/`, {
>>>>>>> 74067c0 (v13-1-08)
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(note)
        })
    }


    let deleteNote = async () => {
<<<<<<< HEAD
        fetch(`/notes/${noteId}/delete/`, {
=======
        fetch(`notes/${noteId}/`, {
>>>>>>> 74067c0 (v13-1-08)
            method: 'DELETE',
            'headers': {
                'Content-Type': 'application/json'
            }
        })
        history.push('/')
    }

    let handleSubmit = () => {
        if (noteId !== 'new' && note.body === '') {
            deleteNote()
        } else if (noteId !== 'new') {
            updateNote()
        } else if (noteId === 'new' && note.body !== null) {
            createNote()
        }
        history.push('/')
    }

    let handleChange = (value) => {
        setNote(note => ({ ...note, 'body': value }))
        console.log('Handle Change:', note)
    }

    return (
        <div className="note" >
        <div className="note-header">
            <h3>
                <Link to="/">
                <ArrowLeft onClick={handleSubmit} />
                </Link>
            </h3>
            {noteId !== 'new' ? (
                <button onClick={deleteNote}>Delete</button>
            ) : (
                <button onClick={handleSubmit}>Done</button>
            )}

        </div>
        <textarea onChange={(e) => { handleChange(e.target.value) }} value={note?.body}></textarea>
    </div>
    )
}

export default NotePage