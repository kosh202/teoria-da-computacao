#dupla  luiz e raphael

class AutomatoFinito:
    def __init__(self):
        self.alfabeto = set()
        self.estados = set()
        self.estado_inicial = None
        self.estados_finais = set()
        self.transicoes = {}
        self.palavras = []
        self.resultados = []

    def carregar_automato(self, arquivo):
        with open(arquivo, 'r') as file:
            for line in file:
                self.processar_linha(line)

    def processar_linha(self, line):
        line = line.strip()
        partes = line.split()

        tipo = partes[0]
        if tipo == '#':
            return  # Linha de comentário, ignorar
        elif tipo == 'A':
            self.alfabeto = set(partes[1:])
        elif tipo == 'Q':
            self.estados = set(partes[1:])
        elif tipo == 'q':
            self.estado_inicial = partes[1]
        elif tipo == 'F':
            self.estados_finais = set(partes[1:])
        elif tipo == 'T':
            origem, simbolo, destino = partes[1:4]

            # Considera "ê" como transição vazia
            simbolo = simbolo.replace('Ãª', '', )

            if origem not in self.transicoes:
                self.transicoes[origem] = {}
            if simbolo not in self.transicoes[origem]:
                self.transicoes[origem][simbolo] = set()
            if destino not in self.transicoes[origem][simbolo]:
                self.transicoes[origem][simbolo].add(destino)
        elif tipo == 'P':
            self.palavras.append(partes[1])

            # Adiciona o movimento vazio ('') para estados que não têm transições com um símbolo específico
            for estado in self.estados:
                if estado not in self.transicoes:
                    self.transicoes[estado] = {}
                for simbolo in self.alfabeto:
                    if simbolo not in self.transicoes[estado]:
                        self.transicoes[estado][simbolo] = set()
                if '' not in self.transicoes[estado]:
                    self.transicoes[estado][''] = set()

    def fechamento_transitivo(self, estados):
        fecho = set(estados)
        pilha = list(estados)

        while pilha:
            estado_atual = pilha.pop()
            if estado_atual in self.transicoes and '' in self.transicoes[estado_atual]:
                destinos = self.transicoes[estado_atual]['']
                novos_destinos = destinos - fecho
                fecho.update(novos_destinos)
                pilha.extend(novos_destinos)

        return fecho

    def reconhecer_palavra(self, palavra):
        estados_atuais = self.fechamento_transitivo({self.estado_inicial})
        resultado = ""
        #resultado = f"Reconhecendo palavra <{palavra}>:\n"

        for i, simbolo in enumerate(palavra):
            #resultado += f"\nProcessando símbolo '{simbolo}':\n"
            #resultado += f"Estados atuais: {estados_atuais}\n"

            if simbolo not in self.alfabeto:
                resultado += f'Erro: Símbolo "{simbolo}" não está no alfabeto.\n'
                resultado += f"M rejeita a palavra <{palavra}>\n"
                self.resultados.append(resultado)
                return False

            novos_estados = set()

            for estado_atual in estados_atuais:
                destinos = set()

                # Adiciona o movimento vazio ('') para estados atuais
                destinos.update(self.transicoes[estado_atual].get('', set()))

                if estado_atual in self.transicoes and simbolo in self.transicoes[estado_atual]:
                    destinos.update(self.transicoes[estado_atual][simbolo])

                fecho_destinos = self.fechamento_transitivo(destinos)
                novos_estados.update(fecho_destinos)

            estados_atuais = novos_estados

        # Verifique se algum estado atual é final
        if any(estado in self.estados_finais for estado in estados_atuais):
            #resultado += f"\nEstados finais possíveis: {estados_atuais}\n"
            resultado += f"M aceita a palavra <{palavra}>\n"
        else:
            #resultado += f"\nEstados finais possíveis: {estados_atuais}\n"
            resultado += f"M rejeita a palavra <{palavra}>\n"

        self.resultados.append(resultado)
        return True

    def reconhecer_palavras(self):
        for palavra in self.palavras:
            self.reconhecer_palavra(palavra)

    def salvar_resultados(self, arquivo):
        with open(arquivo, 'w') as file:
            for resultado in self.resultados:
                file.write(resultado)


def main():
    automato = AutomatoFinito()
    automato.carregar_automato("texto.txt")

    print("Autômato:")
    print(f"Alfabeto: {automato.alfabeto}")
    print(f"Estados: {automato.estados}")
    print(f"Estado Inicial: {automato.estado_inicial}")
    print(f"Estados Finais: {automato.estados_finais}")
    print(f"Transições: {automato.transicoes}")
    print(f"Palavras: {automato.palavras}")

    print("\nReconhecendo Palavras:")
    automato.reconhecer_palavras()

    automato.salvar_resultados("resultados.txt")


if __name__ == "__main__":
    main()
