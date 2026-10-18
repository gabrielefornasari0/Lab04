class Espositori:
    """Rappresenta un espositore registrato al centro fieristico."""

    def __init__(self, codiceE, nome, cognome):
        # Inizializzazione degli attributi protetti (prefisso _)
        self._codiceE = str(codiceE)
        self._nome = nome
        self._cognome = cognome

    # Property per accedere in sola lettura agli attributi incapsulati
    @property
    def codiceE(self):
        return self._codiceE

    @property
    def nome(self):
        return self._nome

    @property
    def cognome(self):
        return self._cognome

    def __eq__(self, other):
        """Confronta due oggetti Espositori in base al codice univoco."""
        if isinstance(other, Espositori):
            return self._codiceE == other._codiceE
        return False

    def __repr__(self):
        """Rappresentazione in stringa dell'espositore."""
        return f'Espositore: {self._codiceE}, nome: {self._nome}, cognome: {self._cognome}'


class Stand:
    """Classe base che rappresenta uno stand generico."""

    def __init__(self, codiceS, superficie, padiglione, prezzo_base):
        self._codiceS = str(codiceS)
        self._superficie = int(superficie)
        self._padiglione = padiglione
        self._prezzo_base = int(prezzo_base)
        # Di default uno stand parte libero (nessun espositore assegnato)
        self._espositore = None

    @property
    def codiceS(self):
        return self._codiceS

    # Property e Setter per gestire l'assegnazione dell'espositore allo stand
    @property
    def espositore(self):
        return self._espositore

    @espositore.setter
    def espositore(self, esp):
        self._espositore = esp

    def calcola_prezzo(self):
        """Restituisce il prezzo base dello stand (metodo sovrascritto nelle sottoclassi)."""
        return self._prezzo_base

    def __lt__(self, other):
        """Consente l'ordinamento tra stand (<) basandosi sul prezzo finale calcolato."""
        if isinstance(other, Stand):
            return self.calcola_prezzo() < other.calcola_prezzo()

    def __repr__(self):
        """Rappresentazione in stringa dello stand base."""
        return f'Stand:{self._codiceS}--Superficie:{self._superficie} m^2--Padiglione:{self._padiglione}-Prezzo:{self.calcola_prezzo()} euro'


class StandElettrici(Stand):
    """Sottoclasse di Stand dotata di prese elettriche aggiuntive."""

    def __init__(self, codiceS, superficie, padiglione, prezzo_base, prese_extra):
        # Invocazione del costruttore della classe padre Stand
        super().__init__(codiceS, superficie, padiglione, prezzo_base)
        self._prese_extra = int(prese_extra)

    def calcola_prezzo(self):
        """Calcola il prezzo aumentandolo del 7% del prezzo base per ogni presa extra."""
        return self._prezzo_base * (1 + 0.07 * self._prese_extra)

    def __repr__(self):
        """Rappresentazione in stringa dello stand elettrico."""
        return f'Stand:{self._codiceS}--Superficie:{self._superficie} m^2--Padiglione:{self._padiglione}-Prezzo :{self.calcola_prezzo()} euro-Prese extra:{self._prese_extra}'


class StandPremium(Stand):
    """Sottoclasse di Stand situata in una posizione privilegiata."""

    def __init__(self, codiceS, superficie, padiglione, prezzo_base, posizione):
        # Invocazione del costruttore della classe padre Stand
        super().__init__(codiceS, superficie, padiglione, prezzo_base)
        self.__posizione = str(posizione)

    def calcola_prezzo(self):
        """Calcola il prezzo applicando una maggiorazione fissa del 30%."""
        return self._prezzo_base * 1.30

    def __repr__(self):
        """Rappresentazione in stringa dello stand premium."""
        return f'Stand:{self._codiceS}--Superficie:{self._superficie} m^2--Padiglione:{self._padiglione}-Prezzo :{self.calcola_prezzo()} euro-Posizione:{self.__posizione}'


class LingottoFiere:
    """Classe principale che gestisce il centro fieristico, gli stand e gli espositori."""

    def __init__(self, nome):
        """Inizializza il nome della struttura e le liste private per contenere i dati."""
        self.__nome = nome
        self.__stands = []
        self.__espositori = []

    # Getter e Setter per il nome del centro fieristico
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    def carica_file_dati(self, file_path):
        """Legge il file CSV e istanzia dinamicamente gli oggetti Stand o Espositori."""
        with open(file_path) as file:
            for riga in file:
                # Rimozione di spazi/a capo e suddivisione dei valori separati da virgola
                dati = riga.strip().split(',')

                # Identificazione delle righe dedicate agli Stand (codice che inizia per 'ST')
                if dati[0].startswith('ST'):
                    if len(dati) == 4:
                        # Stand base (Codice, Superficie, Padiglione, Prezzo)
                        stand = Stand(dati[0], dati[1], dati[2], dati[3])
                    elif len(dati) == 5:
                        # Distinzione tra StandElettrici (5° valore numerico) e StandPremium (5° valore testuale)
                        if dati[4].isdigit():
                            stand = StandElettrici(dati[0], dati[1], dati[2], dati[3], dati[4])
                        else:
                            stand = StandPremium(dati[0], dati[1], dati[2], dati[3], dati[4])
                    # Aggiunta dello stand creato alla lista interna
                    self.__stands.append(stand)
                else:
                    # Identificazione delle righe dedicate agli Espositori (codice che inizia per 'ES')
                    espositore = Espositori(dati[0], dati[1], dati[2])
                    self.__espositori.append(espositore)

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand disponibile ad un espositore eseguendo i controlli di validità."""

        # 1. Ricerca dello stand specificato nella lista
        assegno_stand = None
        for codici in self.__stands:
            if codici.codiceS == codice_stand:
                assegno_stand = codici
                break

        if assegno_stand is None:
            raise ValueError("Codice stand non trovato")

        # 2. Ricerca dell'espositore specificato nella lista
        assegno_espositore = None
        for codici in self.__espositori:
            if codici.codiceE == codice_espositore:
                assegno_espositore = codici
                break

        if assegno_espositore is None:
            raise ValueError("Codice espositore non trovato")

        # 3. Controllo se lo stand è già stato assegnato a un altro espositore
        if assegno_stand.espositore is not None:
            raise ValueError("Stand già assegnato")

        # 4. Controllo che l'espositore non possieda già un altro stand
        for st in self.__stands:
            if st.espositore == assegno_espositore:
                raise ValueError('Espositore già assegnato')

        # Se tutte le verifiche hanno successo, viene registrata l'associazione
        assegno_stand.espositore = assegno_espositore

    def elenca_espositori(self):
        """Stampa l'elenco di tutti gli espositori indicando il rispettivo stand (se assegnato)."""
        for esp in self.__espositori:
            stand_associato = None

            # Cerca se l'espositore corrente risulta assegnato a uno degli stand
            for st in self.__stands:
                if st.espositore == esp:
                    stand_associato = st.codiceS
                    break

            # Stampa il risultato del controllo
            if stand_associato is not None:
                print(f'{esp}---->{stand_associato}')
            else:
                print(f'{esp}---->Non associato')

    def stand_ordinati_per_prezzo(self):
        """Restituisce una nuova lista di stand ordinata in ordine crescente di prezzo usando __lt__."""
        return sorted(self.__stands)