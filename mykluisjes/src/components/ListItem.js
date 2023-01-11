// import { Tab } from 'bootstrap'
import React from 'react'
import { Link } from 'react-router-dom'
import {Table} from 'reactstrap'


let getTime = (note) => {
    return new Date(note.updated).toLocaleDateString()
}

let getTitle = (note) => {
    //spit by new lines and just get the first line
    //split will make a list of each line and will only pull on the first line by index zero
    // const title = note.body.split('\n')[0]
    const title = note.location
    if (title.length > 45) {
        return title.slice(0, 45)
    }
    return title
}


let getContent = (note) => {
    //Get content after title
    let title = getTitle(note)
    let content = note.body.replaceAll('\n', ' ')
    content = content.replaceAll(title, '') +"\n"

    //Slice content and add three dots in over 45 characters to show there is more
    if (content.length > 45) {
        return content.slice(0, 45) + '...'
    } else {
        return content
        // return     <div>

        // <Table className="person-table">
        //         <thead>
        //             <tr>
        //                 <th>Kluis</th>
        //                 <th>Naam</th>
        //                 <th>Code</th>
        //             </tr>
        //         </thead>
        //         <tbody>
        //             <tr>
        //                 <td>{note.location}</td>
        //                 <td>{note.body}</td>
        //                 <td>{note.code}</td>
        //             </tr>
        //         </tbody>
        //     </Table>
        //     </div>
    }

}


const ListItem = ({ note }) => {
    return (
        <Link to={`/note/${note.id}`}>
            <div className="notes-list-item">
                <h3>{getTitle(note)}</h3>
                <p><span>{getTime(note)}</span>{getContent(note)}</p>
            </div>
        </Link>
    )
}

export default ListItem