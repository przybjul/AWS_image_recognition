import logo from './logo.svg';
import './App.css';
import {useState, useEffect} from "react";
import {Center, ChakraProvider, Container, Heading,VStack,Text,HStack,Button,SimpleGrid,Image} from "@chakra-ui/react";

export default function App(){
  const [allPhotos, setAllPhotos] = useState([]);

  useEffect(() =>{
    fetch("http://localhost:8000/photos")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      setAllPhotos(data);
    });
  },[]);
  return(
    <ChakraProvider>
      <Center bg="black" color="white" padding={8}>
        <VStack>
          <Heading>Your gallery</Heading>
          <Text>Take a look at all your photos!</Text>
          <HStack>
            <input type="file" onChange={null} onClick={null}></input>
            <Button size="lg" colorScheme="red" isDisabled={null} onClick={null}>Upload photo</Button>
          </HStack>
          <Heading>Your photos</Heading>
          <SimpleGrid columns={3} spacing={8}>
            {
              allPhotos.map(photo =>{
                console.log(photo["photo_url"])
                return(
                  <Image borderRadius={25} boxSize="300px" src={photo["photo_url"]} fallbackSrc="https://via.placeholder.com/150" objFit="cover"></Image>
                )
              }) 
            }
          </SimpleGrid>
        </VStack>
      </Center>
    </ChakraProvider>
  );
}

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;
