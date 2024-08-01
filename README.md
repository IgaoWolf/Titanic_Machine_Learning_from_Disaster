# Titanic_Machine_Learning_from_Disaster
 Titanic - Aprendizado de máquina a partir de desastres


## Dicionário de dados
Variável	A definição	Chave
Sobrevivência 	Sobrevivência 	0 ? No, 1 ? Sim
pclass (classe) 	Aula de bilhetes 	1 ? 1st, 2 ? 2nd, 3 ? 3rd
Sexo 	Sexo 	
Idade 	Idade em anos 	
sibsp (piospo) 	Irmãos / cônjuges a bordo do Titanic 	
parch 	? de pais / filhos a bordo do Titanic 	
Bilhete de avião 	Número do bilhete 	
A tarifa 	A tarifa do passageiro 	
cabine 	Número da cabine 	
Embarcou 	O Porto de Embarque 	C ? Cherbourg, Q ? Queenstown, S? Southampton

## Notas de Variável

pclass (classe): Um proxy para o status socioeconômico (SES)
1o ? Superior
2o ? Meio
3o ? Mais baixo

Idade: A idade é fracionada se menor que 1. Se a idade é estimada, é na forma de xx.5

sibsp (piospo): O conjunto de dados define as relações familiares desta forma...
Irmão ? irmão, irmã, passo-irmão, stepirister
Cônjuge - marido, esposa (amante e noivas foram ignorados)

parch: O conjunto de dados define as relações familiares desta forma...
Pai ? mãe, pai
Criança - filha, filho, enteada, enteado
Algumas crianças viajaram apenas com uma babá, portanto, parch-0 para eles.