import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage.jsx';
import CreateAlias from './pages/CreateAlias.jsx';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/create-alias" element={<CreateAlias />} />
    </Routes>
  );
}


