
import {useState, useEffect} from "react";
import {Center, ChakraProvider, Container, Heading,VStack,Text,HStack,Button,SimpleGrid,Image, Spinner,} from "@chakra-ui/react";

export default function App(){
  const [allPhotos, setAllPhotos] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isSelected, setIsSelected] = useState(false);
  const [uploadSuccessful, setUploadSuccessful] = useState(false);
  const [showSpinner, setShowSpinner] = useState(false);

  const onInputChange = (e) => {
    setIsSelected(true);
    setSelectedFile(e.target.files[0]);
  };
  const onFileUpload = (e) => {
    setShowSpinner(true);
    const formData = new FormData();
    formData.append("file", selectedFile, selectedFile.name);
    fetch("http://localhost:8000/photos",{
      method: "POST",
      body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success posting");
      setUploadSuccessful(!uploadSuccessful);
      setShowSpinner(false);
    });
  };

  useEffect(() =>{
    fetch("http://localhost:8000/photos")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      setAllPhotos(data);
    });
  },[uploadSuccessful]);
  return(
    <ChakraProvider>
      <Center bg="black" color="white" padding={8}>
        <VStack>
          <Heading>Your gallery</Heading>
          <Text>Take a look at all your photos!</Text>
          <HStack>
            <input type="file" onChange={onInputChange}></input>
            <Button size="lg" colorScheme="red" isDisabled={!isSelected} onClick={onFileUpload}>Upload photo</Button>
            {
              showSpinner && (
                <Center>
                  <Spinner size="xl"></Spinner>
                </Center>
              )
            }
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
