import './App.css';
import Title from './components/Title';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Title header="Meine erste React-Komponente"
                description="Hallo Welt"/>
      </header>
    </div>
  );
}

export default App;
