# Lancement

Pour tester avec le serveur de test MercaNET, les paramètres sont ceux par défaut dans `settings.py`.
Il vous faudrait cependant définir la variable d'environnement `MERCANET_REPONSE_AUTO_URL` à la valeur `http://votre-ip-publique/mercanet/auto/`.

Votre serveur de développement doit pourvoir reçevoir des requêtes POST depuis Internet ...
* Soit vous fait du Port-Forward sur votre Box (attention au Firewall à modifier et à remettre comme avant ainsi que le port-forward)
* soit vous utilisez [*ngrok*](https://ngrok.com/) (il a une fonction d'interception & replay pratique) ou [*ultrahook*](http://www.ultrahook.com/)

## Autres outils:
`mitm-proxy` (Python) permet d'intercepter et rejouer des requêtes comme ngrok mais sur votre machine. Permet de ne pas avoir à refaire 
un faux paiement sur Mercanet-test à chaque fois qu'on veut tester le code de réponse automatique