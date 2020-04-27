# Lancement

Pour tester avec le serveur de test MercaNET, les paramètres sont ceux par défaut dans `settings.py`.
Il vous faudrait cependant définir la variable d'environnement `MERCANET_REPONSE_AUTO_URL` à la valeur `http://votre-ip-publique/mercanet/auto/`.

Votre serveur de développement doit pourvoir reçevoir des requêtes POST depuis Internet ...
* Soit vous fait du Port-Forward sur votre Box (attention au Firewall à modifier et à remettre comme avant ainsi que le port-forward)
* soit vous utilisez [*ngrok*](https://ngrok.com/) (il a une fonction d'interception & replay pratique) ou [*ultrahook*](http://www.ultrahook.com/)

## Autres outils:
`mitm-proxy` (Python) permet d'intercepter et rejouer des requêtes comme ngrok mais sur votre machine. Permet de ne pas avoir à refaire 
un faux paiement sur Mercanet-test à chaque fois qu'on veut tester le code de réponse automatique

```shell script
mitmproxy --listen-host 0.0.0.0 --listen-port 7000 --mode upstream:http://127.0.0.1:8000
```
## Documentation mercanet
En fait la BNP utilise [Worldline SIPS](https://documentation.sips.worldline.com/fr/WLSIPS.317-UG-Sips-Paypage-POST.html)
## Étrangetés de MercaNET
C'est nous qui choisissons l'algorithme de chiffrement utilisé pour la génération des Seals. MercaNET utilisera le même.

 **Attention:** si on ne spécifie pas l'algo, c'est *HMAC-SHA-256* qui est utilisé pour la 1e requête,
 et *SHA-256* pour la réponse automatique (défaut pour la réponse https://documentation.sips.worldline.com/fr/WLSIPS.316-UG-Sips-Paypage-JSON.html#ariaid-title52)...
 
 # Notes
 On peut faire mémoriser des données à Mercanet via les champs `returnContext` (max. 255 caractères) et `orderId` (max. 32 caractères). Peut être utile pour des vérifications