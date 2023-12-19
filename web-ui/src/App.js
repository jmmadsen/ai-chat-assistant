import './App.css';

import React, { useEffect } from 'react';
import ChatBot from 'react-simple-chatbot';
import { ThemeProvider } from 'styled-components';
import axios from 'axios';


// custom component for chat bot step
const Answer = (props) => {

  useEffect(() => {
    const fetchData = async() => {
      try {
        const res = await axios.post(`http://localhost:5000/${props.type}_chain_query`, { message: props.previousStep.message });
        // after receiving API response, trigger next message (changing waitAction)
        props.triggerNextStep({ value: res.data, trigger: `${props.type}-res` });
      } catch (e) {
        props.triggerNextStep({ value: 'ERROR: cannot connect to backend API. Closing chat.', trigger: `error-res` });
      }
    }
    fetchData()
  }, [])

  return (<div>Thinking, give me a second...</div>)
}

// message loop from bot
const steps = [
  {
    id: '0',
    message: 'Hey there! I am your 2023 MLB season AI assistant.',
    trigger: '1'
  },
  {
    id: '1',
    message: 'Would you like to query the batting database, or ask a general question about the season?',
    trigger: '2'
  },
  {
    id: '2',
    options: [
      { value: 'General question', label: 'General question', trigger: 'docs' },
      { value: 'Query the database', label: 'Query the database', trigger: 'database' }
    ],
  },
  {
    id: 'database',
    message: `Please enter your question about the season's batting stats:`,
    trigger: 'database-q'
  },
  {
    id: 'database-q',
    user: true,
    trigger: 'database-wait'
  },
  {
    id: 'database-wait',
    component: <Answer type={'db'}/>,
    asMessage: true,
    trigger: 'db-res',
    waitAction: true
  },
  {
    id: 'docs',
    message: `Please enter your question about this season:`,
    trigger: 'docs-q'
  },
  {
    id: 'docs-q',
    user: true,
    trigger: 'docs-wait'
  },
  {
    id: 'docs-wait',
    component: <Answer type={'docs'}/>,
    asMessage: true,
    trigger: 'docs-res',
    waitAction: true
  },
  {
    id: 'db-res',
    message: '{previousValue}',
    trigger: 1
  },
  {
    id: 'docs-res',
    message: '{previousValue}',
    trigger: 1
  },
  {
    id: 'error-res',
    message: '{previousValue}',
    end: true
  }
];

// chat coloring
const theme = {
  background: '#C9FF8F',
  headerBgColor: '#197B22',
  headerFontSize: '20px',
  botBubbleColor: '#0F3789',
  headerFontColor: 'white',
  botFontColor: 'white',
  userBubbleColor: '#FF5733',
  userFontColor: 'white',
};

const App = () => {
  return (
    <header className="App-header">
      <ThemeProvider theme={theme}>
          <h1>ChatGPT MLB Assistant</h1>
          <ChatBot steps={steps} />
      </ThemeProvider>
    </header>
  );
}

export default App;