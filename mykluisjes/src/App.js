import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import NotesListPage from "./pages/NotesListPage";
import NotePage from "./pages/NotePage";
import './App.css';

function App() {
  return (
      <BrowserRouter>
    <div className="container dark">
      <div className="app">
      <Header />
        <Routes>
          <Route path="/" exact element={<NotesListPage />} />
          <Route path="note/:id" element={<NotePage />} />
        </Routes>
        </div>
      </div>
      </BrowserRouter>
  );
}

export default App;
// from dennis ivy on https://www.youtube.com/watch?v=tYKRAXIio28&t=2324s