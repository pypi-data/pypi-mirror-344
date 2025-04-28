import hashlib

def ler_e_converter_binario(arquivo):
    if arquivo == '_bin_/sniff.py':
     print(f"the file : {arquivo} is not sniffed")
    elif arquivo == '_bin_/sub.py':
     print(f"the file : {arquivo} is not sniffed")
    else:
        try:
          with open(arquivo, 'rb') as f:
            conteudo = f.read()  # Lê o conteúdo do arquivo binário
        
          texto_convertido = ""
        
          for byte in conteudo:
            # Se o byte for imprimível (entre 32 e 126 no ASCII)
            if 32 <= byte <= 126:
                texto_convertido += chr(byte)
            else:
                # Para bytes não imprimíveis, colocamos um ponto
                texto_convertido += '.'
        
        # Verifica se o conteúdo convertido é vazio, caso sim, retorna "Arquivo vazio ou não legível"
          if not texto_convertido.strip():
            return "Arquivo vazio ou não legível"
        
          return texto_convertido
        except Exception as e:
          return f"Erro ao ler o arquivo: {e}"
def sf(string_code):
    sha256_arqv = hashlib.sha256()
    if string_code == '_bin_/sniff.py':
     print(f"the file : {string_code} is not convert")
    elif string_code == '_bin_/sub.py':
     print(f"the file : {string_code} is not convert")
    else:
        try:
          with open(string_code, 'rb') as f:
            while chunk := f.read(4096):
                sha256_arqv.update(chunk)
                return sha256_arqv.hexdigest()
        except Exception as e:
          return f"error : {e}"
# Exemplo de uso

class sniff_lib:
 def scan_bin(self,string_file):
   self.string_file = string_file
   resultado = ler_e_converter_binario(self.string_file)
   print(resultado)  
 def convert_sha256(self,string_file):
   self.string_file = string_file
   print(f"sha256 : {sf(self.string_file)} for arqv : {self.string_file}")