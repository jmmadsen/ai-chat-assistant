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
      type: props.type,
      dbResponse: ''
    };
  }
  
  async componentWillMount() {
    const res = await axios.get(`http://localhost:5000/${this.props.type}_chain_query`);
    this.setState({dbResponse: res.data})
  }

  render = () => <div>{this.state.dbResponse}</div>
}

// message chain from bot
const steps = [
  {
    id: '0',
    message: 'Hey there! I am your 2023 MLB season AI assistant.',
    trigger: '1',
  },
  {
    id: '1',
    message: 'Would you like to query the batting database, or ask a general question about the season?',
    trigger: '2',
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
    trigger: 'database-q',
  },
  {
    id: 'database-q',
    user: true,
    trigger: 'database-res',
  },
  {
    id: 'database-res',
    component: <Answer type={'db'}/>,
    asMessage: true,
    trigger: '1',
  },
  {
    id: 'docs',
    message: `Please enter your question about this season:`,
    trigger: 'docs-q',
  },
  {
    id: 'docs-q',
    user: true,
    trigger: 'docs-res',
  },
  {
    id: 'docs-res',
    component: <Answer type={'docs'}/>,
    asMessage: true,
    trigger: '1',
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