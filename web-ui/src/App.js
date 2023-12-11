import './App.css';

import React, { Component } from 'react';
import ChatBot from 'react-simple-chatbot';
import { ThemeProvider } from 'styled-components';
import axios from 'axios';


// query db chain and return answer
class DBAnswer extends Component {

  constructor(props) {
    super(props);

    this.state = {
      dbResponse: ''
    };
  }
  
  async componentWillMount() {
    const res = await axios.get('http://localhost:5000/db_chain_query');
    this.setState({dbResponse: res.data})
  }

  render() {
    const { dbResponse } = this.state;
    return <div>{dbResponse}</div>
  }
}

// query docs chain and return answer
class DocsAnswer extends Component {

  constructor(props) {
    super(props);

    this.state = {
      docsResponse: ''
    };
  }
  
  async componentWillMount() {
    const res = await axios.get('http://localhost:5000/docs_chain_query');
    this.setState({docsResponse: res.data})
  }

  render() {
    const { docsResponse } = this.state;
    return <div>{docsResponse}</div>
  }
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
      { value: 'Query the database', label: 'Query the database', trigger: 'database' },
      { value: 'General question', label: 'General question', trigger: 'docs' }
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
    component: <DBAnswer/>,
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
    component: <DocsAnswer/>,
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
