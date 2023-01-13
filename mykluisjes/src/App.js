import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import NotesListPage from "./pages/NotesListPage";
import NotePage from "./pages/NotePage";
import './App.css';

function App() {
  return (
    <div className="container dark">
      <div className="app">
      <Header />
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<NotesListPage />} />
          <Route path="/note/:id" element={<NotePage />} />
=======
=======
>>>>>>> 74067c0 (v13-1-08)
=======
>>>>>>> 74067c0 (v13-1-08)

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<NotesListPage />} />
          <Route path="note/:id" element={<NotePage />} />
          {/* <Route path="kluisje/:id" element={<NotePage />} /> */}
          {/* <Route path="/k" element={<KluisjesListPage />} /> */}
>>>>>>> 74067c0 (v13-1-08)
        </Routes>
      </BrowserRouter>
    </div>
      </div>
  );
}

export default App;
// from dennis ivy on https://www.youtube.com/watch?v=tYKRAXIio28&t=2324s