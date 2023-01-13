import React, { useState, useEffect } from 'react'
import ListItem from '../components/ListItem'
import AddButton from '../components/AddButton'


const NotesListPage = () => {

    let [notes, setNotes] = useState([])

    useEffect(() => {
        getNotes()
    }, [])


    let getNotes = async () => {

<<<<<<< HEAD
        let response = await fetch('/notes')
=======
        let response = await fetch('notes')
>>>>>>> 74067c0 (v13-1-08)
        let data = await response.json()
        setNotes(data)
    }

    return (
        <div className="notes">
            <div className="notes-header">
<<<<<<< HEAD
                <h2 className="notes-title">&#9782; Notes-local</h2>
=======
                <h2 className="notes-title">&#9782; NotesPage</h2>
>>>>>>> 74067c0 (v13-1-08)
                <p className="notes-count">{notes.length}</p>
            </div>

            <div className="notes-list">
                {notes.map((note, index) => (
                    <ListItem key={index} note={note} />
                ))}
            </div>
            <AddButton />
        </div>
    )
}

export default NotesListPage