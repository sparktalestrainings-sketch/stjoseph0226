#pip install tiktoken , developer has to install this package
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
import tiktoken as tt
encoder=tt.encoding_for_model('gpt-4o-mini')
mytext='Hello gpt how are you'
tokens=encoder.encode(mytext)
print(tokens)
#text=encoder.decode(tokens)
text=encoder.decode([13225, 329, 555, 1495, 553, 481,5678])
print(text)