import React,{useEffect} from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import { Widget, addResponseMessage,renderCustomComponent } from 'react-chat-widget';
import Menu  from './Menu';
import 'react-chat-widget/lib/styles.css';
import logo from './dua.jpg';
import './App.css';
var flag = true;

function App() {
  useEffect(() => {
    // addResponseMessage('How may i help you?');
    renderCustomComponent(Menu)
  }, []);

  const handleNewUserMessage = async (newMessage) => {
    if(newMessage == '**'){
      flag = !flag;
      console.log('flag', flag);
      var model = flag ? "Intent Model" : 'Conversational Model'
      addResponseMessage('Model switched to ' + model);
      return
    }
    if(flag){
      console.log(`New message incoming! ${newMessage}`);
    // Now send the message throught the backend API
    const response = await axios.post('http://localhost:8000  /intent',{
      chat: newMessage
    });
    console.log('response', response.data.intent);
    const intent = 'Intention: ' + response.data.intent;
    // const probability = 'Probability: ' + response.data.probability.toFixed(2) + ' %'
    const ans = 'Reply:' +response.data.reply
    const reply = intent +'\n' + ans
    addResponseMessage(reply);
    // addResponseMessage(probability)
    }else{
     
    const response = await axios.post('http://localhost:5000/intent',{
      query: newMessage
    });
    if(typeof response.data.answers !== 'undefined' && response.data.answers.length > 0){
      console.log(response.data.answers[0]);
      const reply = response.data.answers[0].answer;
      addResponseMessage(reply);
    }else{
      addResponseMessage("Please rephrase your questions!")
    }
    
    // addResponseMessage(probability)
    }
    

  };
  return (
    <div className="App">
      <Widget 
              handleNewUserMessage={handleNewUserMessage}
              profileAvatar={logo}
          title="BERT Based Chatbot"
          subtitle=""

      />
    </div>
  );
}

export default App;
