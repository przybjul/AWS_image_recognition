# AWS_image_recognition
https://youtu.be/dqCGewXc-j0

W poniższym sprawozdaniu opisano projekt umożliwiający rozpoznanie obrazu z wykorzystaniem
rozwiązań chmurowych AWS. Implementację wykonano jako aplikację webową z użyciem Pythona,
PostreSQL, FastAPI oraz Reacta. Aplikacja posiada dwie główne funkcjonalności: analizę zdjęcia osoby
oraz transkrypcja załączonego zdjęcia. Upload obrazu odbywa się do Storage S3, następnie zdjęcie
jest poddawane analizie. Dla pierwszej funkcjonalności wykorzystano technologię deep-learning
Amazon Rekognition, natomiast dla drugiej – Amazon Textract - jest to serwis, który automatycznie
wykrywa i ekstrahuje tekst z zeskanowanego zdjęcia.
