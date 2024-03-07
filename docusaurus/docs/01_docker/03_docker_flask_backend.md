---
sidebar_position: 3
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Flask - Backend


## Docker-Compose
<Tabs groupId="docker-compose-flask">
   <TabItem value="full" label="Full Code">
   ```yaml title="docker-compose.yml"
   version: '3.8'

   services:
   db:
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

   pgAdmin:
      image: dpage/pgadmin4
      depends_on:
         - db
      environment:
         PGADMIN_DEFAULT_EMAIL: <name@example.com>
         PGADMIN_DEFAULT_PASSWORD: <password>
      ports:
         - "82:80"
      restart: unless-stopped

   flask_app:
      build:
         context: ./backend
         dockerfile: Dockerfile  # Der Name deiner Dockerfile, falls er nicht standardmäßig 'Dockerfile' heißt
      image: agent_backend # Wenn image auch auf Docker-Hub hochgeladen werden soll: <Docker-Hub-Username>/agent_backend
      ports:
         - "5000:5000"

volumes:
  postgres_data:
   ```
   </TabItem>
   <TabItem value="new" label="Flask">
   ```yaml
   flask_app:
      build:
         context: ./backend
         dockerfile: Dockerfile  # Der Name deiner Dockerfile, falls er nicht standardmäßig 'Dockerfile' heißt
      image: agent_backend # Wenn image auch auf Docker-Hub hochgeladen werden soll: <Docker-Hub-Username>/agent_backend
      ports:
         - "5000:5000"

   ```
   </TabItem>
</Tabs>


### Docker-Compose Befehle

<Tabs groupId="docker-compose-commands">
   <TabItem value="start" label="Start">
      ```bash
      docker-compose up -d
      ```
      ```bash title="cmd"
      # highlight-next-line
      ...\Agent_API> docker-compose up -d
      [+] Running 3/4
      - Network agent_api_default               Created                         1.5s
      ✔ Container agent_api-flask_app-1         Started                         1.2s
      ✔ Container agent_api-agentAPI-1          Started                         1.0s
      ✔ Container agent_api-agentAPI_pgAdmin-1  Started                                             
      ```
   </TabItem>
   <TabItem value="stop" label="Stop">
      ```bash
      docker-compose stop 
      ```
      ```bash title="cmd"
      # highlight-next-line
      ...\Agent_API> docker-compose stop
      [+] Stopping 3/3
      ✔ Container agent_api-flask_app-1         Stopped                         0.4s 
      ✔ Container agent_api-agentAPI_pgAdmin-1  Stopped                         1.9s 
      ✔ Container agent_api-agentAPI-1          Stopped                         0.5s
        ```
   </TabItem>
   <TabItem value="remove" label="Remove">
      ```bash
      docker-compose down 
      ```
      ```bash title="cmd"
      # highlight-next-line
      ...\Agent_API> docker-compose down   
      [+] Running 4/4
      ✔ Container agent_api-agentAPI_pgAdmin-1  Removed                         2.0s 
      ✔ Container agent_api-flask_app-1         Removed                         0.4s 
      ✔ Container agent_api-agentAPI-1          Removed                         0.5s 
      ✔ Network agent_api_default               Removed                         0.3s
      ```
   </TabItem>
</Tabs>