import './App.css';
import Title from './components/Title';
import AgentListe from './components/AgentListe';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <Title header="Meine erste React-Komponente"
                description="Hallo Welt"/> */}
      <AgentListe/>
      </header>
    </div>
  );
}

export default App;
