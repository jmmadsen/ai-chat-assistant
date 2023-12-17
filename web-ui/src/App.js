import './App.css';

import React, { Component } from 'react';
import ChatBot from 'react-simple-chatbot';
import { ThemeProvider } from 'styled-components';
import axios from 'axios';


// query db or docs chain and return answer
class Answer extends Component {

  constructor(props) {
    super(props);

    this.state = {
      type: props.type
    };
  }
  
  async componentDidMount() {
    const res = await axios.get(`http://localhost:5000/${this.props.type}_chain_query`);
    // after receiving API response, trigger next message (changing waitAction)
    this.props.triggerNextStep({ value: res.data, trigger: `${this.props.type}-res` });
  }

  render = () => <div>Thinking, give me a second...</div>
}

// message chain from bot
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
    trigger: 'database-res',
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
    id: 'database-res',
    message: '{previousValue}',
    trigger: 1
  },
  {
    id: 'docs-res',
    message: '{previousValue}',
    trigger: 1
  }
];

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

function App() {
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