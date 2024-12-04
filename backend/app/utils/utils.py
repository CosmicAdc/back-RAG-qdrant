import re

from langchain_text_splitters import RecursiveCharacterTextSplitter
import langid
import argostranslate.package
import argostranslate.translate


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=50,
)


async def initializeTranslator(from_code:str = "en",to_code:str = "es"):
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())
    
def translate(text:str,from_code:str = "en",to_code:str = "es"):
    translatedText = argostranslate.translate.translate(text, from_code, to_code)
    return str(translatedText)


def detect_idiom(text:str):
    language, _ = langid.classify(text)
    return language    
    


def cleanTXT(texto: str) -> str:
    texto = texto.lower() # Convierte el texto a minúsculas
    texto = re.sub(r'http\S+', '', texto) # Elimina las URLs
    texto = re.sub(r'[^a-zA-Z0-9\s.,;:?!\'()€$áéíóúÁÉÍÓÚñÑ-]', ' ', texto)# Reemplaza caracteres no alfanuméricos por espacios
    texto = re.sub(r'\.{2,}', '.', texto) # Reemplaza puntos consecutivos por un solo punto
    texto = re.sub(r'\s+', ' ', texto).strip() # Elimina espacios en blanco adicionales y espacios al principio y al final
    texto = re.sub(r'•.*\n?', '', texto) # Elimina viñetas y el texto que las sigue
    texto = re.sub(r'\[[^\]]+\]', '', texto) # Elimina texto entre corchetes
    texto = re.sub(r'\"[^\"]+\"', '', texto) # Elimina texto entre comillas dobles
    texto = re.sub(r'\(\d{4}, [^\)]+\)', '', texto) # Elimina fechas entre paréntesis
    texto = re.sub(r'\b(?:[a-z]\.){2,}', '', texto) # Elimina abreviaturas con más de dos puntos
    return texto