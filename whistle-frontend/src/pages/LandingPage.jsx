import React from 'react';
import { Amplify } from 'aws-amplify';
import { Button, View, Heading, Text } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import awsExports from '../aws-exports';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

Amplify.configure(awsExports);

function LandingPage() {
    const navigate = useNavigate();
  return (
      <View
      height="100vh"
      backgroundColor="#0d0d0d"
      color="white"
      display="flex"
      justifyContent="center"
      alignItems="center"
      flexDirection="column"
      gap="2rem"
    >
      <Heading level={1} color="white">Welcome to WhistleKE</Heading>
      <Text fontSize="1.25rem" maxWidth="400px" textAlign="center">
        Speak truth. Stay anonymous.
      </Text>

      <View display="flex" gap="1rem" marginTop="2rem">
        <Button variation="primary" onClick={() => navigate('/create-alias')}>
          Create Alias
        </Button>
        <Button variation="link" onClick={() => navigate('/alias')}>
          Login Alias
        </Button>
      </View>
    </View>
  );
}
export default LandingPage;