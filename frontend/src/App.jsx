/**
 * Main App component with routing and TanStack Query setup
 */
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import './index.css';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5000,
    },
  },
});

// Temporary placeholder components (will be replaced with actual components)
const Home = () => (
  <div className="min-h-screen bg-gray-100 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-4xl font-bold text-blue-600 mb-4">AarogyaQueue</h1>
      <p className="text-xl text-gray-700 mb-8">Telemedicine Queue Optimizer</p>
      <div className="flex gap-4 justify-center">
        <a href="/patient" className="bg-blue-500 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-600">
          Patient Portal
        </a>
        <a href="/doctor" className="bg-green-500 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-green-600">
          Doctor Portal
        </a>
        <a href="/admin" className="bg-purple-500 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-purple-600">
          Admin Portal
        </a>
      </div>
    </div>
  </div>
);

const PatientPortal = () => <div className="p-8"><h1 className="text-2xl font-bold">Patient Portal</h1></div>;
const DoctorPortal = () => <div className="p-8"><h1 className="text-2xl font-bold">Doctor Portal</h1></div>;
const AdminPortal = () => <div className="p-8"><h1 className="text-2xl font-bold">Admin Portal</h1></div>;

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/patient/*" element={<PatientPortal />} />
          <Route path="/doctor/*" element={<DoctorPortal />} />
          <Route path="/admin/*" element={<AdminPortal />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
