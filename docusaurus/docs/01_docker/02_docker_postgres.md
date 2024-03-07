---
sidebar_position: 3
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# PostgreSQL & pgAdmin mit Docker

## Normal Docker

:::info

Installierte [Docker](https://www.docker.com/products/docker-desktop/) auf Ihrem System.

Nützliche links: 
- [How to Run PostgreSQL and pgAdmin Using Docker](https://www.commandprompt.com/education/how-to-run-postgresql-and-pgadmin-using-docker/)
- [Stackoverflow: docker postgres pgadmin local connection](https://stackoverflow.com/questions/25540711/docker-postgres-pgadmin-local-connection?page=1&tab=scoredesc#tab-top)
- [Teclado](https://rest-apis-flask-python-ln6cqvntr-teclado.vercel.app/)
  :::

### Schritt 1: PostgreSQL-Image herunterladen

Öffne das Terminal und führe den folgenden Befehl aus, um das offizielle Postgres-Image zu ziehen:

```bash
docker pull postgres
```

Link: [postgres - docker hub](https://hub.docker.com/_/postgres).

![docker-pull-postgres](../assets/docker-pull-postgres.png)

### Schritt 2: PostgreSQL-Container starten

Starte einen Postgres-Container mit einem festgelegten Passwort für den `postgres`-Benutzer:

<Tabs groupId="run-code">
  <TabItem value="clear" label="Clear">

    ```bash
    docker run \
    --name <container-postgresdb> \
    -p 5432:5432 \
    -e POSTGRES_USER: <username> \ #default postgres
    -e POSTGRES_PASSWORD=<password> \
    --restart unless-stopped \ #optional
    -d postgres
    ```

  </TabItem>
  
  <TabItem value="copy" label="Copy">
    ```bash
    docker run --name container-postgresdb -p 5432:5432 -e POSTGRES_USER:username -e POSTGRES_PASSWORD=password --restart unless-stopped -d postgres
    ```
  </TabItem>
</Tabs>

Ersetze `<username>` (oder entferne flag), `<password>` und `<container-postgresdb>`.

<details>
  <summary>
    Erklärung
   </summary>

  <div>
- `--name <container-postgresdb>`: Gibt dem Container den Namen `<container-postgresdb>`.
- `-p 5432:5432`: Mappt den Port 5432 vom Host auf den Container.
- `-e POSTGRES_PASSWORD=<password>`: Setzt das Passwort für den eingetragenen User.
- `--restart unless-stopped`: Container wird neugestartet, außer er wird manuell gestoppt.
- `-d postgres`: Startet den Container im Hintergrund mit dem Docker-Image "postgres".

![docker-pull-postgres](../assets/docker-run-postgres.png)

</div>
</details>

### Schritt 3: pgAdmin4-Image herunterladen

Lade das pgAdmin4-Image herunter:

```bash
docker pull dpage/pgadmin4
```

Link: [pgAdmin - docker hub](https://hub.docker.com/r/dpage/pgadmin4).

![docker-pull-postgres](../assets/docker-pull-pgadmin.png)

### Schritt 4: pgAdmin4-Container starten

Erstellen und starte einen pgAdmin4-Container:

<Tabs groupId="run-code">
  <TabItem value="clear" label="Clear">
    ```bash
    docker run \
    --name <container-pgadmin> \
    -p 82:80 \
    -e "PGADMIN_DEFAULT_EMAIL=<name@example.com>" \
    -e "PGADMIN_DEFAULT_PASSWORD=<password>" \
    -d dpage/pgadmin4
    ```
    </TabItem>

  <TabItem value="copy" label="Copy">
    ```bash
    docker run --name <container-pgadmin> -p 82:80 -e "PGADMIN_DEFAULT_EMAIL=<name@example.com>" -e "PGADMIN_DEFAULT_PASSWORD=<password>" -d dpage/pgadmin4
    ```
  </TabItem>
</Tabs>

Ersetze `<name@example.com>` mit Deiner E-Mail-Adresse und `<passwort>` mit einem sicheren Passwort.

<details>
  <summary>
    Erklärung
   </summary>

  <div>
- `--name <container-pgadmin>`: Gibt dem Container den Namen `<container-pgadmin>`.

- `-p 82:80`: Mappt den Port 82 auf den Port 80 im Container. Dies bedeutet, dass Anfragen an Port 82 auf dem Host auf Port 80 im Container weitergeleitet werden.

- `-e PGADMIN_DEFAULT_EMAIL=<name@example.com>`: Setzt die Umgebungsvariable für die Standard-E-Mail-Adresse von PgAdmin auf "name@example.com".

- `-e PGADMIN_DEFAULT_PASSWORD=<password>`: Setzt die Umgebungsvariable für das Standardpasswort von PgAdmin auf .

- `-d dpage/pgadmin4`: Startet den Container im Hintergrund (detach mode) mit dem Image ["dpage/pgadmin4"](https://hub.docker.com/r/dpage/pgadmin4).

![docker-pull-postgres](../assets/docker-run-pgadmin.png)

</div>
</details>

### Schritt 5: Laufende Docker-Container überprüfen

Überprüfe, ob Dein Container laufen:

```bash
docker ps
```

![docker-docker-ps](../assets/docker-ps.png)
:::note
Docker Desktop
![docker-docker-ps2](../assets/docker-ps2.png)
:::

### Schritt 6: pgAdmin im Browser aufrufen

Öffne Deinen Webbrowser und navigiere zu:

:::note
http://localhost:82/
:::

Melde dich mit Deiner `E-Mail-Adresse` und dem `Passwort` an, die Du für pgAdmin festgelegt haben.

![pgadmin-log-page.png](../assets/pgadmin-log-page.png)


### Schritt 7: Verbindung zu PostgreSQL herstellen
<Tabs groupId="pgadmin-initial-config">
  <TabItem value="1" label="Schritt 1">
   ![pgadmin-start-page.png](../assets/pgadmin-start-page.png)

  </TabItem>
  <TabItem value="2" label="Schritt 2">
   ![pgadmin-page_1.png](../assets/pgadmin-page_1.png)

  </TabItem>
  <TabItem value="3" label="Schritt 3">
   ![pgadmin-page_2.png](../assets/pgadmin-page_2.png)

  </TabItem>
  <TabItem value="4" label="Schritt 4">
   ![pgadmin-page_3.png](../assets/pgadmin-page_3.png)

  </TabItem>
</Tabs>

:::note
In pgAdmin erstelle eine neue Serververbindung:

- `Name`: server-name
- `host`: host.docker.internal
- `Maintanance database`: postgres
- `Username`: your-database-username
- `Password`: your-database-password
:::

## Docker compose

<Tabs groupId="docker-compose">
  <TabItem value="full" label="Full Code">

    ```yaml {4-14,16-25} title="docker-compose.yaml"
   version: '3.8'

   services:
      agentAPI:
         image: postgres
         environment:
            POSTGRES_USER: <username>
            POSTGRES_PASSWORD: <password>
            POSTGRES_DB: TEST_SM
         volumes:
            - postgres_data:/var/lib/postgresql/data
         ports:
            - "5432:5432"
         restart: unless-stopped

      agentAPI_pgAdmin:
         image: dpage/pgadmin4
         depends_on:
            - agentAPI
         environment:
            PGADMIN_DEFAULT_EMAIL: <name@example.com>
            PGADMIN_DEFAULT_PASSWORD: <password>
         ports:
            - "82:80"
         restart: unless-stopped

   volumes:
      postgres_data:
    
    ```
</TabItem>

<TabItem value="db" label="Database">
    ```yaml
    agentAPI:
     image: postgres
     environment:
        POSTGRES_USER: <username>
        POSTGRES_PASSWORD: <password>
        POSTGRES_DB: TEST_SM
     volumes:
        - postgres_data:/var/lib/postgresql/data
     ports:
        - "5432:5432"
     restart: unless-stopped
    ```
</TabItem>

<TabItem value="pg" label="pgAdmin">
    ```yaml
    agentAPI_pgAdmin:
     image: dpage/pgadmin4
     depends_on:
        - agentAPI
     environment:
        PGADMIN_DEFAULT_EMAIL: <name@example.com>
        PGADMIN_DEFAULT_PASSWORD: <password>
     ports:
        - "82:80"
     restart: unless-stopped
    ```
</TabItem>

</Tabs>

<details>
   <summary>
      Erklärung
   </summary>
   <div>
      <details>
         <summary>
            1. **Version**:
         </summary>
         <div>
            - `version: '3.8'` definiert, welche Version der Docker Compose-Dienstspezifikation verwendet wird.
         </div>
      </details>
      <details>
         <summary>
            2. **Services**:
         </summary>
         <div>
            - In `services` definiere die Container, die gestartet werden sollen.
         </div>
      </details>
      <details>
         <summary>
            3. **Service: agentAPI (PostgreSQL)**:
         </summary>
         <div>
            - `image`: Verwendet das offizielle `postgres` Docker-Image.
            - `environment`: Stellt Umgebungsvariablen für den Container ein:
            - `POSTGRES_USER`: Der Benutzername für den PostgreSQL Superuser.
            - `POSTGRES_PASSWORD`: Das Passwort für den PostgreSQL Superuser.
            - `POSTGRES_DB`: Der Name der standardmäßig erstellten Datenbank.
            - `volumes`: Ein persistentes Volume namens `postgres_data` wird erstellt und für die Datenhaltung des PostgreSQL-Servers verwendet.
            - `ports`: Die Portweiterleitung von Host `5432` auf Container `5432` ermöglicht den Zugriff auf PostgreSQL von Anwendungen auf dem Hostsystem.
            - `restart`: Die Richtlinie `unless-stopped` sorgt dafür, dass der Container automatisch neu startet, es sei denn er wird manuell gestoppt.
         </div>
      </details>
      <details>
         <summary>
            4. **Service: agentAPI_pgAdmin (pgAdmin)**:
         </summary>
         <div>
            - `image`: Verwendet das offizielle `dpage/pgadmin4` Docker-Image.
            - `depends_on`: Gibt an, dass der `pgadmin`Service vom `postgres`Service abhängt und erst nach dessen Start gestartet werden soll.
            - `environment`: Legt die Anmeldedaten für pgAdmin fest:
            - `PGADMIN_DEFAULT_EMAIL`: Die Standard-E-Mail-Adresse für die Anmeldung bei pgAdmin.
            - `PGADMIN_DEFAULT_PASSWORD`: Das Passwort für die Anmeldung bei pgAdmin.
            - `ports`: Die Portweiterleitung von Host `82` auf Container `80` ermöglicht den Zugriff auf pgAdmin über den Webbrowser auf dem Hostsystem.
            - `restart`: Hier wird ebenfalls `unless-stopped` verwendet, um das gleiche Verhalten wie beim PostgreSQL-Service zu haben.
         </div>
      </details>
      <details>
         <summary>
            5. **Volumes**:
         </summary>
         <div>
            - `postgres_data`: Definiert ein benanntes Docker-Volume, das für die Datenspeicherung des PostgreSQL-Dienstes verwendet wird, und sorgt dafür, dass Daten persistent gespeichert werden und bestehen, selbst wenn der Container neu erstellt wird.
         </div>
      </details>
   </div>
</details>
:::tip
Zum Starten der definierten Dienste speichern Sie das Skript in einer Datei namens `docker-compose.yml` und verwenden dann `docker-compose up -d`, um die Container zu starten. Diese Container können dann zum Betrieb Ihrer PostgreSQL-Datenbank mit pgAdmin als Interface genutzt werden.
:::

```bash title="cmd"
# highlight-next-line
>>>docker-compose up -d
[+] Running 2/4
 - Network agent_api_default               Created                          1.2s 
 - Volume "agent_api_postgres_data"        Created                          1.2s 
 ✔ Container agent_api-agentAPI-1          Started                          0.8s 
 ✔ Container agent_api-agentAPI_pgAdmin-1  Started   
```