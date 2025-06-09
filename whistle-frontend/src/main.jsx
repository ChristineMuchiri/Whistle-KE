import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { Amplify } from 'aws-amplify';
import awsExports from './aws-exports';
import App from './App.jsx'

Amplify.configure(awsExports);

const root = createRoot(document.getElementById('root'));
root.render(<App />);

