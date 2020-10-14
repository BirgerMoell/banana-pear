import React, { useEffect, useState } from 'react';
import './App.css';

function App() {

  return (
    <div className="App">
      <header className="App-header">

        <AnalyzeAudio />
      </header>
    </div>
  );
}



function AnalyzeAudio() {

  const [file, setFile] = useState();
  const [fileUrl, setFileUrl] = useState();
  const [answer, setAnswer] = useState();

  useEffect(() => {
    const inputElement = document.getElementById("input");
    inputElement.addEventListener("change", handleFiles, false);

  });

  function handleFiles() {
    const fileList = this.files; /* now you can work with the file list */
      console.log("the files are fileList", fileList);
      setFile(fileList[0]);
      setFileUrl(URL.createObjectURL(fileList[0]));
  }


  const sendFileToServer = async () => {
    //setAnswer("Thats' a banana!")

    var data = new FormData()
    data.append('file', file)

    let response = await fetch('http://localhost:8082/predict', {
        method: 'POST',
        body: data
    })

    console.log("the response is", response)
    let responseJson = await response.json()

    console.log("the response is", responseJson)
    if (responseJson) {
      setAnswer("Thats' a " + responseJson.prediction)
    }

  }






  return (

      <div>
        <p>Pear or Banana</p>
        <input id="input" type="file" />
        

        {file && <div>

          <img src={fileUrl} height="300px" width="300px"/>

          <hr></hr>
        
        { !answer && <button onClick={sendFileToServer}>Figure it out</button> }
        { answer && <p>{answer}</p>}
        
        </div>
        }

      </div>

    

  )
}



export default App;
