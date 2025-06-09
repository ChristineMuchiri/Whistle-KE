import React from 'react';
import { Amplify } from 'aws-amplify';
import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import awsExports from '../aws-exports';
import './LandingPage.css';

Amplify.configure(awsExports);

function LandingPage() {
  return (
      <div className='landing-page'>
          <div className='cyberpunk-overlay'></div>
          <div className='content'>
             <h1 className='title'>Welcome to <span className='whistleke'>WhistleKE</span>
              </h1> 
              <p className='tagline'>Speak Truth. Stay anonymous</p>

              <div className="button-group">
                 <Authenticator>
            {({ signOut, user }) => (
              <>
                {!user ? (
                  <>
                    <button 
                      className="cyber-button" 
                      onClick={() => window.location.href = '/create-alias'}
                    >
                      CREATE ALIAS
                    </button>
                    <button 
                      className="cyber-button secondary"
                      onClick={() => window.location.href = '/login'}
                    >
                      LOGIN ALIAS
                    </button>
                  </>
                ) : (
                  <button className="cyber-button" onClick={signOut}>
                    SIGN OUT
                  </button>
                )}
              </>
            )}
          </Authenticator> 
              </div>
          </div>
    </div>
  );
}
export default LandingPage;