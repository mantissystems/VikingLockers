import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import kluisHeader from "./components/KluisHeader"
import NotesListPage from "./pages/NotesListPage";
import NotePage from "./pages/NotePage";
// import {Nav,Navbar} from 'react-bootstrap';
// import Button from 'react-bootstrap/Button';
// import KluisjesPage from "./pages/KluisjesPage"
// import KluisjesListPage from "./pages/KluisjesListPage"
import './App.css';

function App() {
  return (
    <div className="container dark">
      <div className="app">
      <kluisHeader />

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<NotesListPage />} />
          {/* <Route path="note/:id" element={<NotePage />} /> */}
          <Route path="notes/:id" element={<NotePage />} />
          {/* <Route path="/k" element={<KluisjesListPage />} /> */}
        </Routes>
      </BrowserRouter>
    </div>
      </div>
  );
}

export default App;
// from dennis ivy on https://www.youtube.com/watch?v=tYKRAXIio28&t=2324s