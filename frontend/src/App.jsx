import { Navigate, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import StoriesPage from './pages/StoriesPage';
import StoryDetailPage from './pages/StoryDetailPage';
import CharactersPage from './pages/CharactersPage';
import CharacterDetailPage from './pages/CharacterDetailPage';
import LocationsPage from './pages/LocationsPage';
import LocationDetailPage from './pages/LocationDetailPage';
import ArtworksPage from './pages/ArtworksPage';
import ArtworkDetailPage from './pages/ArtworkDetailPage';

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<StoriesPage />} />
        <Route path="/stories/:storyId" element={<StoryDetailPage />} />
        <Route path="/characters" element={<CharactersPage />} />
        <Route path="/characters/:characterId" element={<CharacterDetailPage />} />
        <Route path="/locations" element={<LocationsPage />} />
        <Route path="/locations/:locationId" element={<LocationDetailPage />} />
        <Route path="/artworks" element={<ArtworksPage />} />
        <Route path="/artworks/:artworkId" element={<ArtworkDetailPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}
