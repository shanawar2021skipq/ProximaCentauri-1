//import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import { Button,Text,Textarea, Heading,Input,useToast,
} from '@chakra-ui/react'  // CHAKRA UI
import {useState,useEffect} from 'react';

// API URL
const API='https://d92uek17m5.execute-api.us-east-2.amazonaws.com/prod' //beta stage

function App() {
  // Variables for ch
  const [data,setdata]=useState([])
  const [search,setSearchData]=useState(null)
  const [searchOutput,setSearchOutput]=useState(null)
  const [print,setprint]=useState(false)
  const [print1,setprint1]=useState(false)

  axios.get(API).then((response) => 
    {
      console.log(response.data)
      var urlsdata = response.data.split('[');
      var urlsdata = urlsdata[1].split(',');
      // Looping through Data 
      var loopData = ''
      var i = 0 ;
      while (i < urlsdata.length){
          loopData += `<li>${urlsdata[i]}</li>`
          i++;
      }
      console.log(loopData);// Putting data to console
      setdata(loopData) // Change data to loopdata
    });  

  // This function checks if search is in URLS List
  function check()
  {
    setprint1(false)
    if (data.includes(search))
    {
      setprint1(true)
      setSearchOutput('Successful, URL is in the list')
    }
    else
    {
      setprint1(true)
      setSearchOutput('Sorry, URL is not in the list')
    }
  }
  return (
    <>
    <center>
    <Heading mb={7} color='royalblue'>Web Crawler</Heading>  
    <Button onClick={check} colorScheme='blue'>Search</Button> 
    <Input placeholder='Search' onChange={(e)=>setSearchData(e.target.value)}/>   
    <Button onClick={()=>setprint(true)} colorScheme='blue'>Show URLs</Button>
    {  
      print?
      <> {<ul dangerouslySetInnerHTML={{__html: data}}></ul>}  </>
      :null
    }
    {  
      print1?
      <> {searchOutput} </>
      :null
    }
    </center>
    </>
  );
}
export default App;