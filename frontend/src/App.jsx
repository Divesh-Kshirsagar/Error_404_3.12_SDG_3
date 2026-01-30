/**
 * Main App component with routing and TanStack Query setup
 */
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import './index.css';

// Patient Components
import PatientLogin from './components/patient/PatientLogin';
import PatientRegister from './components/patient/PatientRegister';
import PatientHome from './components/patient/PatientHome';
import SubmitSymptoms from './components/patient/SubmitSymptoms';

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

// Home page
const Home = () => (
  <div className="min-h-screen bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center px-4">
    <div className="text-center">
      <h1 className="text-6xl font-bold text-white mb-4">AarogyaQueue</h1>
      <p className="text-2xl text-blue-100 mb-12">Telemedicine Queue Optimizer</p>
      <div className="flex flex-col gap-6 max-w-md mx-auto">
        <a href="/patient" className="bg-white text-blue-600 px-12 py-6 rounded-xl text-2xl font-bold hover:bg-blue-50 shadow-2xl transition-all">
          👤 Patient Portal
        </a>
        <a href="/doctor" className="bg-white text-green-600 px-12 py-6 rounded-xl text-2xl font-bold hover:bg-green-50 shadow-2xl transition-all">
          🩺 Doctor Portal
        </a>
        <a href="/admin" className="bg-white text-purple-600 px-12 py-6 rounded-xl text-2xl font-bold hover:bg-purple-50 shadow-2xl transition-all">
          ⚙️ Admin Portal
        </a>
      </div>
    </div>
  </div>
);

const DoctorPortal = () => <div className="p-8"><h1 className="text-3xl font-bold">Doctor Portal (Coming Soon)</h1></div>;
const AdminPortal = () => <div className="p-8"><h1 className="text-3xl font-bold">Admin Portal (Coming Soon)</h1></div>;

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />

          {/* Patient Routes */}
          <Route path="/patient" element={<PatientLogin />} />
          <Route path="/patient/register" element={<PatientRegister />} />
          <Route path="/patient/home" element={<PatientHome />} />
          <Route path="/patient/submit-symptoms" element={<SubmitSymptoms />} />

          {/* Doctor Routes (placeholders) */}
          <Route path="/doctor/*" element={<DoctorPortal />} />

          {/* Admin Routes (placeholders) */}
          <Route path="/admin/*" element={<AdminPortal />} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
