import React from 'react'
import { useParams, Link } from "react-router-dom";
import notes from '../assets/data';
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg'

const NotePage=(props) => {
    const params = useParams(); // vervanger van match.params
    console.log("PROPS:", props,params)
    let NoteId=params.id
    let note=notes.find(note => note.id === Number(NoteId))
    console.log("NOTEID:",NoteId)
  return (
    <div className='note'>
        <div className='note-header'>
            <h3>
            <Link to="/">
                <ArrowLeft />
            </Link>
            </h3>
        </div>
        <text>{note?.body}</text>
    </div>
  )
}

export default NotePage