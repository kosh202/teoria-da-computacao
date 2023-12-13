class AutomatoFinito:
    def __init__(self):
        self.alfabeto = set()
        self.estados = set()
        self.estado_inicial = None
        self.estados_finais = set()
        self.transicoes = {}
        self.palavras = []

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

        for i, simbolo in enumerate(palavra):
            print(f"\nProcessando símbolo '{simbolo}':")
            print(f"Estados atuais: {estados_atuais}")

            if simbolo not in self.alfabeto:
                print(f'Erro: Símbolo "{simbolo}" não está no alfabeto.')
                return False

            novos_estados = set()

            for estado_atual in estados_atuais:
                destinos = set()

                # Adiciona o movimento vazio ('') para estados que não têm transições com o símbolo específico
                destinos.update(self.transicoes[estado_atual].get('', set()))

                if estado_atual in self.transicoes and simbolo in self.transicoes[estado_atual]:
                    destinos.update(self.transicoes[estado_atual][simbolo])

                fecho_destinos = self.fechamento_transitivo(destinos)
                novos_estados.update(fecho_destinos)

            estados_atuais = novos_estados

        # Verifique se algum estado atual é final
        if any(estado in self.estados_finais for estado in estados_atuais):
            print(f"\nEstados finais possíveis: {estados_atuais}")
            return True
        else:
            print(f"\nEstados finais possíveis: {estados_atuais}")
            return False

    def reconhecer_palavras(self):
        for palavra in self.palavras:
            if self.reconhecer_palavra(palavra):
                print(f'M aceita a palavra <{palavra}>')
            else:
                print(f'M rejeita a palavra <{palavra}>')


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


if __name__ == "__main__":
    main()
