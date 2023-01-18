# Patient Digital Twin

## Synopsis

Il presente lavoro consiste in una proof-of-concept di un sistema di machine learning a supporto di problematiche bioinformatiche che integra in esso elementi di tecnologie cloud-computing. L'uso di tecnologie Digital Twin ha conquistato diverse aree di ricerca; diversi sono stati i tentativi di rappresentazione di un "gemello digitale" per un paziente, che modelli per esso ogni singolo dettaglio, dalle caratteristiche genomiche alle esposizioni del paziente. 

l seguente lavoro fa riferimento alla proposta di Patient Twin di Pietro Barbiero. Per tale applicazione, qui è fornita una prova concettuale che integra in essa elementi di tecnologie cloud: un'applicazione web realizzata in Flask, per fornire l'accesso ai risultati dell'applicazione, nonchè grafici riguardanti il forecasting di endpoint sanitari rilevanti, pressione sanguigna e sistema renina-angiotensina (RAS)

L’architettura proposta prevede di realizzare un’immagine Docker contenente tutte le dipendenze necessarie per poter permettere agli script Python pre-esistenti, forniti dagli accademici autori della repository originale, di essere lanciati senza problemi, in maniera portabile e sicura. Fra le dipendenze pre-installate sull’immagine Docker si annoverano pytorch, numpy e pandas. L’immagine Docker viene generata ogni volta che un collaboratore alla repository effettua una push via GitHub. Il trigger della push permette di inizializzare una routine di CI/CD implementata via GitHub Actions.

Una volta creata l’immagine, essa viene pubblicata su Elastic Container Registry, per poi essere containerizzata e deployata su Elasting Container Service. Il riferimento dell’immagine appena caricata viene in effetti integrata come task definition su ECS. Una volta deployato il container sul cluster Fargate, il
procedimento e concluso e il Digital Twin Provider e pronto ad essere utilizzato dagli utenti finali. 

Il frontend dell’applicazione ha lo scopo di permettere un minimo e limitato grado di interazione con il Digital Twin Provider ed è reso disponibile nel contesto di un container Docker portabile e isolato rispetto al resto del sistema operativo. La virtualizzazione, in questo caso, permette di installare pacchetti Python critici per il funzionamento del backend, come flask e flask-cors, senza contaminare la macchina ospitante
e incorrere in potenziali problemi di versioning.

## Build

[![Deploy to Amazon ECS](https://github.com/antoniogrv/mlops-patient-digital-twin/actions/workflows/__DEPLOY-ECR-ECS.yml/badge.svg)](https://github.com/antoniogrv/mlops-patient-digital-twin/actions/workflows/__DEPLOY-ECR-ECS.yml)

```
docker build --tag mlops-pdt .
docker run --publish 80:80 mlops-pdt
```
