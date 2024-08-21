import re
import argostranslate.package
import argostranslate.translate




async def initializeTranslator(from_code:str = "en",to_code:str = "es"):
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())
    
    
def translate(texto:str,from_code:str = "en",to_code:str = "es"):
    translatedText = argostranslate.translate.translate(texto, from_code, to_code)
    return str(translatedText)

def cleanTXT(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r'http\S+', '', texto)
    texto = re.sub(r'[^a-z0-9\s.,;:?!\'()-]', ' ', texto)
    texto = re.sub(r'\.{2,}', '.', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    texto = re.sub(r'•.*\n?', '', texto)
    texto = re.sub(r'\[[^\]]+\]', '', texto)
    texto = re.sub(r'\"[^\"]+\"', '', texto)
    texto = re.sub(r'\(\d{4}, [^\)]+\)', '', texto)
    texto = re.sub(r'\b(?:[a-z]\.){2,}', '', texto)
    texto = re.sub(r'references?\s+".*?"', '', texto)
    return texto