import React from 'react';

function Title(props) {
  return (
    <div>
      <h1>{props.header}</h1>
      <p>{props.description}</p>
    </div>
  );
}

export default Title;
