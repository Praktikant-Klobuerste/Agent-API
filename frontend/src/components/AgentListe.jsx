// AgentListe.js
import React, { useState, useEffect } from 'react';

function AgentListe() {
  const [agentenDaten, setAgentenDaten] = useState(null);

  useEffect(() => {
    // Funktion, die den GET-Request durchführt
    const fetchAgentenDaten = async () => {
      try {
        const response = await fetch('http://localhost:5000/agent');
        const daten = await response.json();
        setAgentenDaten(daten);
      } catch (fehler) {
        console.error('Fehler beim Abrufen der Daten:', fehler);
      }
    };

    // Aufruf der Funktion
    fetchAgentenDaten();
  }, []); // Leeres Array als Abhängigkeit bedeutet, dass es nur einmal beim Montieren aufgerufen wird

  return (
    <div>
      <h1>Agenten Daten</h1>
      {agentenDaten ? (
        <div>
          {agentenDaten.map((agent) => (
            <div key={agent.id}>
              <p>ID: {agent.id}</p>
              <p>Name: {agent.name}</p>
              <p>Augenfarbe: {agent.eye_color}</p>
              <hr />
            </div>
          ))}
        </div>
      ) : (
        <p>Lade Daten...</p>
      )}
    </div>
  );
}

export default AgentListe;
