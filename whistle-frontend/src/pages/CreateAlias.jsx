import { useState } from 'react';
import { Auth } from '@aws-amplify/auth';
import { Button, View, TextField, Heading } from '@aws-amplify/ui-react';

export default function CreateAlias() {
  const [alias, setAlias] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSignup = async () => {
    try {
      const { user } = await Auth.signUp({
        username: alias,
        password,
        autoSignIn: { enabled: true }, // Optional auto login if available
      });
        console.log('New user created:', user);
      setMessage('Alias created. You can now log in.');
    } catch (err) {
      if (err.code === 'UsernameExistsException') {
        setMessage('Alias already exists. Try logging in instead.');
      } else {
        setMessage(err.message || 'Something went wrong.');
      }
    }
  };

  return (
    <View padding="2rem" backgroundColor="#121212" color="white">
      <Heading level={3}>Create Alias</Heading>
      <TextField
        label="Alias (username)"
        onChange={(e) => setAlias(e.target.value)}
        value={alias}
      />
      <TextField
        label="Password"
        type="password"
        onChange={(e) => setPassword(e.target.value)}
        value={password}
      />
      <Button variation="primary" onClick={handleSignup}>
        Create Alias
      </Button>
      {message && <p style={{ marginTop: '1rem', color: '#00ffcc' }}>{message}</p>}
    </View>
  );
}
