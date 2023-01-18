import React, { useState, useEffect } from 'react'
import ListItem from '../components/ListItem'
import AddButton from '../components/AddButton'


const NotesListPage = () => {
    const [zoekTekst, setZoekTekst] = useState('');
    let [notes, setNotes] = useState([])

    useEffect(() => {
        getNotes()
    }, [zoekTekst])

    
      let handleChange = (value) => {
        setZoekTekst( value)
        console.log('Handle Change:', value)
        getNotes()
    }

    let getNotes = async () => {
        // http://127.0.0.1:8000/notes/waar/find/
        const endpoint = `/notes/${zoekTekst}/find`
        console.log('endpoint',endpoint)
        try{
            const response = await fetch(endpoint,{
                method:'GET'
            })
            const notes = await response.json()
            console.log('ZOEK',notes)
            setNotes(notes)

            // let data = await response.json()
        }

    catch (e){
        console.log(e)
    }
    }
    return (
        <div className="notes">
            <div className="notes-header">
                <h2 className="notes-title">&#9782; Notes</h2>
                <p className="notes-count">{notes.length}</p>
            <input 
            type="search"
            placeholder='find note...'
            // value={zoekTekst}   
            onChange={(e) => { handleChange(e.target.value) }} value={notes?.body}/>
            {/* onChange={e => setZoekTekst(e.target.value)}  */}
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