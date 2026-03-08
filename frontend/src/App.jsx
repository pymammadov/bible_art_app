import { Navigate, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import StoriesPage from './pages/StoriesPage';
import StoryDetailPage from './pages/StoryDetailPage';

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<StoriesPage />} />
        <Route path="/stories/:storyId" element={<StoryDetailPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}
